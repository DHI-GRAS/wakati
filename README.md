[![Build Status](https://travis-ci.org/DHI-GRAS/wakati.svg?branch=master)](https://travis-ci.org/DHI-GRAS/wakati)
[![codecov](https://codecov.io/gh/DHI-GRAS/wakati/branch/master/graph/badge.svg)](https://codecov.io/gh/DHI-GRAS/wakati)

# wakati
Painless timing in Python modules ⏰

Pure Python, no dependencies, minimal overhead.

## Installation

```bash
pip install wakati
```

That's it.

## Usage
`wakati` provides a context manager `Timer`:

```python
>>> import time

>>> import wakati
>>> import numpy as np

>>> with wakati.Timer('allocation'):
...    a = np.random.rand(100, 100)
'[allocation]: 0.12ms'

>>> with wakati.Timer('mean'):
...    b = a.mean()
'[mean]: 0.14ms'

>>> with wakati.Timer('sleep'):
...    time.sleep(2)
'[sleep]: 2.00s'
```

## Other Examples

### Compute statistics

```python
>>> import wakati
>>> import numpy as np

>>> timer = wakati.Timer('work', report=False)

>>> for _ in range(100):
...    with timer:
...        np.sum(np.random.rand(100, 100))

>>> print(np.mean(timer.elapsed))
0.00010946460518

>>> print(len(timer.elapsed))
100
```

### Logging

```python
>>> import logging

>>> import wakati
>>> import numpy as np

>>> with wakati.Timer('work', report_to=logging.warn):
...    np.sum(np.random.rand(100, 100))
'WARNING:root:[work]: 0.20ms'
```

### Custom messages

```python
>>> import time
>>> import wakati

>>> with wakati.Timer('main', message='This took {elapsed}'):
...    time.sleep(65)
'This took 1m 5s'
```

### More custom messages

```python
>>> import time
>>> import wakati

>>> timer = wakati.Timer('main', message='{greeting}! This took {elapsed}')
>>> timer.greeting = 'Hi there'
>>> with timer:
...    time.sleep(5)
'Hi there! This took 5.00s'
```

### Disable unit conversions

```python
>>> import time
>>> import wakati

>>> with wakati.Timer('main', message='{name} took {elapsed:.2e}s', auto_unit=False):
...    time.sleep(0.01)
'main took 1.05e-02s'
