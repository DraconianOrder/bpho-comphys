# planets

# saving animations requires ffmpeg, otherwise animations can just be displayed

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


# returns true anomaly and heliocentric distance as a function of time
# solves kepler's equation using kepler's 1621 fixed-point iteration
def kepler_eq(time, sm_axis, period, eccentricity):
	n = 2 * np.pi / period  # mean motion
	M = n * time  # mean anomaly

	# kepler's equation: E = M + eccentricity * sin(E)
	e = eccentricity
	E = M
	for _ in range(10):  # 10 iterations balances accuracy with speed
		E = M + e * np.sin(E)  # eccentric anomaly

	# true anomaly theta
	theta = 2 * np.arctan(np.sqrt((1 + e) / (1 - e)) * np.tan(E / 2))
	a = sm_axis
	r = a * (1 - e * np.cos(E))  # heliocentric distance

	return theta, r


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
		r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
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
		r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
		x = r * np.cos(theta) * np.cos(np.deg2rad(self.inclination))
		y = r * np.sin(theta)
		z = r * np.cos(theta) * np.sin(np.deg2rad(self.inclination))
		if label is True:
			plt.plot(x, y, z, label=self.name)
		else:
			plt.plot(x, y, z)

	# animates scatter point according to kepler's laws
	def animate_orbit(self, f_ext=""):
		years = 5
		i = 20
		frames = int((1000 / i) * years)
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, self.period * years, frames + 1)

		theta, r = kepler_eq(time[0], a, self.period, e)

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
		ax.legend(loc="upper right")

		def update(frame):
			ax.set(title=f"{self.name}: t={time[frame]:.3f} Julian years")

			theta, r = kepler_eq(time[frame], a, self.period, e)

			x = r * np.cos(theta)
			y = r * np.sin(theta)
			data = np.stack([x, y]).T
			p.set_offsets(data)
			return p

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		if f_ext == "":
			plt.grid(True)
			plt.show()
		else:
			anim.save(f"../images/{self.name} Orbit.{f_ext}", writer="ffmpeg")

	# animates 3d orbit
	def animate_3d(self, f_ext=""):
		years = 5
		i = 20
		frames = int((1000 / i) * years)
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, self.period * years, frames + 1)

		theta, r = kepler_eq(time[0], a, self.period, e)

		x = r * np.cos(theta) * np.cos(np.deg2rad(self.inclination))
		y = r * np.sin(theta)
		z = r * np.cos(theta) * np.sin(np.deg2rad(self.inclination))
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		ax.scatter(0, 0, 0, s=100, c="#FFE100", marker="x", label="Star")
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
		ax.legend(loc="upper right")

		def update(frame):
			ax.set(title=f"{self.name}: t={time[frame]:.3f} Julian years")

			theta, r = kepler_eq(time[frame], a, self.period, e)

			x = r * np.cos(theta) * np.cos(np.deg2rad(self.inclination))
			y = r * np.sin(theta)
			z = r * np.cos(theta) * np.sin(np.deg2rad(self.inclination))
			data = np.stack([x, y]).T
			p.set_data(data)
			p.set_3d_properties(z)
			return p

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		if f_ext == "":
			plt.grid(True)
			plt.show()
		else:
			anim.save(f"../images/{self.name} Orbit 3D.{f_ext}", writer="ffmpeg")


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
	def animate_orbits(self, planet_y, f_ext=""):  # 1 year = 1 second
		period = planet_y.period
		years = self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		ax.scatter(0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			planet.plot_orbit(fig, ax)
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)

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
			ax.legend(loc="upper right")

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity

				theta, r = kepler_eq(time[frame], a, planet.period, e)

				x = r * np.cos(theta)
				y = r * np.sin(theta)
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
			return tuple(plots)

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		if f_ext == "":
			plt.grid(True)
			plt.show()
		else:
			anim.save(
				f"../images/{self.name} Orbits with {planet_y.name} Years.{f_ext}",
				writer="ffmpeg")

	def animate_orbits_3d(self, planet_y, f_ext=""):  # 1 year = 1 second
		period = planet_y.period
		years = self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		ax.scatter(0, 0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		for planet in self.planets:
			planet.plot_orbit_3d(fig, ax)
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)

			x = r * np.cos(theta) * np.cos(np.deg2rad(planet.inclination))
			y = r * np.sin(theta)
			z = r * np.cos(theta) * np.sin(np.deg2rad(planet.inclination))
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
			ax.legend(loc="upper right")

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity

				theta, r = kepler_eq(time[frame], a, planet.period, e)

				x = r * np.cos(theta) * np.cos(np.deg2rad(planet.inclination))
				y = r * np.sin(theta)
				z = r * np.cos(theta) * np.sin(np.deg2rad(planet.inclination))
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
				plots[c].set_3d_properties(z, "z")
			return tuple(plots)

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		if f_ext == "":
			plt.grid(True)
			plt.show()
		else:
			anim.save(
				f"../images/{self.name} Orbits 3D with {planet_y.name} Years.{f_ext}",
				writer="ffmpeg")

	def spirograph(self, planet_y, years=10, f_ext="", line=False):
		period = planet_y.period
		years = years * self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		ax.scatter(0, 0, s=100, c="#FFE100", marker="o", label=self.star)
		x_array = []
		y_array = []
		for planet in self.planets:
			if line is True:
				planet.plot_orbit(fig, ax)
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)

			x = r * np.cos(theta)
			y = r * np.sin(theta)
			x_array.append(x)
			y_array.append(y)
			p = ax.scatter(x, y, s=20, label=planet.name)
			plots.append(p)
			ax.set(
				aspect="equal",
				xlabel="x / AU",
				ylabel="y / AU",
				xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				facecolor="#333333")
			ax.legend(loc="upper right")

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			v = []
			w = []
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity

				theta, r = kepler_eq(time[frame], a, planet.period, e)

				x = r * np.cos(theta)
				y = r * np.sin(theta)
				v.append(x)
				w.append(y)
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
			for b in range(len(v)):
				for d in range(len(v)):
					ax.plot(
						[v[b], v[d]], [w[b], w[d]], "-w", lw="0.5", alpha=0.2)

			return tuple(plots)

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		if f_ext == "":
			plt.grid(True)
			plt.show()
		else:
			temp = ""
			for u in self.planets:
				temp += u.name + "-"
			temp = temp[:-1]
			n = planet_y.name
			anim.save(
				f"../images/{temp} Spirograph with {n} years.{f_ext}",
				writer="ffmpeg")


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
