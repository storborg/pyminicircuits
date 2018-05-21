import sys
import argparse

from .. import Switch


def main(argv=sys.argv):
    p = argparse.ArgumentParser(
        description='Interact with Mini Circuits USB switches.')
    p.add_argument('--verbose', action='store_true')
    p.add_argument('value', type=int, nargs='?')
    opts = p.parse_args(argv[1:])

    sw = Switch()
    print("Part number: %s" % sw.get_part_number())
    print("Serial: %s" % sw.get_serial())
    if opts.value is not None:
        print("Setting switch port to: %d" % opts.value)
        sw.set_active_port(opts.value)
    else:
        print("Current switch port: %d" % sw.get_active_port())
