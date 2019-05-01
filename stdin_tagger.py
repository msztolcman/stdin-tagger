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
    class UnknownTimeZoneError(Exception):
        pass


__version__ = '1.0.0'

MAX_LINE_LENGTH = 4096
INPUT_LINE_SEPARATOR = os.linesep
OUTPUT_LINE_SEPARATOR = os.linesep
INPUT_ENCODING = 'utf-8'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
TIMESTAMP_TIMEZONE = None


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
    if not name:
        return

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
    prog_version = "%%(prog)s %s" % __version__

    usage = 'Read standard input, decorate it with timestamp and optional tag, ' \
            'and print decorated line to standard output'

    # pylint: disable=invalid-name, bad-continuation
    p = argparse.ArgumentParser(usage=usage)
    p.add_argument('--max-line-length', '-m', type=str, default=MAX_LINE_LENGTH)
    p.add_argument('--input-line-separator', '-l', type=str, default=INPUT_LINE_SEPARATOR,
        help='Use INPUT_LINE_SEPARATOR as line separator')
    p.add_argument('--input-encoding', '-i', type=str, default=INPUT_ENCODING,
        help='Decode input from INPUT_ENCODING')
    p.add_argument('--timestamp-format', '-t', type=str, default=TIMESTAMP_FORMAT,
        help=
            'Specify format of timestamp. Please look at https://docs.python.org/3/library/datetime.html'
            '?highlight=time%%20strftime#strftime-and-strptime-behavior for available formats. '
            'Default is "%(default)s".'
    )
    p.add_argument('--timezone', '-z', type=str, default=TIMESTAMP_TIMEZONE,
        help=
            'Timezone used for timestamps. If pytz module is available, you can use timezones names. '
            'If not, please specify offset as an number of minutes or in format HH:MM. '
            'Default is local timezone.'
    )
    p.add_argument('--additional-tag', '-a', type=str, default=None,
        help='Additional tag between timestamp and input line. Default: empty')
    p.add_argument('--version', '-v', action='version', version=prog_version)

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
                sys.stdout.write('%s%s %s' % (
                    timestamp.strftime(args.timestamp_format),
                    '' if args.additional_tag is None else ' %s' % args.additional_tag,
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
