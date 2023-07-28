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


# task 5: uses kepler ii but using integrals instead of iteration
def kepler2(yrs, sm_axis, period, eccentricity, d, ta=0):
	time = np.linspace(0, yrs, d)
	a = sm_axis
	e = eccentricity
	n = np.floor(time[-1] / period)
	theta = np.linspace(ta, 2 * np.pi * n + ta, d)
	f = (1 - e * np.cos(theta)) ** -2
	c = [1] + [4 if x % 2 == 0 else 2 for x in range(len(theta) - 2)] + [1]
	t = period * (1 - e ** 2) ** (3 / 2) / (6 * np.pi) / d * np.cumsum(c * f)
	i = np.interp(t, theta, time)
	r = a * (1 - e ** 2) / (1 + e * np.cos(i))
	return i, theta, r


def task5(yrs, period, eccentricity, d=1000, ta=0):
	e = eccentricity
	time = np.linspace(0, yrs, d)
	n = np.ceil(time[-1] / period)
	theta = np.linspace(ta, 2 * np.pi * n + ta, d)
	f = (1 - e * np.cos(theta)) ** -2
	c = [1] + [4 if x % 2 == 0 else 2 for x in range(len(theta) - 2)] + [1]
	t = period * (1 - e ** 2) ** (3 / 2) / (6 * np.pi) / d * np.cumsum(c * f)
	return np.interp(t, theta, time)


def sort_p(planets):
	def k(e):
		return e.period
	t = planets
	t.sort(key=k)
	return t


class Star:
	def __init__(self, name, marker, color, size):
		self.name = name
		self.marker = marker
		self.color = color
		self.size = size


class Planet:
	def __init__(
		self,
		name="",  # preferably title case
		sm_axis=1,  # in astronomical units, AU
		period=1,  # in sidereal/julian years
		eccentricity=0,  # should be less than 1
		inclination=0,  # in degrees (convert to radians in calculations)
		true_anomaly=0  # in degrees (convert to radians in calculations)
	):
		self.name = name
		self.sm_axis = sm_axis
		self.period = period
		self.eccentricity = eccentricity
		self.inclination = inclination
		self.true_anomaly = true_anomaly

	# plots line graph of elliptical orbit
	def plot_orbit(self, label=False):
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

	# plots line graph of elliptical orbit
	def ptol_orbit(
		self,
		ax,
		offset=(0, 0),
		rt=False,
		yrs=1,
		sp=1000,
		label=False,
		lw=1,
		marker=None
	):
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, yrs, sp)
		theta, r = kepler_eq(time, a, self.period, e)
		# lim = yrs * 2 * np.pi
		# theta = np.linspace(0, lim, sp)
		# r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
		x = r * np.cos(theta) - offset[0]
		y = r * np.sin(theta) - offset[1]
		if rt is True:
			return (x, y)
		else:
			if label is True:
				ax.plot(x, y, lw=lw, marker=marker, label=self.name)
			else:
				ax.plot(x, y, lw=lw, marker=marker)

	def ptol_orbit_3d(
		self,
		ax,
		offset=(0, 0, 0),
		rt=False,
		yrs=1,
		sp=1000,
		label=False,
		lw=1,
		marker=None
	):
		a = self.sm_axis
		e = self.eccentricity
		time = np.linspace(0, yrs, sp)
		theta, r = kepler_eq(time, a, self.period, e)
		# r = a * (1 - e ** 2) / (1 + e * np.cos(theta))
		x = r * np.cos(theta) * np.cos(np.deg2rad(self.inclination)) - offset[0]
		y = r * np.sin(theta) - offset[1]
		z = r * np.cos(theta) * np.sin(np.deg2rad(self.inclination)) - offset[2]
		if rt is True:
			return (x, y, z)
		else:
			if label is True:
				ax.plot(x, y, z, lw=lw, marker=marker, label=self.name)
			else:
				ax.plot(x, y, z, lw=lw, marker=marker)

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
		self.plot_orbit()
		p = ax.scatter(x, y, c="b", s=20, label=self.name)
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
		elif f_ext == "html":
			with open(
				f"../images/Task 3/{self.name} Orbit.html",
				"w"
			) as f:
				print(anim.to_html5_video(), file=f)
		else:
			anim.save(
				f"../images/Task 3/{self.name} Orbit.{f_ext}",
				writer="ffmpeg")
		plt.close()

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
		elif f_ext == "html":
			with open(
				f"../images/Task 4/{self.name} Orbit 3D.html",
				"w"
			) as f:
				print(anim.to_html5_video(), file=f)
		else:
			anim.save(
				f"../images/Task 4/{self.name} Orbit 3D.{f_ext}",
				writer="ffmpeg")
		plt.close()


