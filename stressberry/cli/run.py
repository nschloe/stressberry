import argparse
import datetime
import threading
import time

import yaml

from ..__about__ import __version__
from ..main import (
    cooldown,
    measure_ambient_temperature,
    measure_core_frequency,
    measure_temp,
    test,
)
from .helpers import _get_version_text


def _get_parser_run():
    parser = argparse.ArgumentParser(
        description="Run stress test for the Raspberry Pi."
    )
    parser.add_argument(
        "--version", "-v", action="version", version=_get_version_text()
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="stressberry data",
        help="name the data set (default: 'stressberry data')",
    )
    parser.add_argument(
        "-t",
        "--temperature-file",
        type=str,
        default=None,
        help="temperature file e.g /sys/class/thermal/thermal_zone0/temp (default: vcgencmd)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=300,
        help="stress test duration in seconds (default: 300)",
    )
    parser.add_argument(
        "-i",
        "--idle",
        type=int,
        default=150,
        help="idle time in seconds at start and end of stress test (default: 150)",
    )
    parser.add_argument(
        "--cooldown",
        type=int,
        default=60,
        help="poll interval seconds to check for stable temperature (default: 60)",
    )
    parser.add_argument(
        "-c",
        "--cores",
        type=int,
        default=None,
        help="number of CPU cores to stress (default: all)",
    )
    parser.add_argument(
        "-f",
        "--frequency-file",
        type=str,
        default=None,
        help="CPU core frequency file e.g. /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq (default: vcgencmd)",
    )
    parser.add_argument(
        "-a",
        "--ambient",
        type=str,
        nargs=2,
        default=None,
        help="measure ambient temperature. Sensor Type [11|22|2302] <GPIO Number> e.g. 2302 26",
    )
    parser.add_argument("outfile", type=argparse.FileType("w"), help="output data file")
    return parser


def run(argv=None):
    parser = _get_parser_run()
    args = parser.parse_args(argv)

    # Cool down first
    print("Awaiting stable baseline temperature...")
    cooldown(interval=args.cooldown, filename=args.temperature_file)

    # Start the stress test in another thread
    t = threading.Thread(
        target=lambda: test(args.duration, args.idle, args.cores), args=()
    )
    t.start()

    times = []
    temps = []
    freqs = []
    ambient = []
    while t.is_alive():
        times.append(time.time())
        temps.append(measure_temp(args.temperature_file))
        freqs.append(measure_core_frequency(args.frequency_file))
        if args.ambient:
            ambient_temperature = measure_ambient_temperature(
                sensor_type=args.ambient[0], pin=args.ambient[1]
            )
            if ambient_temperature is None:
                # Reading the sensor can return None if it times out.
                # If never had a good result, probably configuration error
                # Else use last known value if available or worst case set to zero
                if not ambient:
                    print(
                        f"Could not read ambient temperature sensor {args.ambient[0]} "
                        f"on pin {args.ambient[1]}"
                    )
                else:
                    print(
                        "WARN - Could not read ambient temperature, "
                        "using last good value"
                    )
                ambient_temperature = next(
                    (temp for temp in reversed(ambient) if temp is not None), 0
                )
            ambient.append(ambient_temperature)
            delta_t = temps[-1] - ambient[-1]
            print(
                "Temperature (current | ambient | ΔT): "
                f"{temps[-1]:4.1f}°C | {ambient[-1]:4.1f}°C | {delta_t:4.1f}°C "
                f"- Frequency: {freqs[-1]:4.0f}MHz"
            )
        else:
            print(
                f"Current temperature: {temps[-1]:4.1f}°C "
                f"- Frequency: {freqs[-1]:4.0f}MHz"
            )
        # Choose the sample interval such that we have a respectable number of
        # data points
        t.join(2.0)

    # normalize times
    time0 = times[0]
    times = [tm - time0 for tm in times]

    args.outfile.write(
        f"# This file was created by stressberry v{__version__} "
        f"on {datetime.datetime.now()}\n"
    )
    yaml.dump(
        {
            "name": args.name,
            "time": times,
            "temperature": temps,
            "cpu frequency": freqs,
            "ambient": ambient,
        },
        args.outfile,
    )
