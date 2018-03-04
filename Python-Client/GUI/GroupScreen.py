from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from GroupDeviceScreen import GroupDeviceScreen
from Utilities import BaseScreen
from dependency import deprecated
from UserScreen import UserScreen

import threading
from random import randint


GROUPS = deprecated.GET_GRP_DICT()
CLIENT = None
MANAGER = None
FRIENDS = None
POPUP = None
SERVER = None

class GroupScreen(BaseScreen):

	def __init__(self, client, server, manager, friends, **kwargs):
		global CLIENT, MANAGER, GROUPS, FRIENDS, SERVER

		CLIENT = client
		MANAGER = manager
		FRIENDS = friends
		SERVER = server
		self.grouplist = GroupList()
		self.sensor = {}

		self.sensor_period()
		super(GroupScreen, self).__init__(**kwargs)
		try:
			pass
		except Exception as e:
			print 'Error occured in GroupScreen: ', str(e)

	def sensor_period(self):
		self.sensor_repater()
		threading.Timer(120, self.sensor_period).start()

	def on_enter_refresh(self):
		global CLIENT, GROUPS
		GROUPS = CLIENT.get_groups(friends=FRIENDS)
		try:
			self.remove_widget(self.grouplist)
			self.grouplist = GroupList()
			self.add_widget(self.grouplist)
		except Exception as e:
			print 'Error occured in GroupScreen: ', str(e)

	def logout(self):
		try:
			result = CLIENT.logout()
			MANAGER.current = 'login'
		except Exception,e:
			print 'Error occured in GroupScreen logout: ', str(e)

	def back(self):
		try:
			pass
		except Exception,e:
			print 'Error occured in GroupScreen back: ', str(e)

	def get_tag(self):
		try:
			return 'Groups'
		except Exception,e:
			print 'Error occured in GroupScreen back: ', str(e)

	def add_group_popup(self):
		try:
			global POPUP
			POPUP = AddGroupPopup(title='Add new group', size_hint=(None, None), size=(400, 200))
			POPUP.open()
		except Exception,e:
			print 'Error occured in GroupScreen add_group_popup: ', str(e)

	def update_ip(self):
		try:
			result = CLIENT.update_ip()
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)

	def sensor_repater(self):
		try:
			global SERVER
			# temp = SERVER.get_sensor_info()
			temp = self.get_temperature()
			self.sensor = temp
			print 'SENSOR', str(self.sensor)

			popup = Popup(title='Telosb Temperature', content=Label(text=str(self.sensor['temperature'])),
			              pos_hint={'x': 0.85, 'y': 0.1}, size_hint=(None, None), size=(120, 120), background_color=(0, 0, 0, 0))
			popup.open()
		except Exception,e:
			print 'Error occured in LoginScreen sensor_repater: ', str(e)

	def get_temperature(self):
		temp = ['30', '31', '32', '29', '28', '33']
		x = randint(0, 5)
		self.sensor = {'temperature': temp[x]}
		return self.sensor



class GroupList(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 1
		kwargs['col_default_width'] = 100
		kwargs['row_default_height'] = 50
		super(GroupList, self).__init__(**kwargs)
		try:
			if GROUPS != {}:
				devices = { g['_id']: {'name': g['name']} for g in GROUPS if g['name'] != 'FacebookFriends'}
				list_item_args_converter = lambda row_index, rec: {'text': rec['name'],
																	'is_selected': False,
																	'size_hint_y': None,
																	'height': 60 }

				dict_adapter = DictAdapter(sorted_keys=[i for i in range(len(GROUPS))],
											data=devices,
											args_converter=list_item_args_converter,
											selection_mode='single',
											allow_empty_selection=False,
											template='CustomGroupItem')
				list_view = ListView(adapter=dict_adapter)
				self.add_widget(list_view)
		except Exception as e:
			print 'Error occurred in GroupList:', str(e)


class GroupListButton(ListItemButton):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['deselected_color'] = [191.0/255, 191.0/255, 191.0/255, 0.5]
		super(GroupListButton, self).__init__(**kwargs)

	def click(self):
		try:
			for g in GROUPS:
				if g['name'] == self.text:
					if MANAGER.has_screen('user'):
						MANAGER.remove_widget(MANAGER.get_screen('user'))
					MANAGER.add_widget(UserScreen(client=CLIENT, manager=MANAGER, group=g, name='user'))
					MANAGER.current = 'user'
		except Exception as e:
			print 'Error occured in GroupListButton: ', str(e)

	def add_device(self):
		try:
			gid = None
			is_facebook = False
			for g in GROUPS:
				if g['name'] == self.text:
					gid = g['_id']
			if self.text == 'Facebook Friends':
				is_facebook = True
			if MANAGER.has_screen('add_device'):
				MANAGER.remove_widget(MANAGER.get_screen('add_device'))
			MANAGER.add_widget(GroupDeviceScreen(client=CLIENT, manager=MANAGER, gid=gid,
													is_facebook=is_facebook, name='add_device'))
			MANAGER.current = 'add_device'
		except Exception, e:
			print 'Error occured in GroupScreen add_device: ', str(e)


class AddGroupPanel(FloatLayout):

	def add_group(self, group_name):
		try:
			POPUP.dismiss()
			result = CLIENT.add_group(group_name=group_name)
			if not result:
				self.create_popup(title='New group', text='New group added.')
				MANAGER.remove_widget(MANAGER.get_screen('group'))
				MANAGER.add_widget(GroupScreen(client=CLIENT, server=SERVER, manager=MANAGER, friends=FRIENDS, name='group'))
				MANAGER.current = 'group'
			elif result == -1:
				self.create_popup(title='New group', text='Group already exists.')
			else:
				self.create_popup(title='Error', text='An error occurred.')
			MANAGER.current = 'group'
		except Exception as e:
			print 'Error occurred in add_group: ', str(e)

	def create_popup(self, title, text):
		try:
			popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 200))
			popup.open()
		except Exception as e:
			print 'Error occurred in Group create_popup: ', str(e)


class SensorContext(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 2
		kwargs['col_default_width'] = 75
		kwargs['row_default_height'] = 55

		super(SensorContext, self).__init__(**kwargs)


class AddGroupPopup(Popup):

	def __init__(self, **kwargs):
		super(AddGroupPopup, self).__init__(**kwargs)

		popup = AddGroupPanel()
		self.add_widget(popup)