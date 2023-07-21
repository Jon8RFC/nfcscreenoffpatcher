import os, shutil, subprocess
from datetime import datetime
from dotenv import dotenv_values

class Patcher:
	@staticmethod
	def factory(extract_dir):
		env = dotenv_values(f'{extract_dir}/.env')

		date_id = env.get('DATE_ID')
		mod_ver = env.get('MOD_VER')
		manufacturer = env.get('MANUFACTURER')
		model = env.get('MODEL')
		device = env.get('DEVICE')
		rom = env.get('ROM')
		release = env.get('RELEASE')
		sdk = env.get('SDK')
		apk_name = env.get('APK_NAME')
		strategy = env.get('STRATEGY')

		if strategy == 'odex':
			return PatcherOdex(extract_dir, date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_name, 'odex')

		return Patcher(extract_dir, date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_name, 'classic')

	def __init__(self, extract_dir, date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_name, strategy):
		self.extract_dir = extract_dir
		self.date_id = date_id
		self.mod_ver = mod_ver
		self.manufacturer = manufacturer
		self.model = model
		self.device = device
		self.rom = rom
		self.release = release
		self.sdk = sdk
		self.apk_name = apk_name
		self.strategy = strategy

		self.smali_dir = None
		self.on_unlocked_value = None

	def disassemble(self):
		subprocess.run(['./disassemble.sh', self.extract_dir, self.apk_name])
		self.smali_dir = self.get_smali_dir()

	def assemble(self):
		subprocess.run(['./assemble.sh', self.extract_dir, self.apk_name])

	def get_smali_dir(self):
		possible_folders = ['smali', 'smali_classes1', 'smali_classes2', 'smali_classes3', 'smali_classes4', 'smali_classes5', 'smali_classes6', 'smali_classes7', 'smali_classes8', 'smali_classes9']
		for folder in possible_folders:
			path = f'{self.extract_dir}/{self.apk_name}/{folder}'
			if os.path.exists(f'{path}/com/android/nfc'):
				return path 

		return None

	def is_successfully_disassembled(self):
		return self.smali_dir is not None

	def clean(self):
		shutil.rmtree(f'{self.extract_dir}')

	def log_stats(self, status='success'):
		# write headers
		if not os.path.exists('data/stats.csv'):
			with open('data/stats.csv', 'a') as fd:
				fd.write('"date_id","mod_ver","manufacturer","model","device","rom","release","sdk","apk_name","on_unlocked_value","smali_dir","strategy","status","time"\n')

		with open('data/stats.csv', 'a') as fd:
			ts_str = os.path.basename(self.extract_dir)
			date_iso = datetime.fromtimestamp(int(ts_str)).isoformat()
			smali_dir = None if status == 'fail-disassemble' else os.path.basename(self.smali_dir)
			fd.write(f'"{self.date_id}","{self.mod_ver}","{self.manufacturer}","{self.model}","{self.device}","{self.rom}","{self.release}","{self.sdk}","{self.apk_name}","{self.on_unlocked_value}","{smali_dir}","{self.strategy}","{status}","{date_iso}"\n')

	def patch_ScreenStateHelper(self):
		path = f'{self.smali_dir}/com/android/nfc/ScreenStateHelper.smali'
		with open(path) as fd:
			lines = fd.readlines()
			for i, line in enumerate(lines):
				if 'SCREEN_STATE_ON_UNLOCKED' in line:
					self.on_unlocked_value = line.strip().split(' ')[-1]
				if 'checkScreenState' in line:
					insert_index = i + 2

			lines = lines[:insert_index] + [f'const/16 v0, {self.on_unlocked_value}\n', 'return v0\n'] + lines[insert_index:]
		
		with open(path, 'w') as fd:
			fd.writelines(lines)

	def patch_NfcService(self):
		path = f'{self.smali_dir}/com/android/nfc/NfcService.smali'
		with open(path) as fd:
			lines = fd.readlines()
			for i, line in enumerate(lines):
				if 'playSound(' in line:
					insert_index = i + 2

				line = line.replace('SCREEN_OFF', 'SCREEN_OFF_DISABLED')
				line = line.replace('SCREEN_ON', 'SCREEN_ON_DISABLED')
				line = line.replace('USER_PRESENT', 'USER_PRESENT_DISABLED')
				line = line.replace('USER_SWITCHED', 'USER_SWITCHED_DISABLED')
				lines[i] = line

			# patch sound
			if insert_index:
				lines = lines[:insert_index] + ['return-void\n'] + lines[insert_index:]

		with open(path, 'w') as fd:
			fd.writelines(lines)

class PatcherOdex(Patcher):
	def disassemble(self):
		subprocess.run(['./disassemble_odex.sh', self.extract_dir, self.apk_name])
		self.smali_dir = self.get_smali_dir()

	def assemble(self):
		subprocess.run(['./assemble_odex.sh', self.extract_dir, self.apk_name])

	def get_smali_dir(self):
		return f'{self.extract_dir}/smali_classes'
