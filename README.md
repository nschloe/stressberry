# stressberry

Stress tests for the Raspberry Pi.

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/stressberry/master.svg)](https://circleci.com/gh/nschloe/stressberry/tree/master)
[![codecov](https://codecov.io/gh/nschloe/stressberry/branch/master/graph/badge.svg)](https://codecov.io/gh/nschloe/stressberry)
[![PyPi Version](https://img.shields.io/pypi/v/stressberry.svg)](https://pypi.python.org/pypi/stressberry)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://img.shields.io/badge/awesome-yes-brightgreen.svg)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/stressberry.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/stressberry)


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
