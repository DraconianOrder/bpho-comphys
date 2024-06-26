# kivy app (orbits)
# uses planets module and orbits.kv

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.accordion import Accordion
from random import choice

import planets


# button to toggle collapse sidebar
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


# button to submit options
class SubmitBtn(Button):
	def __init__(self, **kwargs):
		super(SubmitBtn, self).__init__(**kwargs)
		self.height = 14
		self.size_hint_x = 0.4
		self.pos_hint = {"center_x": 0.5}
		self.text = "Submit"


# button to generate graphic
class GenerateBtn(Button):
	def __init__(self, **kwargs):
		super(GenerateBtn, self).__init__(**kwargs)
		self.height = 20
		self.size_hint_y = 0.1
		self.text = "Generate graphic"


# layout holding a label and checkbox for selecting true/false options
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


# menu with checkoptions for pre-defined bodies i.e. solar system planets
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

		self.size_hint_min_y = len(self.children) * 40


# layout with label and textinput to allow numbers and names to be inputted
class CustomInput(GridLayout):
	selected = ""

	def check(self, _, value, *args):
		self.selected = value
		return self.selected

	def __init__(self, name, ht, f=None, **kwargs):
		super(CustomInput, self).__init__(**kwargs)
		self.nm = str(name)
		self.cols = 2
		self.height = 26
		self.minimum_height = 14
		self.add_widget(Label(text=name))
		self.txin = TextInput(multiline=False, hint_text=ht, input_filter=f)
		self.txin.bind(text=self.check)
		self.add_widget(self.txin)


# group of custominputs that define a custom planet
# takes in name, semi-major axis, orbital period, eccentricity, inclination
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


# menu that allows users to "create" a custom planet/satellite
# allows for comparing orbits of solar system dwarf planets or exoplanets
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
		self.size_hint_min_y = len(self.children) * 28 * 7 + self.submit_btn.height

	def __init__(self, **kwargs):
		super(CustomMenu, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.padding = 20

		self.submit_btn = SubmitBtn(size_hint_y=0.4)
		self.add_widget(self.submit_btn)
		self.submit_btn.bind(on_press=self.submit)
		self.submit(None)

		self.size_hint_min_y = len(self.children) * 28 * 7


# menu with additional options, mainly regarding how the graphic is displayed
class AddMenu(BoxLayout):
	select = {}

	def submit(self, _, **kwargs):
		self.select = {}
		for child in self.children[::-1]:
			try:
				self.select[child.nm] = child.selected
			except Exception:
				pass
		return self.select

	def __init__(self, **kwargs):
		super(AddMenu, self).__init__(**kwargs)
		self.orientation = "vertical"
		self.spacing = 10
		self.padding = 20

		self.years = CustomInput("Years", "Number of orbits", "float")
		self.add_widget(self.years)
		self.planet_y = CustomInput("Year planet", "1 orbit = 1 second")
		self.add_widget(self.planet_y)
		self.planet_c = CustomInput("Static planet", "Dedicated to Ptolemy ;)")
		self.add_widget(self.planet_c)
		self.facecolor = CustomInput("Background colour", "e.g. #FFF8E7")
		self.add_widget(self.facecolor)
		self.linewidth = CustomInput("Line width", "0 < lw <= 1", "float")
		self.add_widget(self.linewidth)
		self.no_ax_label = CheckOption("Hide axes labels")
		self.add_widget(self.no_ax_label)
		self.no_legend = CheckOption("Hide legend")
		self.add_widget(self.no_legend)
		self.legend_loc = CustomInput("Legend location", "e.g. 'upper right'")
		self.add_widget(self.legend_loc)
		self.three_d = CheckOption("3D? (#6, #7 only)")
		self.add_widget(self.three_d)

		self.submit_btn = SubmitBtn()
		self.add_widget(self.submit_btn)
		self.submit_btn.bind(on_press=self.submit)
		self.submit(None)

		self.size_hint_min_y = len(self.children) * 48


# contains generate button and graphic viewer
class Viewer(BoxLayout):
	options = []

	def generate(self, _, **kwargs):
		# selected task from sidebar
		# either a string e.g. "1" or None
		task = self.parent.parent.parent.parent.accordion.parent.sidebar.selected
		if task is None:
			return

		# options from presets
		presets = self.parent.parent.parent.parent.accordion.a1.presets_menu.select

		display = []
		for n in presets:
			if bool(presets[n]) is True:
				p = next((x for x in planets.pre if x.name == n), None)
				display.append(p)

		# options from custom
		custom = self.parent.parent.parent.parent.accordion.a2.custom_menu.select
		display += custom

		# additional options
		a = self.parent.parent.parent.parent.accordion.a3.add_menu.select
		addt = {
			"yrs": float(a["Years"]) if a["Years"] != "" else 1,
			"planet_y": str(a["Year planet"]),
			"planet_c": str(a["Static planet"]),
			"facecolor": str(a["Background colour"]),
			"lw": float(a["Line width"]) if a["Line width"] != "" else 1,
			"label": not(bool(a["Hide axes labels"])),
			"legend": not(bool(a["Hide legend"])),
			"legend_loc": str(a["Legend location"]),
			"3d": bool(a["3D? (#6, #7 only)"])
		}

		t = []
		x = []
		for n in display:
			if str(type(n)) == "<class 'planets.PlanetarySystem'>":
				t += n.planets
				x.append(n)
		for i in x:
			display.remove(i)

		d = display + t
		if presets["Sun"] is True:
			temp = planets.PlanetarySystem("Custom", d[0], d[1:])
		else:
			temp = planets.PlanetarySystem("Custom", None, d)

		planet_y = next(
			(x for x in d if x.name == addt["planet_y"]),
			temp.planets[-1]
		)
		planet_c = next(
			(x for x in d if x.name == addt["planet_c"]),
			choice(temp.planets)
		)
		yrs = addt["yrs"]  # take from additional
		fc = addt["facecolor"] if addt["facecolor"] != "" else "#000000"
		fn = "temp"

		# change what generate button does according to task selected on sidebar
		# if no task is selected it will do nothing
		if task == "1":
			f = temp.task1(fc, "mp4", fn)
		elif task == "2":
			f = temp.plot_orbits(fc, f_ext="mp4", fname=fn)
		elif task == "3":
			f = temp.animate_orbits(planet_y, yrs, fc, f_ext="mp4", fname=fn)
		elif task == "4":
			f = temp.animate_orbits_3d(planet_y, yrs, fc, f_ext="mp4", fname=fn)
		elif task == "5":
			if yrs <= 4:
				yrs = 5
			f = temp.task5(planet_y, yrs, fc, "mp4", fn)
		elif task == "6":
			# option for 2d/3d
			if addt["3d"] is True:
				f = temp.spirograph_3d(planet_y, yrs, fc, f_ext="mp4", fname=fn)
			else:
				f = temp.spirograph(planet_y, yrs, fc, f_ext="mp4", fname=fn)
		elif task == "7":
			# option for 2d/3d
			if addt["3d"] is True:
				f = temp.ptolemate_3d(planet_y, planet_c, yrs, fc, f_ext="mp4", fname=fn)
			else:
				f = temp.ptolemate(planet_y, planet_c, yrs, fc, f_ext="mp4", fname=fn)

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
		self.video = VideoPlayer()
		self.add_widget(self.video)


# accordion containing presets, custom, additional options + viewer
class Main(Accordion):
	a1 = ObjectProperty(None)
	a2 = ObjectProperty(None)
	a3 = ObjectProperty(None)
	a4 = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Main, self).__init__(**kwargs)


