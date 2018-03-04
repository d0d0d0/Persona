from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.bubble import Bubble
from kivy.uix.label import Label
from kivy.clock import Clock


BUTTON_NAMES = {'sshfs': 'File System Mount', 'camera': 'Camera', 'sendfile': 'Send File',
                'sensor': 'Sensor Information', 'gps': 'GPS', 'other': 'Other'}
PERM = {}


class FunctionalityList(GridLayout):

	def __init__(self, permissions, **kwargs):
		global PERM
		kwargs['cols'] = 3
		kwargs['col_default_width'] = 65
		kwargs['row_default_height'] = 65
		PERM = permissions
		# PERM = {u'sendfile': True, u'camera': True, u'sshfs': True, u'sensor': True, u'other': True, u'gps': True}

		super(FunctionalityList, self).__init__(**kwargs)

	def is_button_disabled(self, name):
		if PERM[name]:
			return False
		return True


class FuncListButton(Button):

	def __init__(self, **kwargs):
		kwargs['selected_color'] = [0, 0, 0, 0.3]
		kwargs['deselected_color'] = [0, 1, 0, 0.5]
		super(FuncListButton, self).__init__(**kwargs)

		Window.bind(mouse_pos=self.on_mouse_pos)

		self.tooltip = FunctionNameHover()

	def get_logo(self, name):
		if name is not '':
			if not PERM[name]:
				return '../static/disabled.png'
			return '../static/' + name + '.png'
		return '../static/disabled.png'

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
		try:
			if len(self.tooltip.content.children) == 0:
				self.tooltip.get_name(f_name=self.text)

			self.tooltip.x = self.x - 35
			self.tooltip.y -= self.height
			Window.add_widget(self.tooltip)
		except Exception as e:
			print 'Error occurred in display_tooltip: ', str(e)


class FunctionNameHover(Bubble):

	def __init__(self, **kwargs):
		kwargs['arrow_pos'] = 'top_mid'
		kwargs['orientation'] = 'vertical'
		kwargs['size_hint'] = (0.2, 0.1)
		super(FunctionNameHover, self).__init__(**kwargs)

	def get_name(self, f_name):
		try:
			func = Label(text='[b]' + (BUTTON_NAMES[f_name]) + '[/b]', font_size='14sp', markup=True)
			self.add_widget(func)
		except Exception as e:
			print 'Error occurred in get_name: ', str(e)