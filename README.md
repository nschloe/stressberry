<p align="center">
  <img alt="stressberry" src="https://nschloe.github.io/stressberry/stressberry.png" width="60%">

  [![CircleCI](https://img.shields.io/circleci/project/github/nschloe/stressberry/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/stressberry/tree/master)
  [![codecov](https://img.shields.io/codecov/c/github/nschloe/stressberry.svg?style=flat-square)](https://codecov.io/gh/nschloe/stressberry)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
  [![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg?style=flat-square)](https://github.com/nschloe/stressberry)
  [![PyPi Version](https://img.shields.io/pypi/v/stressberry.svg?style=flat-square)](https://pypi.org/project/stressberry)
  [![GitHub stars](https://img.shields.io/github/stars/nschloe/stressberry.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/stressberry)
</p>

Stress tests and temperature plots for the Raspberry Pi.

#### Raspberry Pi 4B
<img src="https://nschloe.github.io/stressberry/4b.svg" width="70%">

#### Raspberry Pi 3B+
<img src="https://nschloe.github.io/stressberry/3b+.svg" width="70%">

#### Raspberry Pi 3B
<img src="https://nschloe.github.io/stressberry/3b.svg" width="70%">

There are a million ways to cool down your Raspberry Pi: Small heat sinks, specific
cases, and some [extreme DIY solutions](https://youtu.be/WfQMLInuwws).  stressberry is a
package for testing the core temperature under different loads, and it produces nice
plots which can easily be compared.

To run stressberry on your computer, simply install it with
```
[sudo] apt install stress
pip3 install stressberry --user
```
and run it with
```
stressberry-run out.dat
stressberry-plot out.dat -o out.png
```
(Use `MPLBACKEND=Agg stressberry-plot out.dat -o out.png` if you're running the script
on the Raspberry Pi itself.)

The run lets the CPU idle for a bit, then stresses it with maximum load for 5 minutes,
and lets it cool down afterwards. The entire process takes 10 minutes.  The resulting
data is displayed to a screen or, if specified, written to a PNG file.

If you'd like to submit your own data for display here, feel free to [open an
issue](https://github.com/nschloe/stressberry/issues) and include the data file, a
photograph of your setup, and perhaps some further information.

### The setups

#### A naked Raspberry Pi 3

<img src="https://nschloe.github.io/stressberry/naked-photo.jpg" width="30%">

The Raspberry Pi 3 without fans, heat sinks, or particular cases. The idle core
temperature is about 47°C, under heavy load it reaches 80°C (at which point the CPU
frequency is throttled).

#### A simple acrylic case

<img src="https://nschloe.github.io/stressberry/acryl-photo.jpg" width="30%">

Your average acrylic case from eBay. Temperature measurements are bit warmer than with
the naked Raspberry Pi, presumable because the case hinders the free air flow.

#### A black full-body aluminum alloy case

<img src="https://nschloe.github.io/stressberry/fasttech-photo.jpg" width="30%">

I got [this case](https://www.fasttech.com/p/5299000) from FastTech for about $17. It's
basically a full-body aluminum alloy case with heat pads for the CPU and the RAM chip.
The heat is dissipated _very_ well and in fact beats every other solution I've seen so
far, including [the extreme DIY passive cooling setup](https://youtu.be/WfQMLInuwws).

#### A Rasberry Pi 3B+ with a FLIRC case

<img src="https://nschloe.github.io/stressberry/flirc-photo.jpg" width="30%">

The famous [FLIRC case](https://flirc.tv/more/raspberry-pi-case).
Thanks to @RichardKav for the measurements!

#### A Rasberry Pi 4B with fans

<img src="https://nschloe.github.io/stressberry/rpi4-fans.jpg" width="40%">

Thanks to @flyingferret for the measurements!

### Testing

To run the tests, just check out this repository and type
```
pytest
```

### License
stressberry is published under the [MIT license](https://en.wikipedia.org/wiki/MIT_License).
