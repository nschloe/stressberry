<p align="center">
  <a href="https://github.com/nschloe/stressberry"><img alt="stressberry" src="https://nschloe.github.io/stressberry/stressberry.png" width="60%"></a>
  <p align="center">Stress tests and temperature plots for the Raspberry Pi</p>
</p>

[![CircleCI](https://img.shields.io/circleci/project/github/nschloe/stressberry/master.svg?style=flat-square)](https://circleci.com/gh/nschloe/stressberry/tree/master)
[![codecov](https://img.shields.io/codecov/c/github/nschloe/stressberry.svg?style=flat-square)](https://codecov.io/gh/nschloe/stressberry)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![awesome](https://img.shields.io/badge/awesome-yes-brightgreen.svg?style=flat-square)](https://github.com/nschloe/stressberry)
[![PyPi Version](https://img.shields.io/pypi/v/stressberry.svg?style=flat-square)](https://pypi.org/project/stressberry)
[![GitHub stars](https://img.shields.io/github/stars/nschloe/stressberry.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/nschloe/stressberry)
[![PyPi downloads](https://img.shields.io/pypi/dm/stressberry.svg?style=flat-square)](https://pypistats.org/packages/stressberry)

There are a million ways to cool down your Raspberry Pi: Small heat sinks, specific
cases, and some [extreme DIY solutions](https://youtu.be/WfQMLInuwws). stressberry is a
package for testing the core temperature under different loads, and it produces nice
plots which can easily be compared.

### Raspberry Pi 4B
<img src="https://nschloe.github.io/stressberry/4b.svg" width="70%">

<img src="https://nschloe.github.io/stressberry/rpi4-fans.jpg" width="70%"> | <img src="https://nschloe.github.io/stressberry/kksb.jpg" width="70%"> | <img src="https://nschloe.github.io/stressberry/argon-one.jpg" width="70%">
:--------------------------------------:|:----------------------:|:------:|
custom case with fans  (@flyingferret, [#21](https://github.com/nschloe/stressberry/issues/21))  | [KKSB case](https://kksb-cases.com/products/kksb-raspberry-pi-4-case-aluminium) (@JohBod, [#31](https://github.com/nschloe/stressberry/issues/31)) | [Argon One case](https://www.argon40.com/argon1/argon-one-pi4.html) (@jholloway, [#37](https://github.com/nschloe/stressberry/issues/37))
<img src="https://nschloe.github.io/stressberry/hex-wrench.png" width="70%"> | <img src="https://nschloe.github.io/stressberry/coolipi.jpg" width="70%"> | <img src="https://nschloe.github.io/stressberry/ice-tower.jpg" width="70%">
[hex wrench case](https://www.amazon.ca/Aluminum-Model-Raspberry-Wrench-Enclosure/dp/B07W6FT1DD?th=1) (@patrickpoirier51, [#45](https://github.com/nschloe/stressberry/issues/45)) | [CooliPi](https://www.coolipi.com/) (@CooliPi, [#47](https://github.com/nschloe/stressberry/issues/47), [#48](https://github.com/nschloe/stressberry/issues/48)) | [low-profile ice tower case](https://www.aliexpress.com/i/4000288119233.html) (@leonhess, [#54](https://github.com/nschloe/stressberry/issues/54))
<img src="https://nschloe.github.io/stressberry/flirc4b.jpeg" width="70%"> | |
[Flirc case](https://flirc.tv/more/raspberry-pi-4-case) (@RichardKav, [#73](https://github.com/nschloe/stressberry/issues/73)) | |


### Raspberry Pi 3B+
<img src="https://nschloe.github.io/stressberry/3b+.svg" width="70%">

#### FLIRC case

<img src="https://nschloe.github.io/stressberry/flirc-photo.jpg" width="30%">

The famous [FLIRC case](https://flirc.tv/more/raspberry-pi-case).
Thanks to @RichardKav for the measurements!

### Raspberry Pi 3B
<img src="https://nschloe.github.io/stressberry/3b.svg" width="70%">

<img src="https://nschloe.github.io/stressberry/naked-photo.jpg" width="90%"> | <img src="https://nschloe.github.io/stressberry/acryl-photo.jpg" width="90%"> | <img src="https://nschloe.github.io/stressberry/fasttech-photo.jpg" width="90%">
:-------------------:|:------------------:|:----------:|
No fans, heat sinks, or case. | Your average acrylic case from eBay. | [FastTech case](https://www.fasttech.com/p/5299000), full-body aluminum alloy with heat pads for CPU and RAM.

### How to

To run stressberry on your computer, simply install it with
```
[sudo] apt install stress
pip install stressberry
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


### Testing

To run the tests, just check out this repository and type
```
pytest
```

### License
This software is published under the [GPLv3 license](https://www.gnu.org/licenses/gpl-3.0.en.html).
