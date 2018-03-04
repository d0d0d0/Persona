from kivy.uix.filechooser import FileChooserIconView
from Utilities import BaseScreen

import os

CLIENT = None
MANAGER = None
IP = None

class FileSystemScreen(BaseScreen):

	def __init__(self, client, manager, ip, **kwargs):
		global CLIENT, MANAGER, IP
		CLIENT = client
		MANAGER = manager
		IP = ip
		super(FileSystemScreen, self).__init__(**kwargs)

	def send(self, path, file):
		args = {'command': 'SEND_FILE', 'path': path, 'ip': IP, 'fname': file, 'id':'BLAH'}
		CLIENT.p2p_client_connection(args)

	def request(self, path, file):
		try:
			f_name = os.path.normcase(file[0])
			remote_path = f_name.split('shadow')[-1]
			remote_file = (f_name.split('/'))[-1]

			print remote_path, remote_file
			args = {'command': 'REQUEST_FILE', 'path': remote_path, 'ip': IP, 'fname': remote_file, 'id':'BLAH'}

			CLIENT.p2p_client_connection(args)
		except Exception,e :
			print 'Error occurred in request file: ', str(e)

	def get_tag(self):
		try:
			return 'File System'
		except Exception,e:
			print 'Error occured in FileSystemScreen get_tag: ', str(e)

	def logout(self):
		try:
			# TODO: Logout response handler
			result = CLIENT.logout()
			MANAGER.current = 'login'
		except Exception,e:
			print 'Error occured in FileSystemScreen logout: ', str(e)

	def back(self):
		try:
			MANAGER.current = 'device'
		except Exception,e:
			print 'Error occured in FileSystemScreen back: ', str(e)

	def update_ip(self):
		try:
			result = CLIENT.update_ip()
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)


class RemoteFileChooserView(FileChooserIconView):

	def __init__(self, **kwargs):
		super(RemoteFileChooserView, self).__init__(**kwargs)

	def get_root(self):
		return os.getcwd() + '/../shadow'