class PlanetarySystem:
	def __init__(self, name, star, planets):
		self.name = name
		self.star = star
		self.planets = sort_p([*set(planets)])

	# plot log graph of semi-major axis vs orbital period
	def task1(self, fc="#333333", f_ext="", fname=""):
		x = np.array([planet.sm_axis for planet in self.planets])
		y = np.array([planet.period for planet in self.planets])

		# plot scatter graph to show a^(3/2) ∝ T
		# where a is the semi-major axis and T is the orbital period
		x2 = np.array([planet.sm_axis ** (3 / 2) for planet in self.planets])
		y2 = np.array([planet.period for planet in self.planets])
		k_array = np.array([x2[i] / y2[i] for i in range(len(x2))])
		k = sum(k_array) / len(k_array)  # average k

		fig, ax = plt.subplots(figsize=(7, 7))

		def update(frame):
			plt.cla()
			if frame % 2 == 0:
				ax.set(
					title="""Kepler's Third Law (log-log)
T = ax^k → log(T) = k·log(x) + log(a) → k = Δlog(T)/Δlog(x)
k ≈ 1.5""",
					xlabel="Orbit semi-major axis (AU)",
					ylabel="Orbital period (Julian years)",
					xlim=[x[0] * 0.9, x[-1] * 1.1],
					ylim=[y[0] * 0.9, y[-1] * 1.1],
					aspect="equal",
					facecolor=fc)
				ax.loglog(x, y, marker="*", mec="b", mfc="b", c="k")
				for c, planet in enumerate(self.planets):
					ax.annotate(planet.name, (x[c], y[c]), color="g")
				plt.grid(True, which="both")
			else:
				ax.set(
					title=f"Kepler's Third Law (AU^(3/2) vs yr)\nk = a^(3/2) / T\n≈ {k}",
					xlabel="a^(3/2) (AU^(3/2))",
					ylabel="T (yr)",
					xlim=[x2[0] - (x2[-1] - x2[0]) * 0.1, x2[-1] * 1.1],
					ylim=[y2[0] - (y2[-1] - y2[0]) * 0.1, y2[-1] * 1.1],
					aspect="equal",
					facecolor=fc)
				ax.scatter(x2, y2, marker="*", c="b")
				a, b = np.polyfit(x2, y2, 1)  # line of best fit
				ax.plot(x2, a * x2 + b, c="k")
				for c, planet in enumerate(self.planets):
					ax.annotate(planet.name, (x2[c], y2[c]), color="g")
				plt.grid(True)

			return ax

		anim = FuncAnimation(fig=fig, func=update, frames=2, interval=2000)
		if fname == "":
			fname = f"../images/Task 1/{self.name}"

		if f_ext == "":
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	def task5(self, planet_y, yrs, fc="#333333", f_ext="", fname=""):
		years = planet_y.period * yrs
		d = int(np.ceil(years))
		fig, ax = plt.subplots()
		ax.set(
			title=self.name,
			xlabel="Time / Julian years",
			ylabel="Polar angle / radians",
			facecolor=fc
		)

		def update(frame):
			plots = []
			for planet in self.planets:
				for e in [0, planet.eccentricity]:
					period = planet.period
					time = np.linspace(0, years, d)
					n = np.ceil(time[-1] / period)
					theta = np.linspace(0, 2 * np.pi * n, d)
					f = (1 - e * np.cos(theta)) ** -2
					c = [1] + [4 if x % 2 == 0 else 2 for x in range(len(theta) - 2)] + [1]
					t = period * (1 - e ** 2) ** (3 / 2) / (6 * np.pi) / d * np.cumsum(c * f)
					label = f"{planet.name} Ecc={e:.2f}"
					plots.append(ax.plot(np.interp(t, theta, time), label=label))
			plt.legend(loc="upper right")
			return plots

		anim = FuncAnimation(fig=fig, func=update, frames=1, interval=1000)

		if fname == "":
			fname = f"../images/Task 5/{self.name}"

		if f_ext == "":
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	# plots line graphs of all planets in the system on one axis
	def plot_orbits(self, fc="#333333", f_ext="", fname=""):
		fig, ax = plt.subplots()
		if self.star is not None:
			ax.scatter(
				0,
				0,
				s=self.star.size,
				c=self.star.color,
				marker=self.star.marker,
				label=self.star.name)
		for planet in self.planets:
			planet.plot_orbit(label=True)
		ax.set(
			title=self.name,
			xlabel="Major axis / AU",
			ylabel="Minor axis / AU",
			aspect="equal",
			facecolor=fc)
		plt.legend(loc="upper right")
		plt.grid(True)

		def update(frame):
			return ax

		if fname == "":
			fname = f"../images/Task 2/{self.name}"

		if f_ext == "":
			plt.show()
		else:
			anim = FuncAnimation(fig=fig, func=update, frames=2, interval=1000)
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	# ptols orbits with planet_c as fixed object
	def ptol_orbits(self, ax, planet_c, yrs=1, main=False, fc="#000000"):
		yrs *= planet_c.period
		offset = planet_c.ptol_orbit(ax, rt=True, yrs=yrs)

		if main is True:
			for planet in self.planets:
				if planet != planet_c:
					planet.ptol_orbit(ax, offset=offset, yrs=yrs, lw=0.5, label=True)
				else:
					planet.ptol_orbit(ax, offset=offset, yrs=yrs, marker="o", label=True)
		else:
			for planet in self.planets:
				if planet != planet_c:
					planet.ptol_orbit(ax, offset=offset, yrs=yrs, lw=0.5)
				else:
					planet.ptol_orbit(ax, offset=offset, yrs=yrs, marker="o")

		# plot star
		if self.star is not None:
			ax.plot(
				-offset[0],
				-offset[1],
				color=self.star.color,
				label=self.star.name)

		if main is True:
			ax.set(
				title=f"{self.name} relative to {planet_c.name}: {yrs:.3f} years",
				xlabel="x / AU",
				ylabel="y / AU",
				aspect="equal",
				facecolor=fc
			)
			ax.legend(loc="upper right")
			plt.grid(True)
			plt.show()
			plt.close()

	# ptols 3d orbits with planet_c as fixed object
	def ptol_orbits_3d(self, ax, planet_c, yrs=1, main=False, fc="#000000"):
		yrs *= planet_c.period
		offset = planet_c.ptol_orbit_3d(ax, rt=True, yrs=yrs)

		if main is True:
			for planet in self.planets:
				if planet != planet_c:
					planet.ptol_orbit_3d(ax, offset=offset, yrs=yrs, lw=0.5, label=True)
				else:
					planet.ptol_orbit_3d(ax, offset=offset, yrs=yrs, marker="o", label=True)
		else:
			for planet in self.planets:
				if planet != planet_c:
					planet.ptol_orbit_3d(ax, offset=offset, yrs=yrs, lw=0.5)
				else:
					planet.ptol_orbit_3d(ax, offset=offset, yrs=yrs, marker="o")

		# plot star
		if self.star is not None:
			ax.plot(
				-offset[0],
				-offset[1],
				-offset[2],
				color=self.star.color,
				label=self.star.name)

		if main is True:
			ax.set(
				title=f"{self.name} relative to {planet_c.name}: {yrs:.3f} years",
				xlabel="x / AU",
				ylabel="y / AU",
				zlabel="z / AU",
				facecolor=fc
			)
			ax.legend(loc="upper right")
			plt.grid(True)
			plt.show()
			plt.close()

	# animates all orbits of planets in system
	# takes argument of which planet the years should be counted in
	# expects a planet object
	def animate_orbits(self, planet_y, yrs=1, fc="#333333", f_ext="", fname=""):
		period = planet_y.period
		years = yrs * self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		if self.star is not None:
			ax.scatter(
				0,
				0,
				s=self.star.size,
				c=self.star.color,
				marker=self.star.marker,
				label=self.star.name)
		for planet in self.planets:
			planet.plot_orbit()
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)

			x = r * np.cos(theta)
			y = r * np.sin(theta)
			p = ax.scatter(x, y, s=20, label=planet.name)
			plots.append(p)
			ax.set(
				aspect="equal",
				xlabel="x / AU",
				ylabel="y / AU",
				xlim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				ylim=[-a * (e + 1) * 1.2, a * (e + 1) * 1.2],
				facecolor=fc)
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
		n = planet_y.name
		w = ""
		if yrs != 1:
			w = f"{yrs * self.planets[-1].period / period:.0f} "

		if fname == "":
			fname = f"../images/Task 3/{self.name} Orbits with {w}{n} Years"

		if f_ext == "":
			plt.grid(True)
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	def ptolemate(self, planet_y, planet_c, yrs=1, fc="#333333", f_ext="", fname=""):
		period = planet_y.period
		# years = yrs * period
		i = 20
		frames = int((1000 / i) * yrs)
		lim = period * yrs
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		self.ptol_orbits(ax, planet_c, lim / planet_c.period)

		for planet in self.planets:
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)
			offset = planet_c.ptol_orbit(ax, yrs=lim, sp=frames + 1, rt=True)
			x = r * np.cos(theta) - offset[0][0]
			y = r * np.sin(theta) - offset[1][0]
			p = ax.scatter(x, y, s=20, label=planet.name)
			plots.append(p)
			ax.set(
				aspect="equal",
				xlabel="x / AU",
				ylabel="y / AU",
				facecolor=fc)
			ax.legend(loc="upper right")

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			offset = planet_c.ptol_orbit(ax, yrs=lim, sp=frames + 1, rt=True)
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity

				theta, r = kepler_eq(time[frame], a, planet.period, e)

				x = r * np.cos(theta) - offset[0][frame]
				y = r * np.sin(theta) - offset[1][frame]
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
			return tuple(plots)

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		n = planet_y.name
		w = ""
		if yrs != 1:
			w = f"{yrs:.0f} "

		if fname == "":
			fname = f"../images/Task 7/{self.name} relative to {planet_c.name} {w}{n} years"

		if f_ext == "":
			plt.grid(True)
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	def animate_orbits_3d(self, planet_y, yrs=1, fc="#333333", f_ext="", fname=""):
		period = planet_y.period
		years = yrs * self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		if self.star is not None:
			ax.scatter(
				0,
				0,
				0,
				s=self.star.size,
				c=self.star.color,
				marker=self.star.marker,
				label=self.star.name)
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
				facecolor=fc)
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
		n = planet_y.name
		w = ""
		if yrs != 1:
			w = f"{yrs * self.planets[-1].period / period:.0f} "

		if fname == "":
			fname = f"../images/Task 4/{self.name} Orbits 3D with {w}{n} Years"

		if f_ext == "":
			plt.grid(True)
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	def ptolemate_3d(self, planet_y, planet_c, yrs=1, fc="#333333", f_ext="", fname=""):
		period = planet_y.period
		# years = yrs * period
		i = 20
		frames = int((1000 / i) * yrs)
		lim = period * yrs
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig = plt.figure()
		ax = fig.add_subplot(111, projection="3d")
		self.ptol_orbits_3d(ax, planet_c, lim / planet_c.period)

		for planet in self.planets:
			a = planet.sm_axis
			e = planet.eccentricity

			theta, r = kepler_eq(time[0], a, planet.period, e)
			offset = planet_c.ptol_orbit_3d(ax, yrs=lim, sp=frames + 1, rt=True)
			x = r * np.cos(theta) * np.cos(np.deg2rad(planet.inclination)) - offset[0][0]
			y = r * np.sin(theta) - offset[1][0]
			z = r * np.cos(theta) * np.sin(np.deg2rad(planet.inclination)) - offset[2][0]
			p = ax.scatter(x, y, z, label=planet.name)
			plots.append(p)
			ax.set(
				xlabel="x / AU",
				ylabel="y / AU",
				zlabel="z / AU",
				facecolor=fc)
			ax.legend(loc="upper right")

		def update(frame):
			ax.set(
				title=f"{self.name}: t={time[frame] / period:.3f} {planet_y.name} years")
			offset = planet_c.ptol_orbit_3d(ax, yrs=lim, sp=frames + 1, rt=True)
			for c, planet in enumerate(self.planets):
				a = planet.sm_axis
				e = planet.eccentricity

				theta, r = kepler_eq(time[frame], a, planet.period, e)

				x = r * np.cos(theta) * np.cos(np.deg2rad(planet.inclination)) - offset[0][frame]
				y = r * np.sin(theta) - offset[1][frame]
				z = r * np.cos(theta) * np.sin(np.deg2rad(planet.inclination)) - offset[2][frame]
				data = np.stack([x, y]).T
				plots[c].set_offsets(data)
				plots[c].set_3d_properties(z, "z")
			return tuple(plots)

		anim = FuncAnimation(fig=fig, func=update, frames=frames, interval=i)
		n = planet_y.name
		w = ""
		if yrs != 1:
			w = f"{yrs:.0f} "

		if fname == "":
			fname = f"../images/Task 7/{self.name} relative to {planet_c.name} with {w}{n} Years 3D"

		if f_ext == "":
			plt.grid(True)
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()

	def spirograph(self, planet_y, yrs=10, fc="#000000", f_ext="", line=False, fname=""):
		period = planet_y.period
		years = yrs * self.planets[-1].period / period
		i = 20
		frames = int((1000 / i) * years)
		lim = period * years
		time = np.linspace(0, lim, frames + 1)
		plots = []
		fig, ax = plt.subplots()
		if self.star is not None:
			ax.scatter(
				0,
				0,
				s=self.star.size,
				c=self.star.color,
				marker=self.star.marker,
				label=self.star.name)
		x_array = []
		y_array = []
		for planet in self.planets:
			if line is True:
				planet.plot_orbit()
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
				facecolor=fc)
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
		temp = ""
		for u in self.planets:
			temp += u.name + "-"
		temp = temp[:-1]
		n = planet_y.name
		w = ""
		if yrs != 1:
			w = f"{yrs * self.planets[-1].period / period:.0f} "
		v = ""
		if line is True:
			v = " and line"

		if fname == "":
			fname = f"../images/Task 6/{temp} Spirograph with {w}{n} years{v}"

		if f_ext == "":
			plt.show()
		elif f_ext == "html":
			with open(f"{fname}.html", "w") as f:
				print(anim.to_html5_video(), file=f)
		else:
			fn = f"{fname}.{f_ext}"
			anim.save(fn, writer="ffmpeg")
			plt.close()
			return fn
		plt.close()


