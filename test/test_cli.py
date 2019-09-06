import tempfile

import stressberry


def test_run():
    temperature_file = tempfile.NamedTemporaryFile().name
    with open(temperature_file, "w") as f:
        f.write("12345")

    frequency_file = tempfile.NamedTemporaryFile().name
    with open(frequency_file, "w") as f:
        f.write("1500000")

    outfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.run([outfile, "-t", temperature_file, "-f", frequency_file, "-d", "12", "-i", "3"])

    stressberry.cli.plot([outfile])
    return
