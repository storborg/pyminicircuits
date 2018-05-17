import time
import hid


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

    def __init__(self, vid=None, pid=None):
        vid = vid or self.DEFAULT_VID
        pid = pid or self.DEFAULT_PID
        self.h = hid.device()
        try:
            self.h.open(vid, pid)
        except OSError:
            print(INSTALL_STEPS)
            raise
        self.h.set_nonblocking(1)

    @classmethod
    def parse_response_string(cls, data):
        chars = []
        for b in data[1:]:
            if b == 0:
                break
            chars.append(chr(b))
        return ''.join(chars)

    def _cmd(self, *data):
        cmd = [0] * 64
        for index, data in enumerate(data):
            cmd[index] = data
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


class Attenuator(BaseInterface):
    """
    Class for interfacing with Mini-Circuits USB attenuators.

    Verified working:
        - RUDAT-6000-60
    """
    # Mini-Circuits RUDAT-6000-60
    DEFAULT_PID = 0x23

    CMD_GET_PART_NUMBER = 40
    CMD_GET_SERIAL_NUMBER = 41
    CMD_GET_ATTENUATION = 18
    CMD_SET_ATTENUATION = 19

    def get_part_number(self):
        d = self._cmd(self.CMD_GET_PART_NUMBER)
        return self.parse_response_string(d)

    def get_serial(self):
        d = self._cmd(self.CMD_GET_SERIAL_NUMBER)
        return self.parse_response_string(d)

    def get_attenuation(self):
        d = self._cmd(self.CMD_GET_ATTENUATION)
        full_part = d[1]
        frac_part = float(d[2]) / 4.0
        return full_part + frac_part

    def set_attenuation(self, value):
        value1 = int(value)
        value2 = int((value - value1) * 4.0)
        self._cmd(self.CMD_SET_ATTENUATION, value1, value2)
