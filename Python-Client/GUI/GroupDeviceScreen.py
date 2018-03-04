from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.core.window import Window
from kivy.uix.bubble import Bubble
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.label import Label
from kivy.clock import Clock

from Utilities import BaseScreen

import ast
import json


RAW_DEVICES = []
CLIENT = None
MANAGER = None
GID = None
CUR = None
IS_FACEBOOK = None
POPUP = None


def normalize(text):
	return (text.replace(' ', '')).lower()


class GroupDeviceScreen(BaseScreen):

	def __init__(self, client, manager, gid, is_facebook, **kwargs):
		global CLIENT, MANAGER, RAW_DEVICES, GID, IS_FACEBOOK
		CLIENT = client
		MANAGER = manager
		RAW_DEVICES = CLIENT.get_devices()
		GID = gid
		IS_FACEBOOK = is_facebook
		super(GroupDeviceScreen, self).__init__(**kwargs)
		try:
			device_list = GroupDeviceList()
			self.add_widget(device_list)
		except Exception as e:
			print 'Error occurred in GroupDeviceScreen: ', str(e)

	def logout(self):
		try:
			result = CLIENT.logout()
			MANAGER.current = 'login'
		except Exception,e:
			print 'Error occured in GroupDeviceScreen logout: ', str(e)

	def back(self):
		try:
			MANAGER.current = 'group'
		except Exception,e:
			print 'Error occured in GroupDeviceScreen back: ', str(e)

	def get_tag(self):
		try:
			return 'My Devices'
		except Exception,e:
			print 'Error occured in GroupScreen back: ', str(e)

	def update_ip(self):
		try:
			result = CLIENT.update_ip()
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)


class GroupDeviceList(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 1
		kwargs['col_default_width'] = 100
		kwargs['row_default_height'] = 50
		super(GroupDeviceList, self).__init__(**kwargs)

		try:
			if RAW_DEVICES:
				devices = { d.id: {'name': d.name, 'status': d.status} for d in RAW_DEVICES}
				list_item_args_converter = lambda row_index, rec: {'text': rec['name'],
																	'is_selected': False,
																	'size_hint_y': None,
																	'height': 60}

				dict_adapter = DictAdapter(sorted_keys=[i for i in range(len(RAW_DEVICES))],
											data=devices,
											args_converter=list_item_args_converter,
											selection_mode='single',
											allow_empty_selection=False,
											template='CustomGroupDeviceItem')
				list_view = ListView(adapter=dict_adapter)
				self.add_widget(list_view)
		except Exception as e:
			print 'Error occurred in GroupDeviceList: ', str(e)


class GroupDeviceListButton(ListItemButton):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['deselected_color'] = [191.0/255, 191.0/255, 191.0/255, 0.5]
		super(GroupDeviceListButton, self).__init__(**kwargs)

		Window.bind(mouse_pos=self.on_mouse_pos)
		self.permissions = {
					'sshfs': False, 'sendfile': False, 'gps': False,
					'sensor': False, 'camera': False, 'other': False
					}
		self.tooltip = CapabilityHover()

	def add_device(self):
		try:
			global CUR, POPUP
			CUR = self.text
			POPUP = CapabilityPopup(title='Permissions', size_hint=(None, None), size=(320, 500))
			POPUP.open()

		except Exception, e:
			print 'Error occured in GroupDeviceListButton add_device: ', str(e)

	def toggle(self, func):
		try:
			self.permissions[normalize(func)] = not self.permissions[normalize(func)]
		except Exception, e:
			print 'Error occured in GroupScreen toggle: ', str(e)

	# TODO: Error popups needed
	def add_confirm(self):
		try:
			device = None
			for d in RAW_DEVICES:
				if d.name == CUR:
					device = d
			device = {'did': device.id, 'permissions': self.permissions}
			if IS_FACEBOOK:
				CLIENT.add_device_to_facebook(json.dumps(device))
			else:
				CLIENT.add_device_to_group(GID, json.dumps(device))
			POPUP.dismiss()
			MANAGER.current = 'group'
		except Exception, e:
			print 'Error occured in GroupDeviceListButton add_confirm: ', str(e)

	def get_type(self, dname):
		try:
			for d in RAW_DEVICES:
				if d.name == dname:
					cap = ast.literal_eval(d.functionality)
					return cap['type']
		except Exception as e:
			print 'Error occurred in get_type: ', str(e)

	def get_logo(self, dname):
		typ = self.get_type(dname)
		try:
			if typ == 'desktop':
				return "../static/comp_logo.png"
			elif typ == 'mobile':
				return "../static/mob_logo.png"
			return "../static/edison.png"
		except Exception as e:
			print 'Error occurred in get_logo: ', str(e)

	def on_mouse_pos(self, *args):
		try:
			if not self.get_root_window():
				return
			pos = args[1]
			self.tooltip.pos = pos
			Clock.unschedule(self.display_tooltip)          # cancel scheduled event since I moved the cursor
			self.close_tooltip()                            # close if it's opened
			if self.collide_point(*self.to_widget(*pos)):
				Clock.schedule_once(self.display_tooltip, 0.5)
		except Exception as e:
			print 'Error occurred in on_mouse_pos: ', str(e)

	def close_tooltip(self, *args):
		try:
			Window.remove_widget(self.tooltip)
		except Exception as e:
			print 'Error occurred in close_tooltip: ', str(e)

	def display_tooltip(self, *args):
		cap_dict = {}
		try:
			if len(self.tooltip.content.children) == 0:
				for d in RAW_DEVICES:
					if d.name == self.text:
						cap_dict = ast.literal_eval(d.functionality)
				self.tooltip.get_capabilities(cap_dict=cap_dict)

			self.tooltip.x = self.width - 100
			self.tooltip.y -= self.height * 2
			Window.add_widget(self.tooltip)
		except Exception as e:
			print 'Error occurred in display_tooltip: ', str(e)


class CapabilityHover(Bubble):

	def __init__(self, **kwargs):
		kwargs['arrow_pos'] = 'top_mid'
		kwargs['orientation'] = 'vertical'
		kwargs['size_hint'] = (0.45, 0.2)
		super(CapabilityHover, self).__init__(**kwargs)

	def get_capabilities(self, cap_dict):
		try:
			model_name = Label(text=('Model: ' + cap_dict['model_name']), font_size='12sp')
			camera = Label(text=('Camera: ' + cap_dict['camera']), font_size='12sp')
			bluetooth = Label(text=('Bluetooth: ' + cap_dict['bluetooth_addr']), font_size='12sp')
			battery = Label(text=('Battery: ' + str(cap_dict['charge']) + '%'), font_size='12sp')

			self.add_widget(model_name)
			self.add_widget(camera)
			self.add_widget(bluetooth)
			self.add_widget(battery)

			if cap_dict['type'] == 'mobile':
				sensors = (cap_dict['sensors'][1:-1]).split(',')
				for s in sensors:
					s_label = Label(text=('Sensor: ' + s), font_size='12sp')
					self.add_widget(s_label)
		except Exception as e:
			print 'Error occurred in get_capabilities: ', str(e)


class CapabilitySwitch(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 2
		kwargs['col_default_width'] = 75
		kwargs['row_default_height'] = 55

		super(CapabilitySwitch, self).__init__(**kwargs)


class CapabilityPopup(Popup):

	def __init__(self, **kwargs):
		super(CapabilityPopup, self).__init__(**kwargs)
		popup = CapabilitySwitch(row_force_default=True, row_default_height=70)
		self.add_widget(popup)