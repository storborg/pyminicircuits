# Mini-Circuits Python Interfaces

This package provides interfaces to various Mini Circuits USB devices.

### Quick Start

Targeted to Python 3, works on Python 2 as well.

Install dependencies (Ubuntu):

    $ sudo apt install libudev-dev

Install the package:

    $ pip install pyminicircuits

Create a new udev rules file in ``/etc/udev/rules.d/85-minicircuits.rules``
with:

    ATTR{idVendor}=="20ce", MODE="660", GROUP="plugdev"

This will tell udev to allow members of the plugdev group to access all
Mini-Circuits USB devices.

Ensure that your user is a member of the plugdev group:

    $ sudo usermod -a -G plugdev <username>

Reload the udev rules:

    $ sudo udevadm control --reload-rules
    $ sudo udevadm trigger

Connect to a power sensor and start measuring power:

    $ minicircuits-powersensor

### API Example

Connect to an RUDAT attenuator and set values:

    from pyminicircuits import Attenuator

    a = Attenuator()
    print(a.get_serial())
    a.set_attenuation(32.5)
    print(a.get_attenuation())

#### License

Pyminicircuits is licensed under an MIT license. Please see the LICENSE file
for more information.
