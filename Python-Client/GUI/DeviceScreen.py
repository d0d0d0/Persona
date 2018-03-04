from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.core.window import Window
from kivy.uix.bubble import Bubble
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock


from FileSystemScreen import FileSystemScreen
from FunctionalityList import FunctionalityList
from Utilities import BaseScreen

import subprocess
import platform
import ast
import time
import os

RAW_DEVICES = []
CLIENT = None
MANAGER = None
TAG = None
POPUP = None
CUR = None


class DeviceScreen(BaseScreen):

	def __init__(self, client, manager, user= None, **kwargs):
		global CLIENT, MANAGER, RAW_DEVICES, TAG
		CLIENT = client
		MANAGER = manager
		TAG = user['USER']['user-name']
		RAW_DEVICES = user['USER']['devices']
		super(DeviceScreen, self).__init__(**kwargs)
		try:
			device_list = DeviceList()
			self.add_widget(device_list)
		except Exception as e:
			print 'Error occurred in DeviceScreen: ', str(e)

	def logout(self):
		try:
			# TODO: Logout response handler
			result = CLIENT.logout()
			MANAGER.current = 'login'
		except Exception,e:
			print 'Error occured in LoginScreen logout: ', str(e)

	def update_ip(self):
		try:
			result = CLIENT.update_ip()
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)

	def back(self):
		try:
			MANAGER.current = 'user'
		except Exception,e:
			print 'Error occured in DeviceScreen back: ', str(e)

	def get_tag(self):
		try:
			return TAG + "'s Devices"
		except Exception,e:
			print 'Error occured in DeviceScreen get_tag: ', str(e)


