import argparse

import yaml

from .helpers import _get_version_text


def plot(argv=None):
    import dufte
    import matplotlib.pyplot as plt

    plt.style.use(dufte.style)

    parser = _get_parser_plot()
    args = parser.parse_args(argv)

    data = [yaml.load(f, Loader=yaml.SafeLoader) for f in args.infiles]

    # actually plot it
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    for d in data:
        temperature_data = d["temperature"]
        if args.delta_t:
            temperature_data = []
            zip_object = zip(d["temperature"], d["ambient"])
            for d["temperature"], d["ambient"] in zip_object:
                temperature_data.append(d["temperature"] - d["ambient"])

        plt.plot(d["time"], temperature_data, label=d["name"])

    dufte.legend()

    if args.delta_t:
        plot_yaxis_label = "Δ temperature [°C over ambient]"
    else:
        plot_yaxis_label = "temperature [°C]"
    plt.xlabel("time [s]")
    plt.ylabel(plot_yaxis_label)

    if args.temp_lims:
        ax1.set_ylim(*args.temp_lims)

    # Only plot frequencies when using a single input file
    if len(data) == 1 and args.frequency:
        ax2 = plt.twinx()
        ax2.set_ylabel("core frequency (MHz)")
        if args.freq_lims:
            ax2.set_ylim(*args.freq_lims)
        try:
            for d in data:
                ax2.plot(
                    d["time"],
                    d["cpu frequency"],
                    label=d["name"],
                    color="C1",
                    alpha=0.9,
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
    parser.add_argument(
        "--not-transparent",
        dest="transparent",
        help="do not make images transparent",
        action="store_false",
        default=True,
    )
    parser.add_argument(
        "--delta-t",
        action="store_true",
        default=False,
        help="Use Delta-T (core - ambient) temperature instead of CPU core temperature",
    )
    return parser
