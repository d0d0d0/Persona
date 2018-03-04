from Utilities import BaseScreen,ErrorLabel,validation_username,validation_password,validation_name,validation_mail
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup


class RegisterScreen(BaseScreen):

	def __init__(self, client, manager, **kwargs):
		self.client = client
		self.sm = manager
		super(RegisterScreen, self).__init__(**kwargs)

	def register(self, username, password, name, email):
		'''
		content = BoxLayout(orientation='vertical', padding=[50,10,10,10])
		is_error = 0
		if not validation_username(username):
			is_error += 1
			content.add_widget(ErrorLabel(text='[b]*[/b] User name must contain only letters and digits and be at least 8 characters long.'))
		if not validation_password(password):
			is_error += 1
			content.add_widget(ErrorLabel(text='[b]*[/b] Password must contain at least one upper, one lower, one digit and be 8 characters long.'))
		if not validation_name(name):
			is_error += 1
			content.add_widget(ErrorLabel(text='[b]*[/b] Name must contain only letters and spaces and be at least 6 characters long.'))
		if not validation_mail(email):
			is_error += 1
			content.add_widget(ErrorLabel(text='[b]*[/b] Invalid e-mail address.'))

		if is_error:
			error = RegisterPopup(title='Register Error', content=content, size_hint=(None, None), size=(600, 60 + is_error*50))
			error.open()
		'''
		if True:
		# else:
			result = self.client.register(username=username, password=password, name=name, email=email)
			if not result:
				self.sm.current = 'login'
			else:
				self.create_popup(title='Error', text='An error occurred.')

	def back(self):
		try:
			self.sm.current = 'login'
		except Exception,e:
			print 'Error occured in RegisterScreen back: ', str(e)

	def logout(self):
		try:
			pass
		except Exception,e:
			print 'Error occured in RegisterScreen back: ', str(e)

	def get_tag(self):
		try:
			return 'Register'
		except Exception,e:
			print 'Error occured in RegisterScreen back: ', str(e)

	def update_ip(self):
		try:
			pass
			print 'UPDATE_IP'
		except Exception,e:
			print 'Error occured in LoginScreen back: ', str(e)


class RegisterPopup(Popup):

	def __init__(self, **kwargs):
		super(RegisterPopup, self).__init__(**kwargs)