import sys
import time
import argparse

from .. import PowerSensor


def main(argv=sys.argv):
    p = argparse.ArgumentParser(
        description='Interact with Mini Circuits USB power sensors.')

    p.add_argument('--verbose', action='store_true')
    p.add_argument('--mode', default='low-noise')
    p.add_argument('--freq', type=float, default=10e6)
    p.add_argument('--interval', type=float, default=0.5)
    opts = p.parse_args(argv[1:])

    sensor = PowerSensor()

    if opts.verbose:
        print("Model name: %s" % sensor.get_model_name())
        print("Serial: %s" % sensor.get_serial())
        print("Firmware version: %s" % sensor.get_firmware_version())
        print("Setting measurement mode...")

    sensor.set_measurement_mode(opts.mode)

    if opts.verbose:
        print("Target signal frequency: %s" % opts.freq)

    while True:
        temp = sensor.get_temperature()
        power = sensor.get_power(opts.freq)
        print("%s C / %s dBm" % (temp, power))
        time.sleep(opts.interval)