# define solar system planets using "solar system parameters"
# values from NASA's Horizons System
# https://ssd.jpl.nasa.gov/horizons/app.html#/
# at A.D. 2023-Aug-14 00:00:00.0000
mercury = Planet(
	name="Mercury",
	sm_axis=0.3870978295665558,
	period=0.2410108701802479,
	eccentricity=2.056354954960132E-01,
	inclination=7.003585469292125E+00,
	true_anomaly=1.889230396629393E+02)
venus = Planet(
	name="Venus",
	sm_axis=0.72333967899011,
	period=0.615628142197116,
	eccentricity=6.753028854282829E-03,
	inclination=3.394360369950776E+00,
	true_anomaly=1.894673808209864E+02)
earth = Planet(
	name="Earth",
	sm_axis=1.00073819677731,
	period=1.001810605554546,
	eccentricity=1.604364152762242E-02,
	inclination=3.099622567228552E-03,
	true_anomaly=2.186556906492948E+02)
mars = Planet(
	name="Mars",
	sm_axis=1.52369722627954,
	period=1.882146861200281,
	eccentricity=9.334737917768475E-02,
	inclination=1.847923133607658E+00,
	true_anomaly=2.131590190014785E+02)
jupiter = Planet(
	name="Jupiter",
	sm_axis=5.202378290208416,
	period=11.86864846590255,
	eccentricity=4.833431537183881E-02,
	inclination=1.303626614600446E+00,
	true_anomaly=1.886747335398515E+01)
