import argparse

import yaml

from .helpers import _get_version_text


def plot(argv=None):
    import matplotlib.pyplot as plt

    parser = _get_parser_plot()
    args = parser.parse_args(argv)

    data = [yaml.load(f, Loader=yaml.SafeLoader) for f in args.infiles]

    # sort the data such that the data series with the lowest terminal
    # temperature is plotted last (and appears in the legend last)
    terminal_temps = [d["temperature"][-1] for d in data]
    order = [i[0] for i in sorted(enumerate(terminal_temps), key=lambda x: x[1])]
    # actually plot it
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for k in order[::-1]:
        temperature_data = data[k]["temperature"]
        if args.delta_t:
            temperature_data = [t - data[k]["ambient"] for t in data[k]["temperature"]]
        ax1.plot(
            data[k]["time"], temperature_data, label=data[k]["name"], lw=args.line_width
        )

    ax1.grid()
    if not args.hide_legend:
        ax1.legend(loc="upper left", bbox_to_anchor=(1.03, 1.0), borderaxespad=0)
    if args.delta_t:
        plot_yaxis_label = "Δ temperature °C (over ambient)"
    else:
        plot_yaxis_label = "temperature °C"
    ax1.set_xlabel("time (s)")
    ax1.set_ylabel(plot_yaxis_label)
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
    parser.add_argument(
        "--delta-t",
        action="store_true",
        default=False,
        help="Use Delta-T (core - ambient) temperature instead of CPU core temperature",
    )
    return parser
