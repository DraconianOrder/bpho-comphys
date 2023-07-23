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
from kivy.uix.textinput import TextInput

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
		self.height = 14
		self.size_hint_x = 0.4
		# self.size_hint_y = 0.7
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

	def __init__(self, name, **kwargs):
		super(CheckOption, self).__init__(**kwargs)
		self.nm = str(name)
		self.cols = 2
		self.height = 14
		self.add_widget(Label(text=name))
		self.box = CheckBox()
		self.box.bind(active=self.check)
		self.add_widget(self.box)


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

		self.size_hint_min_y = len(self.children) * 24


class CustomInput(GridLayout):
	selected = ""

	def check(self, _, value, *args):
		self.selected = value
		return self.selected

	def __init__(self, name, ht, f, **kwargs):
		super(CustomInput, self).__init__(**kwargs)
		self.nm = str(name)
		self.cols = 2
		self.height = 26
		self.minimum_height = 26
		self.add_widget(Label(text=name))
		self.txin = TextInput(multiline=False, hint_text=ht, input_filter=f)
		self.txin.bind(text=self.check)
		self.add_widget(self.txin)


class CustomPlanet(BoxLayout):
	pl_select = {}

	def pl_check(self, *args):
		self.planet = planets.Planet()
		try:
			self.planet.name = str(self.name.selected)
		except Exception:
			pass
		try:
			self.planet.sm_axis = float(self.sm_axis.selected)
		except Exception:
			pass
		try:
			self.planet.period = float(self.period.selected)
		except Exception:
			pass
		try:
			self.planet.eccentricity = float(self.eccentricity.selected)
		except Exception:
			pass
		try:
			self.planet.inclination = float(self.inclination.selected)
		except Exception:
			pass
		try:
			self.planet.true_anomaly = float(self.true_anomaly.selected)
		except Exception:
			pass
		# for child in self.children[::-1]:
		# 	try:
		# 		self.pl_select[child.nm] = child.selected
		# 	except Exception:
		# 		pass
		# return self.pl_select
		return self.planet

	def __init__(self, num, **kwargs):
		super(CustomPlanet, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.add_widget(Label(text=f"Custom Planet {num}"))
		self.name = CustomInput(
			name="Name", ht="Custom planet", f=None)
		self.sm_axis = CustomInput(
			name="Semi-major axis", ht="In AU", f="float")
		self.period = CustomInput(
			name="Orbital period", ht="In Earth years", f="float")
		self.eccentricity = CustomInput(
			name="Eccentricity", ht="0 < e < 1", f="float")
		self.inclination = CustomInput(
			name="Inclination", ht="Angle in deg", f="float")
		self.true_anomaly = CustomInput(
			name="Initial polar angle", ht="Angle in deg", f="float")
		attr = [
			self.name, self.sm_axis, self.period, self.eccentricity, self.inclination
		]
		for i in attr:
			self.add_widget(i)

		self.height = len(self.children) * 36
		self.size_hint_min_y = len(self.children) * 36


class CustomMenu(BoxLayout):
	select = []

	def submit(self, _, **kwargs):
		self.select = []
		for child in self.children[::-1]:
			try:
				self.select.append(child.pl_check())
			except Exception:
				pass
		self.add_widget(CustomPlanet(num=len(self.children)), len(self.children))
		self.size_hint_min_y = len(self.children) * 36 * 7 + self.submit_btn.height

	def __init__(self, **kwargs):
		super(CustomMenu, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.padding = 20

		# self.add_widget(CustomPlanet())

		self.submit_btn = SubmitBtn(size_hint_y=0.2)
		self.add_widget(self.submit_btn)
		self.submit_btn.bind(on_press=self.submit)
		self.submit(None)

		self.size_hint_min_y = len(self.children) * 36 * 7


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
		custom = self.parent.parent.parent.parent.accordion.a2.custom_menu.select
		print(custom)
		display += custom
		print(display)
		# breakpoint()

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
