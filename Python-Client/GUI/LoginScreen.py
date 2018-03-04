# -*- coding: utf-8 -*-

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from GroupScreen import GroupScreen
from Utilities import BaseScreen
from dependency import Device

import threading

CLIENT = None
MANAGER = None
FRIENDS = None
POPUP = None
RECON_POPUP = None
SERVER = None

class LoginScreen(BaseScreen):

	def __init__(self, client, server, manager, **kwargs):
		global CLIENT, MANAGER, SERVER
		CLIENT = client
		MANAGER = manager
		SERVER = server
		super(LoginScreen, self).__init__(**kwargs)

	def login(self, username, password, is_facebook=False):
		global FRIENDS, POPUP, RECON_POPUP, SERVER

		def update_ip_period():
			self.update_ip_repater()
			threading.Timer(120, update_ip_period).start()

		if not is_facebook:
			try:
				response = CLIENT.login(username=username, password=password)
				result = response['result']
				CLIENT.auth_key = response['key']
				if result == 0 or result == 1: #success
					if not result:
						self.create_popup(title='Success', text='Successfully login.')
						if MANAGER.has_screen('group'):
							MANAGER.remove_widget(MANAGER.get_screen('group'))
						MANAGER.add_widget(GroupScreen(client=CLIENT, server=SERVER, manager=MANAGER, friends=None, name='group'))
						MANAGER.current = 'group'
					elif result == 1:
						POPUP = AddDevicePopup(title='New device', size_hint=(None, None), size=(400, 200))
						POPUP.open()
					update_ip_period()
				elif result == -1:
					RECON_POPUP = ReconnectPopup(title='Connection Failed', size_hint=(None, None), size=(500, 200))
					RECON_POPUP.open()
				else:
					self.create_popup(title='Error', text='An error occured.')
			except Exception,e:
				self.create_popup(title='Error', text=('An error occured: ', str(e)))
		elif is_facebook:
			try:
				facebook_info = Device.facebook_login()
			except Exception,e:
				print 'Error occurred in internal Facebook login: ', str('NON')
				return

			if not facebook_info or facebook_info == 'NOT SUCCESSFUL':
				print 'Error occurred in login.'
			else:
				profile = facebook_info.get_object("me")
				raw_friends = facebook_info.get_connections(id='me', connection_name='friends')
				FRIENDS = [Device.string_normalizer(friend['name']) for friend in raw_friends['data']]
				try:
					name = Device.string_normalizer(profile['name'])
					#result = CLIENT.register(username=name, password=profile['id'], name=name, email=name)
					result = CLIENT.register(username=name, password='123', name=name, email=name)
					if not result == 3:
						#response = CLIENT.login(username=name, password=profile['id'])
						response = CLIENT.login(username=name, password='123')
						l_result = response['result']
						CLIENT.auth_key = response['key']
						if l_result == 0 or l_result == 1: #success
							if not l_result:
								self.create_popup(title='Success', text='Successfully login.')
								if MANAGER.has_screen('group'):
									MANAGER.remove_widget(MANAGER.get_screen('group'))
								MANAGER.add_widget(GroupScreen(client=CLIENT, server=SERVER, manager=MANAGER, friends=FRIENDS, name='group'))
								MANAGER.current = 'group'
							elif l_result == 1:
								self.popup = AddDevicePopup(title='Add new device', size_hint=(None, None), size=(400, 200))
								self.popup.open()
							update_ip_period()
						elif l_result == -1:
							RECON_POPUP = ReconnectPopup(title='Connection Failed', size_hint=(None, None), size=(500, 200))
							RECON_POPUP.open()
						else:
							print l_result
							self.create_popup(title='Error', text='An error occurred during Facebook login.')
					else:
						self.create_popup(title='Error', text='An error occurred during Facebook auth.')
				except Exception as e:
					print 'Error occurred in Facebook login: ', str(e)

	def forgot_password(self):
		self.create_popup(title='Password recovery', text='Information mail is sent.')

	def logout(self):
		try:
			pass
		except Exception,e:
			print 'Error occured in LoginScreen logout: ', str(e)

	def back(self):
		try:
			pass
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)

	def update_ip(self):
		try:
			rest = CLIENT.update_ip()
			print rest
			return rest
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)

	def update_ip_repater(self):
		try:
			rest = CLIENT.update_ip()
		except Exception,e:
			print 'Error occured in LoginScreen update_ip_repater: ', str(e)

	def get_tag(self):
		try:
			return 'Login'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)


class AddDevicePopup(Popup):

	def __init__(self, **kwargs):
		super(AddDevicePopup, self).__init__(**kwargs)

		popup = AddDevicePanel()
		self.add_widget(popup)


class ReconnectPopup(Popup):

	def __init__(self, **kwargs):
		super(ReconnectPopup, self).__init__(**kwargs)
		popup = ReconnectPanel()
		self.add_widget(popup)


class ReconnectPanel(FloatLayout):

	def reconnect(self):
		global RECON_POPUP
		try:
			RECON_POPUP.dismiss()
			result = CLIENT.server_connection()
			if not result:
				RECON_POPUP = ReconnectPopup(title='Connection Failed', size_hint=(None, None), size=(500, 200))
				RECON_POPUP.open()
			else:
				pop = Popup(title='Connection Successful', content=Label(text='Successfully connected.'), size_hint=(None, None), size=(400, 200))
				pop.open()

		except Exception as e:
			print 'Error occurred in ReconnectPanel reconnect: ', str(e)


class AddDevicePanel(FloatLayout):

	def add_device(self, device_name):
		global SERVER
		try:
			result = CLIENT.add_device(device_name=device_name)
			if not result:
				self.create_popup(title='New device', text='New device added.')
				MANAGER.add_widget(GroupScreen(client=CLIENT, server=SERVER, manager=MANAGER, friends=FRIENDS, name='group'))
				MANAGER.current = 'group'
			elif result == 1:
				self.create_popup(title='New device', text='Device already exists.')
			else:
				self.create_popup(title='Error', text='An error occurred.')
			POPUP.dismiss()
		except Exception as e:
			print 'Error occurred in add_device: ', str(e)

	def create_popup(self, title, text):
		try:
			popup = Popup(title=title, content=Label(text=text), font_size=14, size_hint=(None, None), size=(400, 200))
			popup.open()
		except Exception as e:
			print 'Error occurred in AddDevicePanel create_popup: ', str(e)



