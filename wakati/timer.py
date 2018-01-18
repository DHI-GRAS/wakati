#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import timeit

DEFAULT_REPORT_MESSAGE = '{name} took {elapsed:.2f}{unit}'
UNITS = {
    'm': 60,
    'h': 60 * 60,
    'days': 60 * 60 * 24
}
DECIMAL_UNITS = {
    's': 1,
    'ms': 1e-3,
    'μs': 1e-6,
    'ns': 1e-9
}


def _stdout(message):
    return sys.stdout.write(''.join([message, '\n']))


class Timer:
    def __init__(self, name, report=True, message=DEFAULT_REPORT_MESSAGE,
                 report_to=_stdout):
        self._start = []
        self._elapsed = []

        self.name = name
        self.report = report
        self.report_to = report_to
        self.message = message

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

    @property
    def unit(self):
        return None

    def print_report(self, elapsed):
        public_attributes = {key: val for key, val in vars(self).items() if not key.startswith('_')}
        public_attributes.update(
            elapsed=elapsed,
            unit=self._get_unit(elapsed)
        )
        message = self.message.format(**public_attributes)
        return self.report_to(message)

    @staticmethod
    def _get_unit(val):
        unit = []
        for threshold, unit in UNITS.items():
            pass
        return 's'
