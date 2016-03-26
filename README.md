CVcreator is an automated CV generator from which uses YAML templates.
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

Installation
============

Custom Logo
-----------
To use a custom logo, just replace the local file `logo.pdf` with your own
user provided file.

Prerequisite
------------
```
sudo apt-get install latexmk
pip install pyyaml
```

Install
-------
Install by downloading and running:
```
python setup.py install
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
