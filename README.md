
CVcreator is an automated CV generator which uses YAML templates.
For example outputs, take a look into the `examples/` folder.

Usage
=====
Generate a simple `example.yaml` file:
```
$ cvcreate --yaml
```
Compile `example.yaml` to `example.pdf`:
```
$ cvcreate example.yaml
```

To select a template, use the `-t` option. If tab-completion is one, it allow
to list the templates available:
```
$ cvcreate example.yaml -t<tab>
banking   casual    classic   default   margin    oldstyle
```

For information about other options, see:
```
$ cvcreate --help
```

Custom Logo
-----------
To use a custom logo, just replace the local file `logo.pdf` with your own
user provided file.

Installation
============
For installation on Mac OS-X, see section below

Prerequisite
------------
System dependencies:
- Latex (on Ubuntu/Debian: `sudo apt-get install latexmk texlive-latex-extra`)
- Python

Python package dependencies:
- PyYAML

To use pipenv (to avoid installing the package on your system, but rather in a virtual environment), do:
```
python3 -m pip install pipenv
python3 -m pipenv shell
pipenv install
```

There is currently a bug in the install process of pyyaml in pip on OS X which
unables installation under pyenv. The solution is to install using the
following command:
```
CC=$(which python) pip install pyyaml
```
The problem and the solution is described here:
http://stackoverflow.com/questions/25970966/setup-pyyaml-with-pyenv-on-mac-os-x-file-not-found-python-exe

Alternatively use MacPorts.

Install
-------
Install by running:
```
pip install cvcreator
```

Argument completion
-------------------
The module optimally uses the `argcomplete` module to do auto-completion in
Bash. This requires that the module is installed and enabled.

Linux install:
```
sudo apt-get install python-argcomplete
sudo activate-global-python-argcomplete
```

If installed in Python3:
```
sudo apt-get install python3-argcomplete
sudo activate-global-python-argcomplete3
```

It is possible to install argcomplete using `pip`, but the activation script is
not. It should either be done from package manager or from source:
https://github.com/kislyuk/argcomplete

Tips for installation on Mac OS-X
---------------------------------
The prerequisites can be installed as described above OR using MacPorts

sudo port install latexmk py27-yaml

and then install cvcreator by

python setup.py install --user

(the --user is important not to interfere with the MacPorts installation tree)

It might be necessary to add '/Users/*username*/Library/Python/*python version*/bin/' to the path by replacing the username and python version with the appropriate values and putting the following line in your .profile_bash or .bash file:
export PATH=/Users/*username*/Library/Python/*python version*/bin/:$PATH
