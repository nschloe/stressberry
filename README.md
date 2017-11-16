# stressberry

Stress tests for the Raspberry Pi.

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/stressberry/master.svg)](https://circleci.com/gh/nschloe/stressberry/tree/master)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg)](https://img.shields.io/badge/awesome-yes-brightgreen.svg)
[![PyPi Version](https://img.shields.io/pypi/v/stressberry.svg)](https://pypi.python.org/pypi/stressberry)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/stressberry.svg?style=social&label=Stars&maxAge=2592000)](https://github.com/nschloe/stressberry)

There are a million of ways to cool down your Raspberry Pi: Small heat sinks,
specific cases, and some [extreme DIY solutions](https://youtu.be/WfQMLInuwws).
stressberry is a package for testing the core temperature under different
loads, and it produces nice plots which can easily be compared.

To run stressberry on your computer, simply install it with
```
(sudo -H) pip3 install -U stressberry
```
and run it with
```
stressberry-run out.dat
```
The run stresses the CPU for five minutes, lets it cool down, and stresses
again with a higher load. The entire process takes about half and hour.

The resulting data file can be displayed with
```
stressberry-plot out.dat [out.png]
```
If you specify a PNG file, the image gets written to that.

### "Case" studies

#### The naked Raspberry Pi 3

<img src="https://nschloe.github.io/stressberry/naked-photo.jpg" width="30%">

<img src="https://nschloe.github.io/stressberry/naked-plot.png" width="50%">

The Raspberry Pi 3 without fans, heat sinks, or particular cases. The idle core
temperature is about 47°C, under heavy load it reaches 80°C (at which point the
CPU frequency is throttled).

### Installation

stressberry is [available from the Python Package Index](https://pypi.python.org/pypi/stressberry/),
so with
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
