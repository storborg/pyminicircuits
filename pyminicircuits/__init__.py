import time
import hid
import platform


INSTALL_STEPS = """Failed to open device. You may need to follow these steps:

Install dependencies:

    $ sudo apt install libudev-dev
    $ pip install hidapi

Create a new file /etc/udev/rules.d/85-minicircuits.rules with:

    ATTR{idVendor}=="20ce", MODE="660", GROUP="plugdev"

This will tell udev to allow members of the plugdev group to access all
Mini-Circuits USB devices.

Ensure that your user is a member of the plugdev group:

    $ sudo usermod -a -G plugdev <username>

Reload the udev rules:

    $ sudo udevadm control --reload-rules
    $ sudo udevadm trigger
"""


class BaseInterface(object):
    DEFAULT_VID = 0x20ce

    def __init__(self, vid=None, pid=None, serial=None):
        vid = vid or self.DEFAULT_VID
        pid = pid or self.DEFAULT_PID
        self.h = hid.device()
        if serial is None:
            try:
                self.h.open(vid, pid)
            except OSError:
                print(INSTALL_STEPS)
                raise
        else:
            dev_list = hid.enumerate()
            found = False
            for dev in dev_list:
                if (dev['vendor_id'] == vid) and (dev['product_id'] == pid):
                    # Note: we have to do this dance where we try to open every
                    # device, since Mini-Circuits is inconsistent about
                    # returning HID-compliant serial numbers, so we have to use
                    # the actual Mini-Circuits API for it.
                    try:
                        self.h.open_path(dev['path'])
                    except OSError:
                        # Device already open, skipping.
                        pass
                    else:
                        if self.get_serial() == serial:
                            found = True
                            break
                        else:
                            self.h.close()
            if not found:
                raise ValueError("Serial number not found: %s" % serial)

        self.h.set_nonblocking(1)

    @classmethod
    def parse_response_string(cls, data):
        chars = []
        for b in data[1:]:
            if b == 0:
                break
            chars.append(chr(b))
        return ''.join(chars)

    def _cmd(self, *cmd):
        if len(cmd) > 64:
            raise ValueError('command data length is limited to 64')
        cmd = list(cmd) + (63-len(cmd))*[0]

        if platform.system().lower() == 'windows':
            self.h.write([0]+cmd[:-1])
        else:
            self.h.write(cmd)

        time.sleep(0.05)
        while True:
            d = self.h.read(64)
            if d:
                break
        if d[0] != cmd[0]:
            raise RuntimeError("Invalid response from device: %s" % d)
        return d


class PowerSensor(BaseInterface):
    """
    Class for interfacing with Mini-Circuits USB Power Sensors.

    Verified working:
        - PWR-6GHS
    """

    # Mini-Circuits PWR-6GHS USB Power Sensor
    DEFAULT_PID = 0x11

    # Not sure if any of these command codes are also shared.
    CMD_GET_MODEL_NAME = 104
    CMD_GET_SERIAL = 105
    CMD_SET_MEASUREMENT_MODE = 15
    CMD_READ_POWER = 102
    CMD_GET_TEMPERATURE = 103
    CMD_GET_FIRMWARE_VERSION = 99

    def get_model_name(self):
        d = self._cmd(self.CMD_GET_MODEL_NAME)
        return self.parse_response_string(d)

    def get_serial(self):
        d = self._cmd(self.CMD_GET_SERIAL)
        return self.parse_response_string(d)

    def set_measurement_mode(self, mode='low-noise'):
        mode_num = {
            'low-noise': 0,
            'fast-sampling': 1,
            'fastest-sampling': 2,
        }[mode]
        self._cmd(self.CMD_SET_MEASUREMENT_MODE, mode_num)

    def get_power(self, freq):
        if freq > 65.535e6:
            scale = 1e6
            units = 'M'
        else:
            scale = 1e3
            units = 'k'
        freq = int(round(freq / scale))
        freq1 = freq >> 8
        freq2 = freq - (freq1 << 8)
        d = self._cmd(self.CMD_READ_POWER, freq1, freq2, ord(units))
        s = ''.join(chr(c) for c in d[1:7])
        return float(s)

    def get_temperature(self):
        d = self._cmd(self.CMD_GET_TEMPERATURE)
        s = ''.join(chr(c) for c in d[1:7])
        return float(s)

    def get_firmware_version(self):
        d = self._cmd(self.CMD_GET_FIRMWARE_VERSION)
        return chr(d[5]) + chr(d[6])


class SwitchAttenuatorBase(BaseInterface):
    CMD_GET_PART_NUMBER = 40
    CMD_GET_SERIAL_NUMBER = 41

    def get_part_number(self):
        d = self._cmd(self.CMD_GET_PART_NUMBER)
        return self.parse_response_string(d)

    def get_serial(self):
        d = self._cmd(self.CMD_GET_SERIAL_NUMBER)
        return self.parse_response_string(d)


class Attenuator(SwitchAttenuatorBase):
    """
    Class for interfacing with Mini-Circuits USB attenuators.

    Verified working:
        - RCDAT-6000-110
        - RUDAT-6000-60
    """
    # Mini-Circuits RUDAT-6000-60
    DEFAULT_PID = 0x23

    CMD_GET_ATTENUATION = 18
    CMD_SET_ATTENUATION = 19

    def get_attenuation(self):
        d = self._cmd(self.CMD_GET_ATTENUATION)
        full_part = d[1]
        frac_part = float(d[2]) / 4.0
        return full_part + frac_part

    def set_attenuation(self, value):
        value1 = int(value)
        value2 = int((value - value1) * 4.0)
        self._cmd(self.CMD_SET_ATTENUATION, value1, value2)


class Switch(SwitchAttenuatorBase):
    """
    Class for interfacing with Mini-Circuits USB switches.

    Verified working:
        - USB-SP4T-63
    """
    # Mini-Circuits USB-SP4T-63
    DEFAULT_PID = 0x22

    CMD_GET_SWITCH_PORT = 15

    def set_active_port(self, port):
        """
        Set which port is connected to the COM port: 1-indexed.
        """
        if port not in (1, 2, 3, 4):
            raise ValueError("Invalid switch port: %s" % port)
        self._cmd(port)

    def get_active_port(self):
        """
        Return which port is connected to the COM port: 1-indexed.
        """
        d = self._cmd(self.CMD_GET_SWITCH_PORT)
        port = d[1]
        return port
