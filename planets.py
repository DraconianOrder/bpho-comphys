# planets

import matplotlib.pyplot as plt
import numpy as np


# units: distance in au, time in years
class planet:
	def __init__(self, name, sm_axis, period, eccentricity, inclination):
		self.name = name
		self.sm_axis = sm_axis
		self.period = period
		self.eccentricity = eccentricity
		self.inclination = inclination

	def plot_orbit(self):
		t = np.linspace(0, 2 * np.pi, 1000)
		a = self.sm_axis
		e = self.eccentricity
		r = a * (1 - e ** 2) / (1 - e * np.cos(t))
		plt.plot(r * np.cos(t), r * np.sin(t), label=self.name)


class planetary_system:
	def __init__(self, name, star, planets):
		self.name = name
		self.star = star
		self.planets = planets

	def plot_orbits(self):
		plt.scatter(0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			planet.plot_orbit()
		plt.title(self.name)
		plt.xlabel("Major axis / AU")
		plt.ylabel("Minor axis / AU")
		plt.legend(loc="upper right")
		plt.axis("square")
		plt.grid(True)
		plt.show()


# define solar system planets using "solar system parameters"
# values from wikipedia
mercury = planet("Mercury", 0.387098, 0.240846, 0.205630, 7.005)
venus = planet("Venus", 0.723332, 0.615198, 0.006772, 3.39458)
earth = planet("Earth", 1, 1, 0.0167086, 0)
mars = planet("Mars", 1.52368055, 1.88085, 0.0934, 1.85)
jupiter = planet("Jupiter", 5.2038, 11.862, 0.0489, 1.303)
saturn = planet("Saturn", 9.5826, 29.4571, 0.0565, 2.485)
uranus = planet("Uranus", 19.19126, 84.0205, 0.04717, 0.773)
neptune = planet("Neptune", 30.07, 164.8, 0.008678, 1.77)
pluto = planet("Pluto", 39.482, 247.94, 0.2488, 17.16)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
inner = [mercury, venus, earth, mars]
outer = [jupiter, saturn, uranus, neptune, pluto]
