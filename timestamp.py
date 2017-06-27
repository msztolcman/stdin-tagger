#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals, division

import argparse
import os
import sys

import time

MAX_LINE_LENGTH = 1024
INPUT_LINE_SEPARATOR = os.linesep
OUTPUT_LINE_SEPARATOR = os.linesep
INPUT_ENCODING = 'utf-8'
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'

p = argparse.ArgumentParser()
p.add_argument('--max-line-length', '-m', type=str, default=MAX_LINE_LENGTH)
p.add_argument('--input-line-separator', '-l', type=str, default=INPUT_LINE_SEPARATOR)
p.add_argument('--input-encoding', '-i', type=str, default=INPUT_ENCODING)
p.add_argument('--timestamp-format', '-t', type=str, default=TIMESTAMP_FORMAT)
p.add_argument('--additional-tag', '-a', type=str, default=None)

args = p.parse_args()
if args.input_line_separator == r'\r':
    args.input_line_separator = '\r'
elif args.input_line_separator == r'\n':
    args.input_line_separator = '\n'
elif args.input_line_separator == r'\r\n':
    args.input_line_separator = '\r\n'

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
            sys.stdout.write('%s%s %s' % (
                time.strftime(args.timestamp_format),
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