# sidebar with toggle buttons for task selection
class Sidebar(BoxLayout):
	selected = None

	def check(self, _, value, *args):
		temp = next(
			(x for x in ToggleButton.get_widgets("tasks") if x.state == "down"),
			None)
		self.selected = temp.text if temp else None

	def __init__(self, **kwargs):
		self.orientation = "vertical"
		self.size_hint = (0.25, 1)
		super(Sidebar, self).__init__(**kwargs)
		self.t1 = ToggleButton(text="1", group="tasks")
		self.t2 = ToggleButton(text="2", group="tasks")
		self.t3 = ToggleButton(text="3", group="tasks")
		self.t4 = ToggleButton(text="4", group="tasks")
		self.t5 = ToggleButton(text="5", group="tasks")
		self.t6 = ToggleButton(text="6", group="tasks")
		self.t7 = ToggleButton(text="7", group="tasks")
		a = [self.t1, self.t2, self.t3, self.t4, self.t5, self.t6, self.t7]
		for i in a:
			self.add_widget(i)
			i.bind(state=self.check)


# holds sidebar, collapse button and main accordion
class Frame(BoxLayout):
	sidebar = ObjectProperty(None)
	collapse_btn = ObjectProperty(None)
	placeholder = ObjectProperty(None)

	def toggle(self, b):
		b.toggle_sidebar()

	def __init__(self, **kwargs):
		super(Frame, self).__init__(**kwargs)
		self.sidebar = Sidebar()
		self.add_widget(self.sidebar)
		self.c_btn = CollapseBtn(
			size_hint=(0.06, 1), on_release=self.toggle, text="<")
		self.add_widget(self.c_btn)
		self.add_widget(Main())


class OrbitsApp(App):
	def build(self):
		return Frame()


if __name__ == "__main__":
	OrbitsApp().run()