saturn = Planet(
	name="Saturn",
	sm_axis=9.57511052966961,
	period=29.64552878472513,
	eccentricity=5.409745026803753E-02,
	inclination=2.488383924364373E+00,
	true_anomaly=2.442738264723067E+02)
uranus = Planet(
	name="Uranus",
	sm_axis=19.2960286599553,
	period=84.8199448379608,
	eccentricity=4.411720227915315E-02,
	inclination=7.721283154484431E-01,
	true_anomaly=2.441986196273190E+02)
neptune = Planet(
	name="Neptune",
	sm_axis=30.27978943893903,
	period=166.7338026736612,
	eccentricity=1.450793663505559E-02,
	inclination=1.768991920111643E+00,
	true_anomaly=3.275592247377758E+02)
pluto = Planet(
	name="Pluto",
	sm_axis=39.11030891229124,
	period=244.7611191723939,
	eccentricity=2.442251246317582E-01,
	inclination=1.710818788574056E+01,
	true_anomaly=7.675388171731849E+01)

sun = Star("Sun", "o", "#FFE100", 100)

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
inner = [mercury, venus, earth, mars]
outer = [jupiter, saturn, uranus, neptune, pluto]
full = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto]

inner_planets = PlanetarySystem("Inner Planets", sun, inner)
outer_planets = PlanetarySystem("Outer Planets", sun, outer)
solar_system = PlanetarySystem("Solar System", sun, full)

pre = [
	sun,
	solar_system,
	inner_planets,
	outer_planets,
	mercury,
	venus,
	earth,
	mars,
	jupiter,
	saturn,
	uranus,
	neptune,
	pluto
]
