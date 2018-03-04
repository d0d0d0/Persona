from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListItemButton
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from Utilities import BaseScreen
from DeviceScreen import DeviceScreen

CLIENT = None
USERS = None
MANAGER = None
OWN_GROUP = None


class UserScreen(BaseScreen):

	def __init__(self, client, manager, group, **kwargs):
		global CLIENT, USERS, MANAGER, OWN_GROUP
		CLIENT = client
		MANAGER = manager
		USERS = group['users']
		OWN_GROUP = group
		super(UserScreen, self).__init__(**kwargs)
		try:
			user_list = UserList()
			self.add_widget(user_list)
		except Exception as e:
			print 'Error occured in UserScreen: ', str(e)

	def logout(self):
		try:
			result = CLIENT.logout()
			MANAGER.current = 'login'
		except Exception,e:
			print 'Error occured in LoginScreen logout: ', str(e)

	def back(self):
		try:
			MANAGER.current = 'group'
		except Exception,e:
			print 'Error occured in GroupScreen back: ', str(e)

	def get_tag(self):
		try:
			return OWN_GROUP['name'] + "'s Users"
		except Exception,e:
			print 'Error occured in GroupScreen back: ', str(e)

	def add_user_popup(self):
		try:
			global POPUP
			if OWN_GROUP['name'] == 'My Devices':
				popup = Popup(title='Add new user', content=Label(text='You cannot add new user to this group.', font_size=14), size_hint=(None, None), size=(400, 200))
				popup.open()
			else:
				POPUP = AddUserPopup(title='Add new user', size_hint=(None, None), size=(400, 200))
				POPUP.open()
		except Exception,e:
			print 'Error occured in UserScreen add_group_popup: ', str(e)

	def update_ip(self):
		try:
			result = CLIENT.update_ip()
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)


class UserList(GridLayout):

	def __init__(self, **kwargs):
		kwargs['cols'] = 1
		kwargs['col_default_width'] = 100
		kwargs['row_default_height'] = 50
		super(UserList, self).__init__(**kwargs)
		try:
			if USERS != {}:
				devices = { u['user-id']: {'name': u['user-name']} for u in USERS}
				list_item_args_converter = lambda row_index, rec: {'text': rec['name'],
																	'is_selected': False,
																	'size_hint_y': None,
																	'height': 60}

				dict_adapter = DictAdapter(sorted_keys=[i for i in range(len(USERS))],
											data=devices,
											args_converter=list_item_args_converter,
											selection_mode='single',
											allow_empty_selection=False,
											template='CustomUserItem')
				list_view = ListView(adapter=dict_adapter)
				self.add_widget(list_view)
		except Exception as e:
			print 'Error occurred in UserList:', str(e)


class UserListButton(ListItemButton):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['deselected_color'] = [191.0/255, 191.0/255, 191.0/255, 0.5]
		super(UserListButton, self).__init__(**kwargs)

	def click(self, text=None):
		try:
			if not text:
				text = self.text
			for u in USERS:
				if u['user-name'] == text:
					user = {'GROUP_ID': OWN_GROUP['_id'], 'GROUP_NAME': OWN_GROUP['name'], 'USER': u}
					if MANAGER.has_screen('device'):
						MANAGER.remove_widget(MANAGER.get_screen('device'))
					MANAGER.add_widget(DeviceScreen(client=CLIENT, manager=MANAGER, user=user, name='device'))
					MANAGER.current = 'device'
		except Exception as e:
			print 'Error occured in UserListButton: ', str(e)


class AddUserPanel(FloatLayout):

	def add_user(self, user_name):
		try:
			result = CLIENT.add_user(gid=OWN_GROUP['_id'], user_name=user_name)
			if not result:
				self.create_popup(title='New user', text='New user added.')
				MANAGER.remove_widget(MANAGER.get_screen('user'))
				MANAGER.add_widget(UserScreen(client=CLIENT, manager=MANAGER, group=OWN_GROUP, name='user'))
				MANAGER.current = 'user'
			elif result == -1:
				self.create_popup(title='New user', text='User already exists.')
			else:
				self.create_popup(title='Error', text='An error occurred.')
			POPUP.dismiss()
			MANAGER.current = 'group'
		except Exception as e:
			print 'Error occurred in add_user: ', str(e)

	def create_popup(self, title, text):
		try:
			popup = Popup(title=title, content=Label(text=text), font_size=14, size_hint=(None, None), size=(400, 200))
			popup.open()
		except Exception as e:
			print 'Error occurred in create_popup: ', str(e)


class AddUserPopup(Popup):

	def __init__(self, **kwargs):
		super(AddUserPopup, self).__init__(**kwargs)

		popup = AddUserPanel()
		self.add_widget(popup)