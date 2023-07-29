# bpho-comphys
### BPhO Computational Challenge: 2023 Solar System Orbits

Competition website: https://www.bpho.org.uk/bpho/computational-challenge/


## Summary
A Python module and Kivy app addressing all tasks. Running `app.py` will launch the Kivy app for an accessible graphical user interface, while custom Python projects can make extensive use of the `planets` module (examples of usage are provided in the main folder).

Samples of images/animations generated with the `planets` module are provided in the images folder, sorted by task.


## Usage
There are two main ways to use this module:
  1. Run `app.py` with Python in the main folder
  2. Use it in Python code using `import planets` or `from planets import *` in the main folder


### App
The first option launches an app with a graphical user interface.

On Windows:

![Orbits app on Windows](https://github.com/DraconianOrder/bpho-comphys/assets/139047098/d37edae4-8b15-4fdc-acde-189ffff23f38)

On mobile:

![Orbits app on Android](https://github.com/DraconianOrder/bpho-comphys/assets/139047098/1be8b4d4-7ee6-4e68-9960-5aae91253d8f)

- The sidebar provides task selection e.g. to view a 3D animation of the inner planets, one would select 4 on the sidebar.
- The "<" or ">" button toggles the sidebar, useful for smaller screens
- The "Presets" menu allows selection of pre-defined bodies i.e. the planets of the Solar System
- The "Custom" menu allows one to create their own custom planet
- The "Additional options" menu provides extra options regarding how graphs should be displayed
- The "View" menu allows one to generate and view their selected graph/animation.

### Python module
The second option provides even greater flexibility with the use of Python OOP (object-oriented programming).
The `planets` module contains the following classes:
- `Planet`
- `PlanetarySystem`
- `Star`

`Planet` and `PlanetarySystem` objects can be used to complete all base tasks and more, as they make customisation simple. Presets are already defined in the `planets` module, but one can easily create new `Planet` and `PlanetarySystem` objects with custom parameters for experimentation.

Examples of usage are in the main folder, from `task1.py` to `task7.py`, each serving as a sample of the task solutions.

#### Saving files
Many methods in the `Planet` and `PlanetarySystem` classes allow for saving the generated animation as a file of a given extension. For example, `planets.PlanetarySystem.animate_orbits` provides the option for `f_ext` and `fname`:

  `def animate_orbits(self, planet_y, yrs=1, fc="#333333", f_ext="", fname=""):`

- `f_ext` allows you to provide a file extension e.g. "gif", "mp4"
- `fname` allows you to provide a custom file name e.g. "Inner Planets orbit animation"

Not providing a value for `f_ext` means the animation will be shown using matplotlib. Providing a value for `f_ext` determines the file type of the saved file. Not providing a value for `fname` means the file name will default to something based on the planet/planetary system name and inside the images folder under the appropriate task. As such, one can change `fname` for a custom name and location.

##### Example usage
```
from planets import *
my_inner_planets = PlanetarySystem("My Inner Planets", sun, [mercury, venus, earth, mars])
my_inner_planets.animate_orbits(earth, 10, "#FFF8E7", "gif", "/Saved Images/My Inner Planets/animation")
```
The above code will save an animation of the four inner planets orbiting the Sun as /Saved Images/My Inner Planets/animation.gif.

## Software
The app uses the Python framework Kivy to build the GUI, meaning it can be ported to Android and iOS. The `planets` module uses `matplotlib` and `numpy` for graphing and calculations respectively. FFmpeg is recommended if one wants to save video files, otherwise, Python Pillow is adequate for saving .gif files.
