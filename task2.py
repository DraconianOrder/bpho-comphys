# task 2

from planets import *


inner = planetary_system("Inner planets", "Sun", inner)
outer = planetary_system("Outer planets", "Sun", outer)

inner.plot_orbits()
outer.plot_orbits()
