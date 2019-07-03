import tempfile

import stressberry


def test_run():
    temperature_file = tempfile.NamedTemporaryFile().name
    with open(temperature_file, "w") as f:
        f.write("12345")

    outfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.run([outfile, "-t", temperature_file, "-d", "12"])

    stressberry.cli.plot([outfile])
    return
