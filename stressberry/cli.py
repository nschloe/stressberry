import argparse
import datetime
import sys
import threading
import time

import matplotlib.pyplot as plt
import yaml

from .__about__ import __copyright__, __version__
from .main import cooldown, measure_temp, measure_core_frequency, test


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
    while t.is_alive():
        times.append(time.time())
        temps.append(measure_temp(args.temperature_file))
        freqs.append(measure_core_frequency(args.frequency_file))
        print(
            "Current temperature: {:4.1f}°C - Frequency: {:4.0f}MHz".format(
                temps[-1], freqs[-1]
            )
        )
        # Choose the sample interval such that we have a respectable number of
        # data points
        t.join(2.0)

    # normalize times
    time0 = times[0]
    times = [tm - time0 for tm in times]

    args.outfile.write(
        "# This file was created by stressberry v{} on {}\n".format(
            __version__, datetime.datetime.now()
        )
    )
    yaml.dump(
        {
            "name": args.name,
            "time": times,
            "temperature": temps,
            "cpu frequency": freqs,
        },
        args.outfile,
    )
    return


def plot(argv=None):
    parser = _get_parser_plot()
    args = parser.parse_args(argv)

    data = [yaml.load(f, Loader=yaml.SafeLoader) for f in args.infiles]

    # sort the data such that the data series with the lowest terminal
    # temperature is plotted last (and appears in the legend last)
    terminal_temps = [d["temperature"][-1] for d in data]
    order = [i[0] for i in sorted(enumerate(terminal_temps), key=lambda x: x[1])]
    # actually plot it
    fig = plt.figure()
    ax1 = fig.add_subplot()
    for k in order[::-1]:
        ax1.plot(
            data[k]["time"],
            data[k]["temperature"],
            label=data[k]["name"],
            lw=args.line_width,
        )

    ax1.grid()
    if not args.hide_legend:
        ax1.legend(loc="upper left", bbox_to_anchor=(1.03, 1.0), borderaxespad=0)
    ax1.set_xlabel("time (s)")
    ax1.set_ylabel("temperature (°C)")
    ax1.set_xlim([data[-1]["time"][0], data[-1]["time"][-1]])
    if args.temp_lims:
        ax1.set_ylim(*args.temp_lims)

    # Only plot frequencies when using a single input file
    if len(data) == 1 and args.frequency:
        ax2 = plt.twinx()
        ax2.set_ylabel("core frequency (MHz)")
        if args.freq_lims:
            ax2.set_ylim(*args.freq_lims)
        try:
            for k in order[::-1]:
                ax2.plot(
                    data[k]["time"],
                    data[k]["cpu frequency"],
                    label=data[k]["name"],
                    color="C1",
                    alpha=0.9,
                    lw=args.line_width,
                )
            ax1.set_zorder(ax2.get_zorder() + 1)  # put ax1 plot in front of ax2
            ax1.patch.set_visible(False)  # hide the 'canvas'
        except KeyError():
            print("Source data does not contain CPU frequency data.")

    if args.outfile is not None:
        plt.savefig(
            args.outfile,
            transparent=args.transparent,
            bbox_inches="tight",
            dpi=args.dpi,
        )
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
    parser.add_argument(
        "-d",
        "--dpi",
        type=int,
        default=None,
        help="image resolution in dots per inch when written to file",
    )
    parser.add_argument(
        "-f",
        "--frequency",
        help="plot CPU core frequency (single input files only)",
        action="store_true",
    )
    parser.add_argument(
        "-l",
        "--freq-lims",
        type=float,
        nargs=2,
        default=None,
        help="limits for the frequency scale (default: data limits)",
    )
    parser.add_argument("--hide-legend", help="do not draw legend", action="store_true")
    parser.add_argument(
        "--not-transparent",
        dest="transparent",
        help="do not make images transparent",
        action="store_false",
        default=True,
    )
    parser.add_argument(
        "-lw", "--line-width", type=float, default=None, help="line width"
    )
    return parser
