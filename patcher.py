import os
import shutil
import subprocess
from datetime import datetime
from dotenv import dotenv_values

def safe_value(value):
    return value if value is not None else ''

class Patcher:
    @staticmethod
    def factory(extract_dir):
        env = dotenv_values(f'{extract_dir}/.env')

        date_id = env.get('DATE_ID')
        client_fail = env.get('CLIENT_FAIL')
        response_code = env.get('RESPONSE_CODE')
        zip_error = env.get('ZIP_ERROR')
        repatch = env.get('REPATCH')
        repatch_date_id = env.get('REPATCH_DATE_ID')
        mod_ver = env.get('MOD_VER')
        manufacturer = env.get('MANUFACTURER')
        model = env.get('MODEL')
        device = env.get('DEVICE')
        rom = env.get('ROM')
        release = env.get('RELEASE')
        sdk = env.get('SDK')
        apk_dir = env.get('APK_DIR')
        apk_name = env.get('APK_NAME')
        framework_res_path = env.get('FRAMEWORK_RES_PATH')
        odex_exist = env.get('ODEX_EXIST')
        odex_framework_res_path = env.get('ODEX_FRAMEWORK_RES_PATH')
        strategy = env.get('STRATEGY')

        if strategy == 'odex':
            return PatcherOdex(extract_dir, date_id, client_fail, response_code, zip_error, repatch, repatch_date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_dir, apk_name, framework_res_path, odex_exist, odex_framework_res_path, 'odex')

        return Patcher(extract_dir, date_id, client_fail, response_code, zip_error, repatch, repatch_date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_dir, apk_name, framework_res_path, odex_exist, odex_framework_res_path, 'classic')

    def __init__(self, extract_dir, date_id, client_fail, response_code, zip_error, repatch, repatch_date_id, mod_ver, manufacturer, model, device, rom, release, sdk, apk_dir, apk_name, framework_res_path, odex_exist, odex_framework_res_path, strategy):

        self.extract_dir = extract_dir
        self.date_id = date_id
        self.client_fail = client_fail
        self.response_code = response_code
        self.zip_error = zip_error
        self.repatch = repatch
        self.repatch_date_id = repatch_date_id
        self.mod_ver = mod_ver
        self.manufacturer = manufacturer
        self.model = model
        self.device = device
        self.rom = rom
        self.release = release
        self.sdk = sdk
        self.apk_dir = apk_dir
        self.apk_name = apk_name
        self.framework_res_path = framework_res_path
        self.odex_exist = odex_exist
        self.odex_framework_res_path = odex_framework_res_path
        self.strategy = strategy
        self.smali_dir = None
        self.on_unlocked_value_and12 = None
        self.on_unlocked_value_and13 = None

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
                fd.write('"date_id","client_fail","response_code","zip_error","repatch","repatch_date_id","mod_ver","manufacturer","model","device","rom","release","sdk","apk_dir","apk_name","framework_res_path","odex_exist","odex_framework_res_path","on_unlocked_value","on_unlocked_value_and_ver","smali_dir","strategy","status","time"\n')

        with open('data/stats.csv', 'a') as fd:
            ts_str = os.path.basename(self.extract_dir)
            date_iso = datetime.fromtimestamp(int(ts_str)).isoformat()
            smali_dir = '' if status == 'fail-disassemble' else os.path.basename(self.smali_dir) if self.smali_dir else ''
            on_unlocked_value = safe_value(self.on_unlocked_value_and12) if self.on_unlocked_value_and12 is not None else safe_value(self.on_unlocked_value_and13)
            on_unlocked_value_and_ver = 'and12' if self.on_unlocked_value_and12 is not None else 'and13' if self.on_unlocked_value_and13 is not None else ''
            fd.write(f'"{safe_value(self.date_id)}","{safe_value(self.client_fail)}","{safe_value(self.response_code)}","{safe_value(self.zip_error)}","{safe_value(self.repatch)}","{safe_value(self.repatch_date_id)}","{safe_value(self.mod_ver)}","{safe_value(self.manufacturer)}","{safe_value(self.model)}","{safe_value(self.device)}","{safe_value(self.rom)}","{safe_value(self.release)}","{safe_value(self.sdk)}","{safe_value(self.apk_dir)}","{safe_value(self.apk_name)}","{safe_value(self.framework_res_path)}","{safe_value(self.odex_exist)}","{safe_value(self.odex_framework_res_path)}","{on_unlocked_value}","{on_unlocked_value_and_ver}","{smali_dir}","{safe_value(self.strategy)}","{status}","{date_iso}"\n')

    def patch_ScreenStateHelper(self):
        path = f'{self.smali_dir}/com/android/nfc/ScreenStateHelper.smali'
        with open(path) as fd:
            lines = fd.readlines()

        insert_index = None
        method_start = None
        method_end = None

        for i, line in enumerate(lines):
            if 'SCREEN_STATE_ON_UNLOCKED' in line:
                self.on_unlocked_value_and12 = line.strip().split(' ')[-1]
                break

        if self.on_unlocked_value_and12 is None:
            for i, line in enumerate(lines):
                if '.method static screenStateToString' in line:
                    method_start = i
                elif '.end method' in line and method_start is not None:
                    method_end = i
                    break

            for i in range(method_start, method_end + 1):
                if 'ON_UNLOCKED' in lines[i]:
                    for j in range(i - 1, method_start - 1, -1):
                        if 'const/' in lines[j]:
                            self.on_unlocked_value_and13 = lines[j].strip().split(' ')[-1]
                            break

        for i, line in enumerate(lines):
            if 'checkScreenState' in line:
                insert_index = i + 2
                if self.on_unlocked_value_and12 is not None:
                    lines = lines[:insert_index] + [f'const/16 v0, {self.on_unlocked_value_and12}\n', 'return v0\n'] + lines[insert_index:]
                elif self.on_unlocked_value_and13 is not None:
                    lines = lines[:insert_index] + [f'const/16 v0, {self.on_unlocked_value_and13}\n', 'return v0\n'] + lines[insert_index:]

        with open(path, 'w') as fd:
            fd.writelines(lines)

    def patch_NfcService(self):
        path = f'{self.smali_dir}/com/android/nfc/NfcService.smali'
        with open(path) as fd:
            lines = fd.readlines()

        insert_index = None

        for i, line in enumerate(lines):
            if 'playSound(' in line:
                insert_index = i + 2
            if self.on_unlocked_value_and12 is not None:
                # the below appear to be what break the service after some time in android 13 ~May 2023+, and also cause crashes in android 14
                line = line.replace('SCREEN_OFF', 'SCREEN_OFF_DISABLED')
                line = line.replace('SCREEN_ON', 'SCREEN_ON_DISABLED')
                line = line.replace('USER_PRESENT', 'USER_PRESENT_DISABLED')
                line = line.replace('USER_SWITCHED', 'USER_SWITCHED_DISABLED')
                lines[i] = line
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
