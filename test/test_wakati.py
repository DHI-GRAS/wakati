#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import re

import wakati


def test_init():
    timer = wakati.Timer('test')
    assert isinstance(timer, wakati.Timer)


def test_repr():
    timer = wakati.Timer('test')
    for _ in range(100):
        with timer:
            pass
    assert repr(timer) == '<wakati.Timer (name: test, num_times: 100)>'


def test_base(capsys):
    timer = wakati.Timer('test')
    with timer:
        time.sleep(2)
    assert abs(timer.elapsed[0] - 2) < 1e-2
    captured = capsys.readouterr()
    assert captured.out == '[test]: 2.00s\n'


def test_base_2(capsys):
    with wakati.Timer('test'):
        time.sleep(2)
    captured = capsys.readouterr()
    assert captured.out == '[test]: 2.00s\n'


def test_base_long(capsys):
    timer = wakati.Timer('test')
    with timer:
        time.sleep(61.1)
    captured = capsys.readouterr()
    assert captured.out == '[test]: 1m 1s\n'


def test_base_short(capsys):
    timer = wakati.Timer('test')
    with timer:
        pass
    captured = capsys.readouterr()
    assert re.match(r'\[test\]: \d\.\d{2}[μn]s\n', captured.out)


def test_multiple(capsys):
    timer = wakati.Timer('test')
    with timer:
        time.sleep(1)
    with timer:
        time.sleep(1)
    assert abs(timer.elapsed[0] - 1) < 1e-2 and abs(timer.elapsed[1] - 1) < 1e-2
    captured = capsys.readouterr()
    assert captured.out == '[test]: 1.00s\n' * 2


def test_noreport(capsys):
    with wakati.Timer('test', report=False):
        pass
    captured = capsys.readouterr()
    assert not captured.out


def test_custom_message(capsys):
    with wakati.Timer('test', message='A test message. {elapsed:.0f}s{name}', auto_unit=False):
        time.sleep(2)
    captured = capsys.readouterr()
    assert captured.out == 'A test message. 2stest\n'


def test_custom_attributes(capsys):
    timer = wakati.Timer('test', message='{testattribute:.0e}')
    timer.testattribute = 100
    with timer:
        time.sleep(2)
    captured = capsys.readouterr()
    assert captured.out == '1e+02\n'


def test_setattr_forbidden():
    timer = wakati.Timer('test')
    try:
        timer.elapsed = 'test'
    except AttributeError as e:
        assert str(e) == 'can\'t set attribute'
    else:
        assert False
