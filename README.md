# Mini-Circuits Python Interfaces

This package provides interfaces to various Mini Circuits USB devices.

### Device Support

| Part            | Type                  | Status                          |
|-----------------|-----------------------|---------------------------------|
| RCM series      | mechanical switches   | Not supported yet               |
| ZTM series      | mechanical switches   | Not supported yet               |
| RC series       | mechanical switches   | Not supported yet               |
| USB series      | mechanical switches   | Not supported yet               |
| U2C-1SP2T-63VH  | solid-state switch    | Not supported yet               |
| U2C-1SP4T-63H   | solid-state switch    | Not supported yet               |
| USB-1SP16T-83H  | solid-state switch    | Not supported yet               |
| USB-1SP8T-63H   | solid-state switch    | Not supported yet               |
| USB-2SP2T-DCH   | solid-state switch    | Not supported yet               |
| USB-4SP2T-63H   | solid-state switch    | Not supported yet               |
| USB-SP4T-63     | solid-state switch    | Verified working :+1:           |
| PWR-2.4GHS-75   | power sensor          | Might work?                     |
| PWR-4GHS        | power sensor          | Might work?                     |
| PWR-4RMS        | power sensor          | Might work?                     |
| PWR-6GHS        | power sensor          | Verified working :+1:           |
| PWR-6LGHS       | power sensor          | Might work?                     |
| PWR-6LRMS-RC    | power sensor          | Might work?                     |
| PWR-6RMS-RC     | power sensor          | Might work?                     |
| PWR-8P-RC       | power sensor          | Might work?                     |
| PWR-8FS         | power sensor          | Might work?                     |
| PWR-8GHS        | power sensor          | Might work?                     |
| PWR-8GHS-RC     | power sensor          | Might work?                     |
| RC4DAT-6G-60    | 4-channel attenuator  | Not supported yet               |
| RC4DAT-6G-95    | 4-channel attenuator  | Not supported yet               |
| RCDAT-30G-30    | attenuator            | Might work via USB?             |
| RCDAT-3000-63W2 | attenuator            | Might work via USB?             |
| RCDAT-4000-120  | attenuator            | Verified working via USB :+1:   |
| RCDAT-6000-30   | attenuator            | Might work via USB?             |
| RCDAT-6000-60   | attenuator            | Might work via USB?             |
| RCDAT-6000-90   | attenuator            | Might work via USB?             |
| RCDAT-6000-110  | attenuator            | Verified working via USB :+1:   |
| RCDAT-8000-30   | attenuator            | Might work via USB?             |
| RCDAT-8000-60   | attenuator            | Might work via USB?             |
| RCDAT-8000-90   | attenuator            | Might work via USB?             |
| RUDAT-13G-90    | attenuator            | Might work?                     |
| RUDAT-13G-60    | attenuator            | Might work?                     |
| RUDAT-4000-120  | attenuator            | Might work?                     |
| RUDAT-6000-30   | attenuator            | Might work?                     |
| RUDAT-6000-60   | attenuator            | Verified working :+1:           |
| RUDAT-6000-90   | attenuator            | Might work?                     |
| RUDAT-6000-110  | attenuator            | Might work?                     |
| ZVVA-3000       | attenuator            | Might work?                     |
| UFC-6000        | frequency counter     | Not supported yet               |
| FCPM-6000RC     | frequency and power   | Not supported yet               |
| SSG-6000RC      | signal generator      | Not supported yet               |
| SSG-6001RC      | signal generator      | Not supported yet               |


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
