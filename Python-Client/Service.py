import hashlib
import json
import os
import socket
import sys
import uuid
import platform
import ssl
import time
import threading

from multiprocessing import Process
from threading import Semaphore

from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport, TSocket

from project import *
from dependency import *
from dependency import Device

reload(sys);
sys.setdefaultencoding("utf8")

address = [0, 0]
address_sem = Semaphore()


class Service(Process):
	def __init__(self, typ='client'):
		"""
		Thrift TCP Connection
		"""
		self.socket = None              # TSocket.TSocket()
		self.transport = None           # TTransport.TFramedTransport(self.socket)
		self.protocol = None            # TBinaryProtocol.TBinaryProtocol(self.transport)
		self.client = None              # myService.Client(self.protocol)
		self.transport = None           # myService.Client(self.protocol)
		self.p2p = None
		self.typ = typ
		self.auth_key = None
		self.is_con = False
		self.sensor_info = {}
		Process.__init__(self)

	def server_connection(self, ip='188.166.48.245', port=8081):
		"""
		Thrift TCP Connection
		"""
		global address, address_sem
		common_ips = {'home': '192.168.0.12', 'phone': '192.168.43.25', 'docean': '188.166.48.245', 'dept': '144.122.71.154'}
		try:
			self.socket = TSocket.TSocket(common_ips['docean'], port)
			self.socket.setTimeout(5000)
			# self.socket = TSSLSocket.TSSLSocket(host=ip, port=port, ca_certs='dependency/certificate/server.crt')
			self.transport = TTransport.TFramedTransport(self.socket)
			self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
			# self.protocol = TMultiplexedProtocol.TMultiplexedProtocol(self.protocol, "myService")
			self.client = myService.Client(self.protocol)
			self.transport.open()
			address = self.socket.handle.getsockname()
			self.is_con = True
		except Exception as e:
			print 'Error occured in main server connection: ', str(e)
			return False
		except socket.timeout:
			return False
		finally:
			address_sem.release()


	def p2p_client_connection(self, args={}, ip='192.168.0.28', host=55555):

		sock = Transfer.create_socket(ip=args['ip'], host=host) #, ssl_id=args['id'])
		try:
			if args['command'] == 'REQUEST_FILE':
				path = os.path.normpath(args['path']) 
				fname = args['fname']
				Transfer.transfer_file(sock=sock, path=path, fname=fname, typ='REQUEST')

			if args['command'] == 'SEND_FILE':
				path = os.path.normpath(args['path'])
				fname = args['fname']
				Transfer.transfer_file(sock=sock, path=path, fname=fname, typ='SEND')

			if args['command'] == 'SENSORS':
				command_form = {'command': args['command']}
				sock.send(json.dumps(command_form))
				size_dict = json.loads(sock.recv(1024))
				sensors = json.loads(Transfer.transfer_object(sock=sock, obj_size=size_dict['size']))
				return sensors

			if args['command'] == 'LCD':
				command_form = {'command': args['command'], 'text': args['text']}
				sock.send(json.dumps(command_form))

			if args['command'] == 'LED':
				command_form = {'command': args['command'], 'status': args['status']}
				sock.send(json.dumps(command_form))

			if args['command'] == 'BUZZER':
				command_form = {'command': args['command'], 'duration': args['duration']}
				sock.send(json.dumps(command_form))

			if args['command'] == 'FS':
				command_form = {'command': args['command']}
				sock.send(json.dumps(command_form))
				size_dict = json.loads(sock.recv(1024))
				FS = Transfer.transfer_object(sock=sock, obj_size=size_dict['size'])
				print FS
				FS_info = json.loads(FS)
				Device.create_virtual_filesystem(FS_info, '../shadow')

			if args['command'] == 'SSHFS':
				command_form = {'command': args['command']}
				sock.send(json.dumps(command_form))
				size_dict = json.loads(sock.recv(1024))
				ssh_info = json.loads(Transfer.transfer_object(sock=sock, obj_size=size_dict['size']))
				print ssh_info
				remote_adress = '%s@%s:%s' % (ssh_info['username'], args['ip'], ssh_info['path'])
				mount_path = os.getcwd() + '/../shadow/' + ssh_info['username']
				if not os.path.isdir(mount_path):
					os.mkdir(mount_path)
				rsa_path = os.path.expanduser('~') + '/.ssh/id_rsa'
				sshfs_command = 'sshfs -o IdentityFile=%s %s %s' % (rsa_path, remote_adress, mount_path)
				os.popen(sshfs_command)

			if args['command'] == 'WEBRTC':
				command_form = {'command': args['command']}
				sock.send(json.dumps(command_form))
				size_dict = json.loads(sock.recv(1024))
				webrtc_info = json.loads(Transfer.transfer_object(sock=sock, obj_size=size_dict['size']))
				Device.get_camera_webrtc(browser='FIREFOX', room_id=webrtc_info['room_id'])

			if args['command'] == 'LOCATION':
				command_form = {'command': args['command']}
				sock.send(json.dumps(command_form))
				size_dict = json.loads(sock.recv(1024))
				location = json.loads(Transfer.transfer_object(sock=sock, obj_size=size_dict['size']))
				return location['location']

		except Exception as e:
			print 'Error occurred p2p_client_connection: ', str(e)
			return
		finally:
			sock.close()

	def get_sensor_info(self):
		return self.sensor_info

	def p2p_server_connection(self):
		"""
		p2p Thrift SSL Connection
		"""
		#global address, address_sem
		#address_sem.acquire()

		temp_address = ('144.122.246.61', 55555)
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		server_socket.bind(temp_address)
		server_socket.listen(1)
		server_socket.setblocking(0)
		server_socket.settimeout(100000)

		#address_sem.release()

		print >>sys.stderr, 'starting up on %s port %s' % temp_address

		while True:
			try:
				connection, client_address = server_socket.accept()
				# path = os.getcwd() + '/../dependency/certificate/own'
				# connection = ssl.wrap_socket(connection, server_side=True, certfile=path + '.crt', keyfile=path + '.key')
				print >>sys.stderr, 'connection from', client_address
				if connection:
					connection.settimeout(3)
					while True:
						data = connection.recv(1024)
						args = json.loads(data)
						command = args['command'].encode('ascii')
						print command
						print args

						if command == 'REQUEST_FILE':
							path = os.path.normpath(args['path'])
							path = os.getcwd() + '/..' + path
							fdesc = Device.get_file(path)
							size = os.path.getsize(path)
							size_dict = {'size': size, 'path': args['path']}
							connection.send(json.dumps(size_dict))
							connection.sendall(fdesc)

						if command == 'SEND_FILE':
							fname = args['fname']
							fdesc = open('../downloads/' + fname, 'wb')
							data = connection.recv(1024)
							while data:
								try:
									fdesc.write(data)
									data = connection.recv(1024)
								except Exception as e:
									print 'Error occurred during receiving file: ', str(e)
									continue
							fdesc.close()

						if args['command'] == 'FS':
							direc = json.dumps(Device.get_directory_structure(dict={"DirName": '', "SubDirs": [], "Files": []}))
							size_dict = {'size': len(direc)}
							print direc
							connection.send(json.dumps(size_dict))
							connection.sendall(direc)

						if command == 'SSHFS':
							direc = Device.get_sshfs_info()
							size_dict = {'size': len(direc)}
							connection.send(json.dumps(size_dict))
							connection.sendall(direc)

						if command == 'WEBRTC':
							room_id = str(uuid.uuid4().fields[-1])[:8]
							room_info = json.dumps({'room_id': room_id})
							size_dict = {'size': len(room_info)}
							connection.send(json.dumps(size_dict))
							connection.sendall(room_info)
							Device.get_camera_webrtc(room_id=room_id)

						if command == 'LOCATION':
							direc = Device.get_location()
							size_dict = {'size': len(direc)}
							connection.send(json.dumps(size_dict))
							connection.sendall(direc)

						if command == 'SENSORS':
							cur = {key: value for key, value in args.iteritems() if key != 'command'}
							print cur
							if self.sensor_info != cur and cur != {}:
								self.sensor_info = cur
								print 'HANOHA',cur['temperature']

			except Exception as e:
				print 'Error occured p2p server connection: ', str(e)
				continue
			finally:
				pass

	def register(self, username, password, name, email):
		"""
		Register as a new user
		"""
		try:
			passw = hashlib.sha1(password).hexdigest().upper()
			self.server_connection()
			return self.client.registerRequest(username, passw, name, email)
		except Exception as e:
			print e

	def login(self, username, password):
		"""
		Login
		"""
		try:
			print username
			passw = hashlib.sha1(password).hexdigest().upper()
			print passw
			mac = hex(uuid.getnode())
			self.server_connection()
			if not self.is_con:
				return {'result': -1, 'key': None}
			result = json.loads(self.client.login(username, passw, mac))
			return result
		except Exception as e:
			print e

	def add_device(self, device_name, custom_mac=None):
		"""
		Add a new device
		"""
		try:
			print self.auth_key
			# SSL.ssl_certificate_generator()
			mac = hex(uuid.getnode())
			if not custom_mac:
				custom_mac = mac

			cert = (open(os.getcwd() + "/../dependency/certificate/own.crt", "rb")).read()
			home_path = os.path.expanduser('~')
			rsa_pub_path = home_path + '/.ssh/id_rsa.pub'
			if os.path.isfile(rsa_pub_path) and os.access(rsa_pub_path, os.R_OK):
				pass

			rsa_pub = (open(rsa_pub_path, "rb")).read()
			cap = Device.get_capability(platform=platform.system())

			return self.client.addDevice(custom_mac, device_name, cert, cap, rsa_pub, self.auth_key)
		except Exception as e:
			print e

	def get_devices(self):
		"""
		Get all devices
		"""
		try:
			device_list = self.client.getDevices(self.auth_key)
			home_path = os.path.expanduser('~')
			authorized_keys_path = home_path + '/.ssh/authorized_keys'
			fdesc = open(authorized_keys_path, 'a')
			for d in device_list:
				fdesc.write(d.certfile)
			fdesc.close()
			return device_list
		except Exception as e:
			print e

	def get_groups(self, friends):
		"""
		Get all devices
		"""
		try:
			group_list = self.client.getGroups(friends=friends, key=self.auth_key)
			'''
			home_path = os.path.expanduser('~')
			authorized_keys_path = home_path + '/.ssh/authorized_keys'
			fdesc = open(authorized_keys_path, 'a')
			for d in device_list:
				fdesc.write(d.certfile)
			fdesc.close()
			'''
			return json.loads(group_list)['groups']
		except Exception as e:
			print e

	def add_group(self, group_name):
		"""
		Add group
		"""
		try:
			return self.client.addGroup(group_name, self.auth_key)
		except Exception as e:
			print 'Error occured in Service add_group: ', str(e)

	def add_user(self, gid, user_name):
		"""
		Add user to group with gid
		"""
		try:
			return self.client.addUserToGroup(gid, user_name, self.auth_key)
		except Exception as e:
			print 'Error occured in Service add_user: ', str(e)


	def add_device_to_facebook(self,device):
		"""
		Add device to Facebook group
		"""
		try:
			return self.client.addDeviceToFacebook(device, self.auth_key)
		except Exception as e:
			print 'Error occured in Service add_device_to_group: ', str(e)

	def add_device_to_group(self, gid, device):
		"""
		Add device to group
		"""
		try:
			return self.client.addDeviceToGroup(gid, device, self.auth_key)
		except Exception as e:
			print 'Error occured in Service add_device_to_group: ', str(e)

	def update_ip(self):
		"""
		Add device to group
		"""
		try:
			mac = hex(uuid.getnode())
			ip = socket.gethostbyname(socket.gethostname())
			result = self.client.updateIp(mac, ip, self.auth_key)
			return result
		except Exception as e:
			print 'Error occured in Service update_ip: ', str(e)

	def logout(self):
		"""
		Logout
		"""
		try:
			mac = hex(uuid.getnode())
			return self.client.logout(mac, self.auth_key)
		except Exception as e:
			print 'Error occured in Service logout: ', str(e)

	def rename_devices(self):
		"""
		Rename an existing device
		"""
		try:
			mac = hex(uuid.getnode())
			name = raw_input("Enter new name: ")
			return self.client.renameDevice(mac, name, self.auth_key)
		except Exception as e:
			print e

	def run(self):
		"""
		Run as thread
		"""
		if self.typ == 'client':
			self.server_connection()
		elif self.typ == 'server':
			self.p2p_server_connection()
