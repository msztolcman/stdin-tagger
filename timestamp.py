#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, division

import argparse
import datetime
import os
import sys

try:
    import pytz
    UnknownTimeZoneError = pytz.exceptions.UnknownTimeZoneError
except ImportError:
    pytz = None
    class UnknownTimeZoneError(Exception): pass


MAX_LINE_LENGTH = 1024
INPUT_LINE_SEPARATOR = os.linesep
OUTPUT_LINE_SEPARATOR = os.linesep
INPUT_ENCODING = 'utf-8'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
TIMESTAMP_TIMEZONE = 'UTC'


class Timezone(datetime.tzinfo):
    def __init__(self, offset):
        self._offset = offset
        self._name = offset

    def utcoffset(self, dt):
        return self._offset

    def tzname(self, dt):
        return self._name

    def dst(self, dt):
        return datetime.timedelta(0)


def get_timezone(name):
    try:
        name = int(name)
        offset = datetime.timedelta(minutes=name)
        return Timezone(offset)
    except ValueError:
        pass

    if ':' in name:
        hours, minutes = name.split(':')
        if name.startswith('-'):
            hours = hours.lstrip('-')
            minus = -1
        else:
            minus = 1

        offset = datetime.timedelta(hours=int(hours) * minus, minutes=int(minutes) * minus)
        return Timezone(offset)

    if pytz:
        return pytz.timezone(name)

    if name.upper() == 'UTC':
        return Timezone(datetime.timedelta(0))

    raise UnknownTimeZoneError(name)


def parse_args(argv):
    p = argparse.ArgumentParser()
    p.add_argument('--max-line-length', '-m', type=str, default=MAX_LINE_LENGTH)
    p.add_argument('--input-line-separator', '-l', type=str, default=INPUT_LINE_SEPARATOR)
    p.add_argument('--input-encoding', '-i', type=str, default=INPUT_ENCODING)
    p.add_argument('--timestamp-format', '-t', type=str, default=TIMESTAMP_FORMAT)
    p.add_argument('--timezone', '-z', type=str, default=TIMESTAMP_TIMEZONE)

    args = p.parse_args(argv)
    if args.input_line_separator == r'\r':
        args.input_line_separator = '\r'
    elif args.input_line_separator == r'\n':
        args.input_line_separator = '\n'
    elif args.input_line_separator == r'\r\n':
        args.input_line_separator = '\r\n'

    try:
        args.timezone = get_timezone(args.timezone)
    except UnknownTimeZoneError:
        p.error('Invalid timezone: %s' % (args.timezone, ))

    return args


def main():
    args = parse_args(sys.argv[1:])
    is_new_line = True
    should_decode = None
    while True:
        try:
            line = sys.stdin.readline(args.max_line_length)
            if should_decode is None:
                should_decode = hasattr(line, 'decode')
            if should_decode:
                line = line.decode(args.input_encoding)
            if line == '':
                break

            if is_new_line:
                timestamp = datetime.datetime.now(args.timezone)
                sys.stdout.write('%s %s' % (
                    timestamp.strftime(args.timestamp_format),
                    line
                ))
            else:
                sys.stdout.write(line)

            is_new_line = line.endswith(args.input_line_separator)
            if is_new_line:
                sys.stdout.flush()

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
