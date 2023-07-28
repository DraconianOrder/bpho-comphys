# task 1

from planets import *


# plot log graph of semi-major axis vs orbital period
def task1():
	x = np.array([planet.sm_axis for planet in planets])
	y = np.array([planet.period for planet in planets])

	plt.title("""Kepler's Third Law (log-log)
	T = ax^k → log(T) = k·log(x) + log(a) → k = Δlog(T)/Δlog(x)
	k ≈ 1.5""")
	plt.xlabel("Orbit semi-major axis (AU)")
	plt.ylabel("Orbital period (Julian years)")
	plt.xlim([0.2, 200])
	plt.ylim([0.2, 200])
	plt.axis("square")  # looks neater and easier to find gradient
	plt.loglog(x, y, marker="*", mec="b", mfc="b", c="k")  # "b"=blue, "k"=black
	for i in range(len(planets)):  # annotate all plotted points
		plt.annotate(planets[i].name, (x[i], y[i]), color="g")  # "g"=green
	plt.grid(True, which="both")  # grid lines
	plt.show()


	# plot scatter graph to show a^(3/2) ∝ T
	# where a is the semi-major axis and T is the orbital period
	x2 = np.array([planet.sm_axis ** (3 / 2) for planet in planets])
	y2 = np.array([planet.period for planet in planets])
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
	for i in range(len(planets)):  # annotate
		plt.annotate(planets[i].name, (x2[i], y2[i]), color="g")
	plt.grid(True)
	plt.show()
