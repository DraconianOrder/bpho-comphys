# planets

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


# units: distance in au, time in years
class planet:
	def __init__(self, name, sm_axis, period, eccentricity, inclination):
		self.name = name
		self.sm_axis = sm_axis
		self.period = period
		self.eccentricity = eccentricity
		self.inclination = inclination

	# plots line graph of elliptical orbit
	def plot_orbit(self, fig, ax, label=False):
		theta = np.linspace(0, 2 * np.pi, 1000)
		a = self.sm_axis
		e = self.eccentricity
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
		x = r * np.cos(theta)
		y = r * np.sin(theta)
		if label is True:
			plt.plot(x, y, label=self.name)
		else:
			plt.plot(x, y)

	# plots 3d line graph of elliptical orbit
	# ax must be 3d
	def plot_orbit_3d(self, fig, ax, label=False):
		theta = np.linspace(0, 2 * np.pi, 1000)
		a = self.sm_axis
		e = self.eccentricity
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
		x = r * np.cos(theta) * np.cos(self.inclination)
		y = r * np.sin(theta)
		z = r * np.cos(theta) * np.sin(self.inclination)
		if label is True:
			plt.plot(x, y, z, label=self.name)
		else:
			plt.plot(x, y, z)

	# animates scatter point according to kepler's laws
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
		self.plot_orbit(fig, ax)
		p = ax.scatter(x, y, c="b", s=10, label=self.name)
		ax.set(
			aspect="equal",
			xlabel="x / AU",
			ylabel="y / AU",
			xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			facecolor="#333333")
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

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=20)
		plt.grid(True)
		plt.show()

	# animates 3d orbit
	def animate_3d(self):
		frames = int(1000 * 50 / self.period)
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, 1000, frames + 1)
		theta = 2 * np.pi * time[0] / self.period
		r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
		x = r * np.cos(theta) * np.cos(self.inclination)
		y = r * np.sin(theta)
		z = r * np.cos(theta) * np.sin(self.inclination)
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		p = ax.plot(x, y, z, c="b", marker="o", label=self.name)[0]
		self.plot_orbit_3d(fig, ax)
		ax.set(
			xlabel="x / AU",
			ylabel="y / AU",
			zlabel="z / AU",
			xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			zlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
			facecolor="#333333")
		ax.legend()

		def update(frame):
			ax.set(title=f"{self.name}: t={time[frame]:.3f} Julian years")
			theta = 2 * np.pi * time[frame] / self.period
			r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
			x = r * np.cos(theta) * np.cos(self.inclination)
			y = r * np.sin(theta)
			z = r * np.cos(theta) * np.sin(self.inclination)
			data = np.stack([x, y]).T
			p.set_data(data)
			p.set_3d_properties(z)
			return p

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=20)
		plt.grid(True)
		plt.show()


class planetary_system:
	def __init__(self, name, star, planets):
		self.name = name
		self.star = star
		self.planets = planets

	# plots line graphs of all planets in the system on one axis
	def plot_orbits(self):
		fig, ax = plt.subplots()
		plt.scatter(0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			planet.plot_orbit(fig, ax, label=True)
		plt.title(self.name)
		plt.xlabel("Major axis / AU")
		plt.ylabel("Minor axis / AU")
		plt.legend(loc="upper right")
		plt.axis("square")
		plt.grid(True)
		plt.show()

	# animates all orbits of planets in system
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
			planet.plot_orbit(fig, ax)
			a = planet.sm_axis
			e = planet.eccentricity
			theta = 2 * np.pi * time[0] / planet.period
			r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
			x = r * np.cos(theta)
			y = r * np.sin(theta)
			p = ax.scatter(x, y, s=10, label=planet.name)
			plots.append(p)
			ax.set(
				aspect="equal",
				xlabel="x / AU",
				ylabel="y / AU",
				xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				facecolor="#333333")
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

	def animate_orbits_3d(self, planet_y):  # 1 year = 1 second
		period = planet_y.period
		frames = 50 * 1000
		lim = period * 1000
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		ax.scatter(0, 0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			planet.plot_orbit_3d(fig, ax)
			a = planet.sm_axis
			e = planet.eccentricity
			theta = 2 * np.pi * time[0] / planet.period
			r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
			x = r * np.cos(theta) * np.cos(planet.inclination)
			y = r * np.sin(theta)
			z = r * np.cos(theta) * np.sin(planet.inclination)
			p = ax.scatter(x, y, z, label=planet.name)
			plots.append(p)
			ax.set(
				xlabel="x / AU",
				ylabel="y / AU",
				zlabel="z / AU",
				xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				zlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				facecolor="#333333")
			ax.legend()

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity
				theta = 2 * np.pi * time[frame] / planet.period
				r = a * (1 - e ** 2) / (1 - e * np.cos(theta))
				x = r * np.cos(theta) * np.cos(planet.inclination)
				y = r * np.sin(theta)
				z = r * np.cos(theta) * np.sin(planet.inclination)
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
				plots[c].set_3d_properties(z, 'z')
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


# testing
# pluto.animate_3d()
