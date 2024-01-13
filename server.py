import os, zipfile
import http.server as server
from datetime import datetime

from patcher import Patcher

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/':
		 # for custom response during server check, comment each line below until "# above here"
			self.path = '/data/index.html'
			if not os.path.exists('data/index.html'):
				os.makedirs(os.path.dirname('data/index.html'), exist_ok=True)
				with open('data/index.html', 'a') as fd:
					fd.write('<html><h1><center>NFC Screen Off Patcher</center></h1></html>')
		elif self.path in ['/stats.csv', '/data.csv']:
			self.path = '/data/stats.csv'
		if self.path in ['/data/index.html', '/data/stats.csv']:
			return server.SimpleHTTPRequestHandler.do_GET(self)
		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes('File Not Found', 'utf-8'))
			# above here, and uncomment the 4 "self" lines below
			# custom response example, use 800-899 for built-in client abort after message, or 700-799 to show message and continue patching
			#self.send_response(826)
			#self.send_header('Content-type', 'text/html')
			#self.end_headers()
			#self.wfile.write(bytes('Example custom message', 'utf-8'))
			return

	def do_PUT(self):
		try:
			# save archive
			filename = os.path.basename(self.path)
			file_length = int(self.headers['Content-Length'])
			with open(filename, 'wb') as output_file:
					output_file.write(self.rfile.read(file_length))

			# unzip
			timestamp = int(datetime.timestamp(datetime.now()))
			extract_dir = f'data/{timestamp}'
			with zipfile.ZipFile(filename) as archive:
				archive.extractall(extract_dir)

			# disassemble
			patcher = Patcher.factory(extract_dir)
			patcher.disassemble()

			# temporarily disable patching for known fail states
			#if patcher.sdk >= '34':
			#	patcher.clean()
			#	patcher.log_stats('fail-SDK-34')
			#	self.send_response(535)
			#	self.send_header('Content-type', 'text/html')
			#	self.end_headers()
			#	self.wfile.write(bytes('Test', 'utf-8'))
			#	return

			# check that apk has been successfully disassembled
			if not patcher.is_successfully_disassembled():
				# manufacturer = patcher.manufacturer.replace(' ', '')
				# model = patcher.model.replace(' ', '')
				# os.rename(extract_dir, f'data/fail-{timestamp}-{manufacturer}-{model}')
				patcher.clean()
				patcher.log_stats('fail-disassemble')
				self.send_error(545)
				# Rename the failed patch zip file with the DATE_ID (both lines)
				#failed_patch_filename = f'{patcher.date_id}.zip'
				#os.rename(filename, failed_patch_filename)
				return

			# patch
			patcher.patch_ScreenStateHelper()
			patcher.patch_NfcService()
			patcher.assemble()

			# write aligned apk in response
			with open(f'{extract_dir}/{patcher.apk_name}_align.apk', 'rb') as apk:
				self.send_response(200)
				self.send_header("Content-Type", 'application/vnd.android.package-archive')
				fs = os.fstat(apk.fileno())
				self.send_header("Content-Length", str(fs[6]))
				self.end_headers()
				self.wfile.write(apk.read())

			patcher.clean()
			patcher.log_stats()

		except Exception as error:
			print(timestamp, error)
			patcher.clean()
			patcher.log_stats('exception')
			self.send_response(555)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(bytes('Exception', 'utf-8'))
			# Rename the failed patch zip file with the DATE_ID (both lines)
			#failed_patch_filename = f'{patcher.date_id}.zip'
			#os.rename(filename, failed_patch_filename)

server.test(HandlerClass=HTTPRequestHandler)
