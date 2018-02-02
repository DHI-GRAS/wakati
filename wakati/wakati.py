#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import timeit

DEFAULT_REPORT_MESSAGE = '[{name}]: {elapsed}'
UNITS = {
    1: 's',
    60: 'm',
    60 * 60: 'h',
    60 * 60 * 24: 'days'
}
DECIMAL_UNITS = {
    1: 's',
    10**3: 'ms',
    10**6: 'μs',
    10**9: 'ns',
    10**12: 'fs'
}


def _stdout(message):
    return sys.stdout.write(''.join([message, '\n']))


class Timer(object):
    def __init__(self, name, report=True, message=DEFAULT_REPORT_MESSAGE,
                 report_to=_stdout, auto_unit=True):
        self._start = []
        self._elapsed = []

        self.name = name
        self.report = report
        self.report_to = report_to
        self.message = message
        self.auto_unit = auto_unit

    def __enter__(self):
        self._start.append(timeit.default_timer())

    def __exit__(self, *args):
        elapsed = timeit.default_timer() - self._start.pop()
        self._elapsed.append(elapsed)

        if self.report:
            self.print_report(elapsed)

    @property
    def elapsed(self):
        return self._elapsed

    def print_report(self, elapsed):
        if self.auto_unit:
            elapsed = self._pprint_timedelta(elapsed)

        attributes = vars(self)
        attributes['elapsed'] = elapsed
        message = self.message.format(**attributes)
        return self.report_to(message)

    @staticmethod
    def _pprint_timedelta(remainder):
        if remainder < 60:
            unit = 1
            while remainder < 0.1:
                remainder *= 1000
                unit *= 1000
            return '{value:.2f}{unit}'.format(value=remainder, unit=DECIMAL_UNITS[unit])

        pieces = []
        remainder = int(round(remainder))
        for factor in sorted(UNITS.keys(), reverse=True):
            if remainder < factor:
                continue
            unit_value, remainder = divmod(remainder, factor)
            pieces.append('{value:d}{unit}'.format(value=unit_value, unit=UNITS[factor]))
        return ' '.join(pieces)
