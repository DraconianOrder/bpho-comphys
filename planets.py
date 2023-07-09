# planets

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# units: distance in au, time in years
class planet:
	def __init__(self, name, sm_axis, period, eccentricity, inclination):
		self.name = name
		self.sm_axis = sm_axis
		self.period = period
		self.eccentricity = eccentricity
		self.inclination = inclination

	def plot_orbit(self):
		theta = np.linspace(0, 2 * np.pi, 1000)
		a = self.sm_axis
		e = self.eccentricity
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
		plt.plot(r * np.cos(theta), r * np.sin(theta), label=self.name)

	def animate_orbit(self):
		frames = int(1000 * 50 / self.period)
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, 1000, frames + 1)
		theta = 2 * np.pi * time[0] / self.period
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
		x = r * np.cos(theta)
		y = r * np.sin(theta)
		fig, ax = plt.subplots()
		ax.scatter(0, 0, s=100, c="#FFE100", marker="x", label="Star")
		theta_temp = np.linspace(0, 2 * np.pi, 1000)
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta_temp))
		ax.plot(r * np.cos(theta_temp), r * np.sin(theta_temp))
		p = ax.scatter(x, y, c="b", s=5, label=self.name)
		ax.set(
			aspect="equal",
			xlabel="x / AU",
			ylabel="y / AU",
			xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2])
		ax.legend()

		def update(frame):
			ax.set(title=f"{self.name}: t={time[frame]:.3f} Julian years")
			theta = 2 * np.pi * time[frame] / self.period
			r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
			x = r * np.cos(theta)
			y = r * np.sin(theta)
			data = np.stack([x, y]).T
			p.set_offsets(data)
			return p

		# i = 1000 / (self.period * 100)  # convert to ms
		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=20)
		plt.grid(True)
		plt.show()


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

	# takes argument of which planet the years should be counted in
	# expects a planet object
	def animate_orbits(self, planet_y):  # 1 year = 1 second
		period = planet_y.period
		frames = 50 * 1000
		lim = period * 1000
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		ax.scatter(0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			a = planet.sm_axis
			e = planet.eccentricity
			theta = 2 * np.pi * time[0] / planet.period
			r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
			x = r * np.cos(theta)
			y = r * np.sin(theta)
			p = ax.scatter(x, y, s=5, label=planet.name)
			plots.append(p)
			ax.set(
				aspect="equal",
				xlabel="x / AU",
				ylabel="y / AU",
				xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2])
			ax.legend()

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity
				theta = 2 * np.pi * time[frame] / planet.period
				r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
				x = r * np.cos(theta)
				y = r * np.sin(theta)
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
			return tuple(plots)

		# tested optimal interval is 20 ms with 50k frames, where k is a constant
		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=20)
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

inner_planets = planetary_system("Inner planets", "Sun", inner)
outer_planets = planetary_system("Outer planets", "Sun", outer)
