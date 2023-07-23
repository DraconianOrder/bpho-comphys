from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from kivy.uix.button import Button
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.videoplayer import VideoPlayer

import planets


class CollapseBtn(Button):
	def toggle_sidebar(self):
		if self.parent.sidebar.size_hint_x == 0.25:
			self.parent.sidebar.size_hint_x = None
			self.parent.sidebar.width = "0dp"
			self.parent.sidebar.opacity = 0
			self.text = ">"
		else:
			self.parent.sidebar.size_hint_x = 0.25
			self.parent.sidebar.opacity = 1
			self.text = "<"


class SubmitBtn(Button):
	def __init__(self, **kwargs):
		super(SubmitBtn, self).__init__(**kwargs)
		self.height = 20
		self.size_hint_x = 0.4
		self.size_hint_y = 0.4
		self.pos_hint = {"center_x": 0.5}
		self.text = "Submit"


class GenerateBtn(Button):
	def __init__(self, **kwargs):
		super(GenerateBtn, self).__init__(**kwargs)
		self.height = 20
		# self.size_hint_x = 0.2
		self.size_hint_y = 0.1
		self.text = "Generate graphic"


class CheckOption(GridLayout):
	selected = False

	def check(self, _, value, *args):
		self.selected = value
		# return value
		# if value:
		# 	print(f"checkbox {checkbox} is active")
		# else:
		# 	print(f"checkbox {checkbox} is inactive")

	def __init__(self, name, **kwargs):
		super(CheckOption, self).__init__(**kwargs)
		self.nm = str(name)
		self.cols = 2
		self.height = 12
		self.box = CheckBox()
		self.box.bind(active=self.check)
		self.add_widget(self.box)
		self.add_widget(Label(text=name))


class PresetsMenu(BoxLayout):
	select = {}

	def submit(self, _, **kwargs):
		for child in self.children[::-1]:
			try:
				self.select[child.nm] = child.selected
			except Exception:
				pass
			finally:
				pass
		# print(self.select)

	def __init__(self, **kwargs):
		super(PresetsMenu, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.padding = 20

		for i in planets.pre:
			self.add_widget(CheckOption(name=i.name))

		self.submit_btn = SubmitBtn()
		self.add_widget(self.submit_btn)
		self.submit_btn.bind(on_press=self.submit)
		self.submit(None)

		self.size_hint_min_y = len(self.children) * 22 + self.submit_btn.height


class CustomMenu(BoxLayout):
	select = {}

	def submit(self, _, **kwargs):
		for child in self.children[::-1]:
			try:
				self.select[child.nm] = child.selected
			except Exception:
				pass
			finally:
				pass
		# print(self.select)

	def __init__(self, **kwargs):
		super(PresetsMenu, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.padding = 20

		for i in planets.pre:
			self.add_widget(CheckOption(name=i.name))

		self.submit_btn = SubmitBtn()
		self.add_widget(self.submit_btn)
		self.submit_btn.bind(on_press=self.submit)
		self.submit(None)

		self.size_hint_min_y = len(self.children) * 22 + self.submit_btn.height


class Viewer(BoxLayout):
	options = []

	def generate(self, _, **kwargs):
		# options from presets
		presets = self.parent.parent.parent.parent.accordion.a1.presets_menu.select

		display = []
		for n in presets:
			if bool(presets[n]) is True:
				p = next((x for x in planets.pre if x.name == n), None)
				display.append(p)
		print(display)

		# options from custom
		custom = None
		# additional options
		additional = None

		self.options = [presets, custom, additional]
		print(self.options)

		t = []
		x = []
		for n in display:
			if str(type(n)) == "<class 'planets.PlanetarySystem'>":
				print(n.name)
				t += n.planets
				x.append(n)
		for i in x:
			display.remove(i)

		d = display + t
		print(display)
		print(d)
		if presets["Sun"] is True:
			temp = planets.PlanetarySystem("temp", d[0], d[1:])
		else:
			temp = planets.PlanetarySystem("temp", None, d)
		f = temp.animate_orbits(d[-1], f_ext="mp4")
		self.remove_widget(self.video)
		self.video = VideoPlayer(source=f, state="play", options={"eos": "loop"})
		self.add_widget(self.video)

	def __init__(self, **kwargs):
		super(Viewer, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.padding = 10

		self.gen_btn = GenerateBtn()
		self.add_widget(self.gen_btn)
		self.gen_btn.bind(on_press=self.generate)
		# self.add_widget(Label(text="Hello World"))
		self.video = VideoPlayer()
		self.add_widget(self.video)
		print(self.options)


class Main(Accordion):
	a1 = ObjectProperty(None)
	a2 = ObjectProperty(None)
	a3 = ObjectProperty(None)
	a4 = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Main, self).__init__(**kwargs)


class Frame(BoxLayout):
	sidebar = ObjectProperty(None)
	collapse_btn = ObjectProperty(None)
	placeholder = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Frame, self).__init__(**kwargs)


class OrbitsApp(App):
	def build(self):
		return Frame()


if __name__ == "__main__":
	OrbitsApp().run()
