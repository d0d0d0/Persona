from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from re import match


def validation_username(username):
	"""
	Only letters and digits and be 8 characters long
	"""
	valid_username = '^[a-zA-Z0-9]{8,}$'
	try:
		if match(valid_username, username):
			return True
		return False
	except Exception,e:
		print 'Error occurred in Utilities validation_username: ', str(e)
		return False


def validation_password(password):
	"""
	At least one upper, one lower, one digit and be 8 characters long
	"""
	valid_password = '^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{10,}$'
	try:
		if match(valid_password, password):
			return True
	except Exception,e:
		print 'Error occurred in Utilities validation_password: ', str(e)
		return False


def validation_name(name):
	"""
	Only letters and digits and be 6 characters long
	"""
	valid_name = '^[a-zA-Z\s]{6,}$'
	try:
		if match(valid_name, name):
			return True
		return False
	except Exception,e:
		print 'Error occurred in Utilities validation_name: ', str(e)
		return False


def validation_mail(mail):
	"""
	Only letters and digits and be 6 characters long
	"""
	valid_mail = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
	try:
		if match(valid_mail, mail):
			return True
		return False
	except Exception,e:
		print 'Error occurred in Utilities validation_mail: ', str(e)
		return False


class InputBox(TextInput):
	pass


class Logo(FloatLayout):
	pass


class Seperator(Widget):
	pass


class SubtleLabel(Label):
	pass


class ErrorLabel(Label):
	pass


class OpButton(Button):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['background_color'] = [0, 1, 0, 0.5]
		kwargs['size_hint'] = (0.5, 1)
		super(OpButton, self).__init__(**kwargs)


class BaseScreen(Screen):

	def create_popup(self, title, text):
		try:
			print text
			print title
			self.popup = Popup(title=title, content=Label(text=text), size_hint=(None, None), size=(400, 200))
			self.popup.open()
		except Exception as e:
			print 'Error occurred in BaseScreen create_popup: ', str(e)

	def logout(self):
		pass

	def back(self):
		pass

	def get_tag(self):
		pass