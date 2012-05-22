#!/usr/bin/python2.7
#
# Script to dump raw serial data to a file
#
# Copyright 2012 Lee Verberne <lee@blarg.org>
"""Script to dump raw serial data to a file.  

Reads data from a serial device and writes it to a file or STDOUT if no file is
specified.  Continues until an interrupt (^C) is received."""

import argparse
import io
import select
import serial
import sys

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baud', metavar='RATE', type=int, default=9600,
                        help="Baud rate for serial port, default 9600")
    parser.add_argument('--output', metavar='FILE',
                        help="Write output to FILE, default STDOUT")
    parser.add_argument('--version', action='version', version='0.1')
    parser.add_argument('device', help="Serial Device")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.output:
        out = io.open(args.output, 'wb')
    else:
        out = sys.stdout

    ser = serial.Serial(args.device, args.baud, timeout=0)
    b = bytearray(64)
    try:
        n = True
        while n:
            select.select([ser],[],[ser])
            n = ser.readinto(b)
            if n:
                out.write(b[:n])
    except KeyboardInterrupt:
        pass
    else:
        print >>sys.stderr, "Received EOF on %s; shutting down" % args.device


if __name__ == '__main__':
    main()
