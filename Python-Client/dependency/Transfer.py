"""
This file contains functions that allows file and object transfer in both ways.

	-Create an asynchronous generic socket

	-Transfer meta information and small objects in size

	-Transfer files
"""


import socket
import json
import sys
import ssl
import os


def create_socket(ip, host, ssl_id=None):
	"""
	Returns an asynchronous client socket
	"""
	try:
		server_address = (ip, host)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setblocking(0)
		sock.settimeout(15)
		if ssl_id:
			path = os.getcwd() + '/../dependency/certificate/' + ssl_id + '.crt'
			ssl_sock = ssl.wrap_socket(sock, ca_certs=path, cert_reqs=ssl.CERT_REQUIRED)
			ssl_sock.connect(server_address)
			return ssl_sock
		sock.connect(server_address)

	except Exception as e:
		print 'Error occurred in socket: ', str(e)

	return sock


def transfer_object(sock, obj_size):
	"""
	Transfers meta object
	"""
	try:
		size = obj_size
		obj = ''
		while size > 0:
			try:
				new_data = sock.recv(1024)
				obj += new_data
				size -= len(new_data)
			except socket.timeout:
				continue
		return obj
	except Exception as e:
		print e
	finally:
		sock.close()


def transfer_file(sock, path, fname='default', typ='SEND'):
	"""
	Transfers large files in chunks
	"""
	try:
		if typ == 'SEND':
			command_form = {'command': '', 'fname': ''}
			command_form['command'] = 'SEND_FILE'
			command_form['fname'] = fname[0].split('/')[-1]
			print path
			sock.send(json.dumps(command_form))
			fdesc = open(fname[0], 'rb')
			chunk = fdesc.read(1024)
			i = 0
			while chunk:
				try:
					sock.send(chunk)
					chunk = fdesc.read(1024)
					if not chunk:
						break
					i += 1
				except Exception as e:
					print 'Error occurred during sending file: ', str(e)
					continue
			fdesc.close()

		if typ == 'REQUEST':
			command_form = {'command': '', 'path': ''}
			command_form['command'] = 'REQUEST_FILE'
			command_form['path'] = fname[0]
			sock.send(json.dumps(command_form))
			fdesc = open('../downloads/' + fname[0].split('/')[-1], 'wb')
			size_dict = json.loads(sock.recv(1024))
			data = sock.recv(1024)
			while data:
				try:
					fdesc.write(data)
					size_dict['size'] -= len(data)
					print sys.getsizeof(data)
					if size_dict['size'] < 0:
						break
					data = sock.recv(1024)
				except Exception as e:
					print 'Error occurred during receiving file: ', str(e)
					continue
			fdesc.close()

	except Exception as e:
		print 'Error occurred during file transfer: ', str(e)
	finally:
		sock.close