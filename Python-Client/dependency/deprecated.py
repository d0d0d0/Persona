"""
This file contains deprecated but still possible will-use functions' prototypes in variables.
"""

file_request = '''
			SERVER:
			if command == 'REQUEST_FILE':
				path = args['path'].replace('\\', '/')
				path = shared_dir + '/' + '/'.join(path.split('/')[2:])
				print path
				fdesc = self.get_file(path)
				size = os.path.getsize(path)
				size_dict = {'size': size, 'path': args['path']}
				connection.send(json.dumps(size_dict))
				connection.sendall(fdesc)

			CLIENT:
			if args['command'] == 'REQUEST_FILE':
				fname = (str(args['fname'][0]).split('/'))[-1]
				path = args['path'] + '/' + fname
				ex = os.getcwd() + '/shadow'
				path = path.replace(ex, '')
				ClientLib.transfer_file(sock=sock, path=path, typ='REQUEST')

			TRANSFER_FILE:
			if typ == 'REQUEST':
				command_form['command'] = 'REQUEST_FILE'
				command_form['path'] = path
				sock.send(json.dumps(command_form))
				fname = path.split('/')[-1]
				fdesc = open('downloads/' + fname, 'wb')
				size_dict = json.loads(sock.recv(1024))
				data = sock.recv(1024)
				while data:
					try:
						fdesc.write(data)
						size_dict['size'] -= sys.getsizeof(data)
						if size_dict['size'] < 0:
							break
						data = sock.recv(1024)
					except Exception as e:
						print 'Error occurred during receiving file: ', str(e)
						continue
				fdesc.close()
			'''

virtual_filesystem_create = '''
						def create_virtual_filesystem(self, dict=None, path='./shadow'):
							"""
							Creating a meta directory structure from dictionary
							"""
							path = os.path.join(os.getcwd(), path)
							if not os.path.isdir(path):
								os.mkdir(path)
							try:
								for key,value in dict.iteritems():
									if type(value) is int:
										nested_path = os.path.join(path, key)
										fdesc = open(nested_path, 'wb')
										fdesc.write(str(value))
										fdesc.close()
									else:
										nested_path = os.path.join(path, key)
										os.mkdir(nested_path)
										if value is not {}:
											self.create_virtual_filesystem(dict=value, path=nested_path)
							except Exception as e:
								print e
						'''


directory_struture = '''
				def get_directory_structure(self, rootdir='./shared'):
					"""
					Creates a nested dictionary that represents the folder structure of rootdir
					"""
					shared_dir = rootdir

					def get_dir_size(root, dirt):
						for key,value in dirt.iteritems():
							if value == None:
								nested_path = os.path.join(root, key)
								dirt[key] = os.path.getsize(nested_path)
							else:
								nested_path = os.path.join(root, key)
								get_dir_size(nested_path, value)

					direc = {}
					rootdir = rootdir.rstrip(os.sep)
					start = rootdir.rfind(os.sep) + 1
					for path, dirs, files in os.walk(rootdir):
						folders = path[start:].split(os.sep)
						subdir = dict.fromkeys(files)
						parent = reduce(dict.get, folders[:-1], direc)
						parent[folders[-1]] = subdir


					path = '/'.join(rootdir.split('/')[:-1])
					get_dir_size(path, direc)
					return json.dumps(direc)
				'''

get_file_metadata = '''
				def get_file_metadata(self):
					"""
					Convert root meta data to json object
					"""
					try:
						return json.dumps(self.raw_file_metadata())
					except Exception as e:
						print e
				'''

custom_file_size = '''
				def get_nice_size(self, fn):
					size = 0
					if self.file_system.is_dir(fn):
						return ''
					try:
						if 'shared' in fn:
							try:
								with open(fn) as f:
									for line in f:
										size = int(line)
										break
							except :
								size = self.file_system.getsize(fn)
								#return '--'
						else:
							size = self.file_system.getsize(fn)

					except OSError:
						return '--'

					for unit in {'B', 'KB', 'MB', 'GB'}:
						if size < 1024.0:
							return '%1.0f %s' % (size, unit)
						size /= 1024.0
				'''

chrome_cam = '''
				System.setProperty("webdriver.chrome.driver","C://chromedriver.exe");
				chrome_options = webdriver.ChromeOptions()
				chrome_options.add_argument("--app")

				driver = webdriver.Chrome(chrome_options=chrome_options)
				driver.get("http://www.appr.tc/r/123456789")
				driver.find_element_by_id('confirm-join-button').click()
			'''

linux_charge = '''
			# charge_full_command = 'upower -i ' + battery_dir + ' | grep energy-full:'
			# charge_remaining_command= 'upower -i ' + battery_dir + ' | grep energy:'
			# charge_full = os.popen(charge_full_command).read()[:-4].split(':         ')[-1]
			# charge_remaining = os.popen(charge_remaining_command).read()[:-4].split(':              ')[-1]
			'''

compact_filesystem = '''
			def get_directory_structure(rootdir='./shadow'):
				"""
				Return directory structure in format
				{
					"foldername":[
						{
							"filename": 0
						},
						{
							"filename": 0
						}
				"""
				dic = {rootdir: []}
				if not os.path.isfile(rootdir):
					try:
						for f in os.listdir(rootdir):
							subfolder = os.path.join(rootdir, f)
							dic[rootdir].append(get_directory_structure(subfolder))
					except Exception as e:
						print 'Error occurred: ', str(e)
				else:
					return {rootdir: 0}
				return dic



			def create_virtual_filesystem(dict=None, path='./deneme'):
				"""
				Creating a meta directory structure from dictionary
				"""
				path = os.path.join(os.getcwd(), path)
				if not os.path.isdir(path):
					os.mkdir(path)
				try:
					for key,value in dict.iteritems():
						if value == 0:
							nested_path = os.path.join(path, key)
							fdesc = open(nested_path, 'wb')
							fdesc.close()
						else:
							nested_path = os.path.join(path, key)
							os.mkdir(nested_path)
							if value is not []:
								for v in value:
									create_virtual_filesystem(dict=v, path=path)
				except Exception as e:
					print e
			'''


GRP_DICT_STRCT = '''
		{
			'_id' : gid,
			'name': gname,
			'users': [
						{
							'user-id': uid,
							'user-name': uname,
							'devices': [
											{
												'DEVICE_ID': did,
												'DEVICE_NAME': dname,
												'DEVICE_IP': dip,
												'PERMISSIONS': perm_list

											}

							]
						}
			]
		}
'''

EXMPL_GRP_DICT = [{
				'_id': 12345678,
				'name': 'EV',
				'users': [
					{
						'id': 444444444,
						'user': 'DOGANALP',
						'devices': [
								{
									'DEVICE_ID': 555555555,
									'DEVICE_NAME': 'YENI ALET',
									'DEVICE_IP': '192.168.1.2',
									'PERMISSIONS': ['sensor']
								}
						]

					}


				]
        }]

def GET_GRP_DICT():
	return EXMPL_GRP_DICT