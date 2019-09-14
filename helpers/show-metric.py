import argparse
import glob
import yaml

def getFiles():
    filelist = [f for f in glob.glob("*.out", recursive=False)]
    return filelist

def printAmbient(outFiles=None, metric=None):
    # csv header
    print("FileName,Metric,Min,Max,Var")
    # data
    for f in outFiles:
        with open(f, 'r') as stream:
            data = yaml.safe_load(stream)
        minimum = min(data[metric])
        maximum = max(data[metric])
        variance = maximum - minimum
        print("{},{},{},{},{}".format(f, metric, minimum, maximum, variance))

def _get_parser_metrics():
    parser = argparse.ArgumentParser(description="CSV of basic metrics")
    parser.add_argument(
        "metric",
        type=str,
        help="metric to dump [ambient, temperature, cpu frequency, delta-t]",
    )
    return parser

if __name__ == "__main__":
    argv=None
    parser = _get_parser_metrics()
    args = parser.parse_args(argv)
    filelist = getFiles()
    printAmbient(outFiles=filelist, metric=args.metric)
