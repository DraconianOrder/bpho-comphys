# task 1

import matplotlib.pyplot as plt
import numpy as np


# units: distance in au, time in years
class planet:
	def __init__(self, name, sm_axis, period):
		self.name = name
		self.period = period
		self.sm_axis = sm_axis


# define solar system planets using "solar system parameters"
# values from wikipedia
mercury = planet("Mercury", 0.387098, 0.240846)
venus = planet("Venus", 0.723332, 0.615198)
earth = planet("Earth", 1, 1)
mars = planet("Mars", 1.52368055, 1.88085)
jupiter = planet("Jupiter", 5.2038, 11.862)
saturn = planet("Saturn", 9.5826, 29.4571)
uranus = planet("Uranus", 19.19126, 84.0205)
neptune = planet("Neptune", 30.07, 164.8)

solar_system = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


# plot log graph of semi-major axis vs orbital period
x = np.array([planet.sm_axis for planet in solar_system])
y = np.array([planet.period for planet in solar_system])

plt.title("""Kepler's Third Law (log-log)
T = ax^k → log(T) = k·log(x) + log(a) → k = Δlog(T)/Δlog(x)
k ≈ 1.5""")
plt.xlabel("Orbit semi-major axis (AU)")
plt.ylabel("Orbital period (Julian years)")
plt.xlim([0.2, 200])
plt.ylim([0.2, 200])
plt.axis("square")  # looks neater and easier to find gradient
plt.loglog(x, y, marker="*", mec="b", mfc="b", c="k")  # "b"=blue, "k"=black
for i in range(len(solar_system)):  # annotate all plotted points
	plt.annotate(solar_system[i].name, (x[i], y[i]), color="g")  # "g"=green
plt.grid(True, which="both")  # grid lines
plt.show()


# plot scatter graph to show a^(3/2) ∝ T
# where a is the semi-major axis and T is the orbital period
x2 = np.array([planet.sm_axis ** (3 / 2) for planet in solar_system])
y2 = np.array([planet.period for planet in solar_system])
k_array = np.array([x2[i] / y2[i] for i in range(len(x2))])
k = sum(k_array) / len(k_array)  # average k

plt.title(f"Kepler's Third Law (AU^(3/2) vs yr)\nk = a^(3/2) / T\n≈ {k}")
plt.xlabel("a^(3/2) (AU^(3/2))")
plt.ylabel("T (yr)")
plt.xlim([-5, 175])
plt.ylim([-5, 175])
plt.axis("square")
plt.scatter(x2, y2, marker="*", c="b")  # scatter points
a, b = np.polyfit(x2, y2, 1)  # line of best fit
plt.plot(x2, a * x2 + b, c="k")
for i in range(len(solar_system)):  # annotate
	plt.annotate(solar_system[i].name, (x2[i], y2[i]), color="g")
plt.grid(True)
plt.show()
