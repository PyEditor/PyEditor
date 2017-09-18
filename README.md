# PyEditor

Python Editor for beginners and Minecraft Fans.

works only on Python 3 ;)


## quickstart

### Raspbian/Linux/MacOS:

```bash
~$ wget https://raw.githubusercontent.com/PyEditor/PyEditor/master/boot_PyEditor.sh
~$ chmod +x boot_PyEditor.sh
~$ ./boot_PyEditor.sh
~$ cd PyEditor_env
~/PyEditor_env$ source bin/activate
(PyEditor_env) ~/PyEditor_env$ pyeditor
```

### Windows:

* download [boot_PyEditor.cmd](https://github.com/PyEditor/PyEditor/raw/master/boot_PyEditor.cmd)
* store it somewhere
* Execute the batchfile
* The Executeable can then be found under: `...\PyEditor\Scripts\pyeditor.exe`


## TODO

* file name input field
* filelist
* unittests: Travis CI, tox
* gettext
* check if minecraft runs, before execute script (if mcpi module used)
* cleanup backups
* "desktop" integration
* installation? (e.g.: setup.exe for windows, debian package etc.)


## history

* v0.2.1 - 18.09.2017 - [[https://github.com/PyEditor/PyEditor/compare/v0.2.0...v0.2.1|compare v0.2.0...v0.2.1]]
  * [Bugfix idlelib imports for Python 3.6](https://github.com/PyEditor/PyEditor/pull/2)
* v0.2.0 - 07.05.2017 - [[https://github.com/PyEditor/PyEditor/compare/v0.1.0...v0.2.0|compare v0.1.0...v0.2.0]]
  * status output
  * load/save
* v0.1.0
  * display "run output" in GUI
* v0.0.1
  * first release created on "[PyDDF Python Spring Sprint 2017](http://www.pyddf.de/)"
  * Project started with [SpotlightKid/python-package-cookiecutter](https://github.com/SpotlightKid/python-package-cookiecutter)


## links

Project stuff:

* Project Homepage: https://github.com/PyEditor/PyEditor
* PyPi: https://pypi.python.org/pypi/PyEditor

other:

* https://www.raspberrypi.org/learning/getting-started-with-minecraft-pi/worksheet/
* Mcpi Lib: https://github.com/martinohanlon/mcpi
* http://minecraft-de.gamepedia.com/Pi_Edition
* http://pi.minecraft.net/
