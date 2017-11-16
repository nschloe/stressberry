# stressberry

Stress tests for the Raspberry Pi.

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/stressberry/master.svg)](https://circleci.com/gh/nschloe/stressberry/tree/master)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://img.shields.io/badge/awesome-yes-brightgreen.svg)
[![PyPi Version](https://img.shields.io/pypi/v/stressberry.svg)](https://pypi.python.org/pypi/stressberry)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/stressberry.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/stressberry)

### Installation

stressberry is [available from the Python Package Index](https://pypi.python.org/pypi/stressberry/),
so with
```
pip install -U stressberry
```
you can install/upgrade.

### Testing

To run the tests, just check out this repository and type
```
MPLBACKEND=Agg pytest
```

### Distribution

To create a new release

1. bump the `__version__` number,

2. publish to PyPi and GitHub:
    ```
    $ make publish
    ```

### License
stressberry is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
