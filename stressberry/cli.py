import argparse
import datetime
import sys
import threading
import time

import matplotlib.pyplot as plt
import yaml

from .__about__ import __copyright__, __version__
from .main import cooldown, measure_temp, test


def _get_version_text():
    return "\n".join(
        [
            "stressberry {} [Python {}.{}.{}]".format(
                __version__,
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            ),
            __copyright__,
        ]
    )


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
        default="/sys/class/thermal/thermal_zone0/temp",
        help="temperature file (default: /sys/class/thermal/thermal_zone0/temp)",
    )
    parser.add_argument(
        "-d",
        "--duration",
        type=int,
        default=600,
        help="test duration in seconds (default: 600)",
    )
    parser.add_argument("outfile", type=argparse.FileType("w"), help="output data file")
    return parser


def run(argv=None):
    parser = _get_parser_run()
    args = parser.parse_args(argv)

    # Cool down first
    print("Cooldown...")
    cooldown(filename=args.temperature_file)

    # Start the stress test in another thread
    t = threading.Thread(target=lambda: test(args.duration), args=())
    t.start()

    times = []
    temps = []
    while t.is_alive():
        times.append(time.time())
        temps.append(measure_temp(args.temperature_file))
        # Choose the sample interval such that we have a respectable number of
        # data points
        t.join(2.0)
        print("Current temperature: {}°C".format(temps[-1]))

    # normalize times
    time0 = times[0]
    times = [tm - time0 for tm in times]

    args.outfile.write(
        "# This file was created by stressberry v{} on {}\n".format(
            __version__, datetime.datetime.now()
        )
    )
    yaml.dump({"name": args.name, "time": times, "temperature": temps}, args.outfile)
    return


def plot(argv=None):
    parser = _get_parser_plot()
    args = parser.parse_args(argv)

    data = [yaml.load(f, Loader=yaml.SafeLoader) for f in args.infiles]

    # sort the data such that the data series with the lowest terminal
    # temperature is plotted last (and appears int he legend last)
    terminal_temps = [d["temperature"][-1] for d in data]
    order = [i[0] for i in sorted(enumerate(terminal_temps), key=lambda x: x[1])]
    # actually plot it
    for k in order[::-1]:
        plt.plot(data[k]["time"], data[k]["temperature"], label=data[k]["name"])

    plt.grid()
    plt.legend(loc="upper left", bbox_to_anchor=(1.03, 1.0), borderaxespad=0)
    plt.xlabel("time (s)")
    plt.ylabel("temperature (°C)")
    plt.xlim([data[-1]["time"][0], data[-1]["time"][-1]])
    if args.temp_lims:
        plt.ylim(*args.temp_lims)

    if args.outfile is not None:
        plt.savefig(args.outfile, transparent=True, bbox_inches="tight")
    else:
        plt.show()
    return


def _get_parser_plot():
    parser = argparse.ArgumentParser(description="Plot stress test data.")
    parser.add_argument(
        "--version", "-v", action="version", version=_get_version_text()
    )
    parser.add_argument(
        "infiles",
        nargs="+",
        type=argparse.FileType("r"),
        help="input YAML file(s) (default: stdin)",
    )
    parser.add_argument(
        "-o",
        "--outfile",
        help=(
            "if specified, the plot is written to this file "
            "(default: show on screen)"
        ),
    )
    parser.add_argument(
        "-t",
        "--temp-lims",
        type=float,
        nargs=2,
        default=None,
        help="limits for the temperature (default: data limits)",
    )
    return parser
