import sys
import os

PROJECT_PATH = os.getcwd() + '/..'
KIVY_PATH = os.getcwd() + '/Kivy'
PYTHON_PATH = '/Library/Python/2.7/site-packages'
sys.path.append(PROJECT_PATH)
sys.path.append(PYTHON_PATH)

from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.app import App

from RegisterScreen import RegisterScreen
from LoginScreen import LoginScreen
from Service import Service


class NetworkApp(App):

	def build(self, *args, **kwargs):
		Builder.load_file(KIVY_PATH + '/main.kv')
		screens = {
					'RegisterScreen': RegisterScreen(client=client, manager=sm, name='register'),
					'LoginScreen': LoginScreen(client=client, server=p2p_server, manager=sm, name='login')
					}
		for key in screens:
			sm.add_widget(screens[key])
		sm.current = 'login'
		return sm


if __name__ == '__main__':
	p2p_server = Service('server')
	p2p_server.start()
	client = Service('client')
	sm = ScreenManager()
	NetworkApp().run()