class DeviceList(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 1
		kwargs['col_default_width'] = 100
		kwargs['row_default_height'] = 50
		super(DeviceList, self).__init__(**kwargs)

		try:
			if RAW_DEVICES:
				devices = { d['_id']: {'name': d['name'], 'status': d['status']} for d in RAW_DEVICES}
				for d in RAW_DEVICES:
					if d['cert'] != '':
						path = os.getcwd() + '/../dependency/certificate/' + str(d['_id']) + '.crt'
						if not os.path.lexists(path):
							cert = open(path, 'wb')
							cert.write(d['cert'])
							cert.close()



				list_item_args_converter = lambda row_index, rec: {'text': rec['name'],
																	'is_selected': False,
																	'size_hint_y': None,
																	'height': 60}

				dict_adapter = DictAdapter(sorted_keys=[i for i in range(len(RAW_DEVICES))],
											data=devices,
											args_converter=list_item_args_converter,
											selection_mode='single',
											allow_empty_selection=False,
											template='CustomListItem')
				list_view = ListView(adapter=dict_adapter)
				self.add_widget(list_view)
		except Exception as e:
			print 'Error occurred in DeviceList: ', str(e)


class DeviceListButton(ListItemButton):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['deselected_color'] = [191.0/255, 191.0/255, 191.0/255, 0.5]
		super(DeviceListButton, self).__init__(**kwargs)

		Window.bind(mouse_pos=self.on_mouse_pos)

		self.tooltip = CapabilityHover()

	def get_remote_filesystem(self):
		try:
			typ = self.get_type(CUR)
			args = None
			if typ == 'mobile':
				args = {'command': 'FS', 'ip': self.get_ip(), 'id': self.get_id()}
			elif typ == 'desktop':
				args = {'command': 'SSHFS', 'ip': self.get_ip(), 'id': self.get_id()}
			CLIENT.p2p_client_connection(args=args)
			path = '../shadow'

			if typ == 'mobile':
				self.get_local_filesystem()
			else:
				if platform.system() == "Windows":
					os.startfile(path)
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", path])
				else:
					subprocess.Popen(["xdg-open", path])
		except Exception as e:
			print 'Error occurred in get_remote_filesystem: ', str(e)

	def get_local_filesystem(self):
		try:
			ip = None
			if not MANAGER.has_screen('file_system'):
				for d in RAW_DEVICES:
					if d['name'] == CUR:
						ip = d['ip']
				MANAGER.add_widget(FileSystemScreen(client=CLIENT, manager=MANAGER, ip=ip, name='file_system'))
			MANAGER.current = 'file_system'
		except Exception as e:
			print 'Error occurred in get_local_filesystem: ', str(e)

	def camera_request(self):
		try:
			args = {'command': 'WEBRTC', 'ip': self.get_ip(), 'id': self.get_id()}
			CLIENT.p2p_client_connection(args=args)
		except Exception as e:
			print 'Error occurred in camera_request: ', str(e)

	def sensor_formatter(self, result):
		def value(typ):
			if typ == 'Temperature':
				return ' C'
			if typ == 'Sound':
				return ' dB'
			if typ == 'Light':
				return ' L'
			return ''

		grid = SensorGrid()
		for name, info in result.iteritems():
			sensor_tag = Label(text='[b]' + str(name) + '[/b]: ', font_size=14, markup=True, halign='left')
			sensor_info = Label(text=str(info) + value(str(name)), font_size=13, halign='right')
			grid.add_widget(sensor_tag)
			grid.add_widget(sensor_info)
		return grid

	def sensor_request(self):
		try:
			args = {'command': 'SENSORS', 'ip': self.get_ip(), 'id': self.get_id()}
			result = CLIENT.p2p_client_connection(args=args)
			grid = self.sensor_formatter(result)
			popup = Popup(title='Sensor Information', content=grid, size_hint=(None, None), size=(300, len(result)*75))
			popup.open()

		except Exception as e:
			print 'Error occurred in camera_request: ', str(e)

	def other_request(self):
		try:
			# args = {'command': 'LCD', 'text': 'Ertan is the best', 'id': 'DEFAULT'}
			# CLIENT.p2p_client_connection(args=args)

			args = {'command': 'LED', 'status': 1, 'ip':self.get_ip(), 'id': 'DEFAULT'}
			CLIENT.p2p_client_connection(args=args)
			self.sensor_request()
			time.sleep(2)
			args = {'command': 'BUZZER', 'duration': 3, 'ip':self.get_ip(), 'id': 'DEFAULT'}
			# CLIENT.p2p_client_connection(args=args)
			popup = PanelWrite(title="Enter a message", ip=self.get_ip(), size_hint=(None, None), size=(450, 250))
			popup.open()
		except Exception as e:
			print 'Error occurred in other_request: ', str(e)

	def get_location(self):
		try:
			args = {'command': 'LOCATION', 'ip': self.get_ip(), 'id': self.get_id()}
			location = CLIENT.p2p_client_connection(args=args)
			popup = Popup(title=self.text + "'s Location", content=Label(text=location, text_size=(self.width*6, None)), size_hint=(None, None), size=(450, 250))
			popup.open()
		except Exception as e:
			print 'Error occurred in get_location: ', str(e)

	def get_type(self, dname):
		try:
			for d in RAW_DEVICES:
				if d['name'] == dname:
					cap = ast.literal_eval(d['capabilities'])
					return cap['type']
		except Exception as e:
			print 'Error occurred in get_type: ', str(e)

	def get_id(self):
		try:
			for d in RAW_DEVICES:
				if d['name'] == self.text:
					return str(d['_id'])
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

	def status_color(self, device_name):
		for d in RAW_DEVICES:
			if d['name'] == device_name:
				status = d['status']
				if status:
					return [0.5, 0.5, 0.5, 0.5]
				else:
					return [0.5, 0.5, 0.5, 0.2]

	def click(self):
		try:
			global POPUP, CUR
			CUR = self.text
			device = None
			permissions = None
			for d in RAW_DEVICES:
				if d['name'] == self.text:
					permissions = d['permissions']
					device = d
			if device['status']:
				POPUP = DevicePopup(title=self.text + "'s Functions", size_hint=(None, None), size=(375, 300), permissions=permissions, index=0)
				POPUP.open()
			else:
				popup = Popup(title='Device Offline', content= Label(text=(self.text + ' is not online.'), font_size='13sp', markup=True), size_hint=(None, None), size=(300, 200))
				popup.open()
				MANAGER.current = 'group'
		except Exception as e:
			print 'Error occurred in click: ', str(e)

	def on_mouse_pos(self, *args):
		try:
			if not self.get_root_window():
				return
			pos = args[1]
			self.tooltip.pos = pos
			Clock.unschedule(self.display_tooltip)          # cancel scheduled event since I moved the cursor
			self.close_tooltip()                            # close if it's opened
			if self.collide_point(*self.to_widget(*pos)):
				Clock.schedule_once(self.display_tooltip, 0.2)
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
					if d['name'] == self.text:
						cap_dict = ast.literal_eval(d['capabilities'])
				self.tooltip.get_capabilities(cap_dict=cap_dict)

			self.tooltip.x = self.width - 200
			self.tooltip.y -= self.tooltip.height
			Window.add_widget(self.tooltip)
		except Exception as e:
			print 'Error occurred in display_tooltip: ', str(e)

	def get_ip(self):
		for d in RAW_DEVICES:
			if d['name'] == CUR:
				print d['name'], CUR
				print d['ip']
				return d['ip']


class CapabilityHover(Bubble):

	def __init__(self, **kwargs):
		kwargs['arrow_pos'] = 'top_mid'
		kwargs['orientation'] = 'vertical'
		super(CapabilityHover, self).__init__(**kwargs)

	def get_capabilities(self, cap_dict):
		try:
			size = 0
			model_name = Label(text=('[b]Model[/b]: ' + cap_dict['model_name']), font_size='13sp', markup=True)
			camera = Label(text=('[b]Camera[/b]: ' + cap_dict['camera']), font_size='13sp', markup=True)
			bluetooth = Label(text=('[b]Bluetooth[/b]: ' + cap_dict['bluetooth_addr']), font_size='13sp', markup=True)
			battery = Label(text=('[b]Battery[/b]: ' + str(cap_dict['charge']) + '%'), font_size='13sp', markup=True)

			self.add_widget(model_name)
			self.add_widget(camera)
			self.add_widget(bluetooth)
			self.add_widget(battery)

			if cap_dict['type'] == 'mobile':
				sensors = (cap_dict['sensors'][1:-1]).split(',')
				size += len(sensors)
				for s in sensors:
					s_label = Label(text=('[b]Sensor[/b]: ' + s), font_size='13sp', markup=True)
					self.add_widget(s_label)
			size += 4
			self.size_hint = (0.5, 0.04*size)
		except Exception as e:
			print 'Error occurred in get_capabilities: ', str(e)


class DevicePopup(Popup):

	def __init__(self, permissions, **kwargs):
		super(DevicePopup, self).__init__(**kwargs)
		popup = FunctionalityList(permissions=permissions, row_force_default=True, row_default_height=70)
		self.add_widget(popup)


class PanelWrite(Popup):

	def __init__(self, ip, **kwargs):
		self.ip = ip
		super(PanelWrite, self).__init__(**kwargs)

	def write_panel(self, text):
		args = {'command': 'LCD', 'text': text, 'ip': self.ip, 'id': 'DEFAULT'}
		CLIENT.p2p_client_connection(args=args)


class SensorGrid(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 2
		kwargs['col_default_width'] = 75
		kwargs['row_default_height'] = 55

		super(SensorGrid, self).__init__(**kwargs)
