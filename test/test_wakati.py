import time

import wakati


def test_init():
    timer = wakati.Timer('test')
    assert isinstance(timer, wakati.Timer)


def test_base(capsys):
    timer = wakati.Timer('test')
    with timer:
        time.sleep(2)
    assert abs(timer.elapsed[0] - 2) < 1e-3
    captured = capsys.readouterr()
    assert captured.out == 'test took 2.00s\n'


def test_base2(capsys):
    with wakati.Timer('test'):
        time.sleep(2)
    captured = capsys.readouterr()
    assert captured.out == 'test took 2.00s\n'


def test_multiple(capsys):
    timer = wakati.Timer('test')
    with timer:
        time.sleep(1)
    with timer:
        time.sleep(1)
    assert abs(timer.elapsed[0] - 1) < 1e-3 and abs(timer.elapsed[1] - 1) < 1e-3
    captured = capsys.readouterr()
    assert captured.out == 'test took 1.00s\n' * 2


def test_noreport(capsys):
    with wakati.Timer('test', report=False):
        pass
    captured = capsys.readouterr()
    assert not captured.out


def test_custom_message(capsys):
    with wakati.Timer('test', message='A test message. {elapsed:.0f}{unit}{name}'):
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
        assert False
    except AttributeError as e:
        assert str(e) == 'can\'t set attribute'
    
