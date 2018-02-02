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
    """Wakati: Easy timing in Python modules

    Arguments:
        name (str): Identifier of the Timer object.
        report (bool, optional): Print report after exiting context manager (default: True).
        message (str, optional): Message to print when reporting. Placeholders in `{}` are
            replaced by instance attributes via `str.format`.
        report_to (callable, optional): Reports are sent to this callable
            (default: `sys.stdout.write`).
        auto_unit (bool, optional): Automatically choose the most appropriate time unit when
            reporting (default: True).

    Example:
        >>> import wakati
        >>> import time
        >>> timer = wakati.Timer('test')
        >>> with timer:
        ...     time.sleep(2)
        '[test]: 2.00s'

    """
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

    def __repr__(self):
        return '<wakati.Timer (name: %s, num_times: %d)>' % (self.name, len(self.elapsed))

    @property
    def elapsed(self):
        """List of all recorded times in seconds"""
        return self._elapsed

    def print_report(self, elapsed):
        """Pretty-print a report for given time"""
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
