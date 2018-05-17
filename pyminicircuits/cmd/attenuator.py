import sys
import argparse

from .. import Attenuator


def main(argv=sys.argv):
    p = argparse.ArgumentParser(
        description='Interact with Mini Circuits USB attenuators.')
    p.add_argument('--verbose', action='store_true')
    p.add_argument('value', type=float, nargs='?')
    opts = p.parse_args(argv[1:])

    atten = Attenuator()
    print("Part number: %s" % atten.get_part_number())
    print("Serial: %s" % atten.get_serial())
    if opts.value:
        print("Setting attenuation to: %f dB" % opts.value)
        atten.set_attenuation(opts.value)
    else:
        print("Current attenuation: %f dB" % atten.get_attenuation())
