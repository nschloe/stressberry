import tempfile

import stressberry


def test_run():
    temperature_file = tempfile.NamedTemporaryFile().name
    with open(temperature_file, "w") as f:
        f.write("12345")

    frequency_file = tempfile.NamedTemporaryFile().name
    with open(frequency_file, "w") as f:
        f.write("1500000")

    outfile1 = tempfile.NamedTemporaryFile().name
    stressberry.cli.run(
        [outfile1, "-d", "12", "-i", "2", "--cooldown", "1"]
    )
    
    outfile2 = tempfile.NamedTemporaryFile().name
    stressberry.cli.run(
        [outfile2, "-t", temperature_file, "-f", frequency_file, "-d", "12", "-i", "2", "--cooldown", "1"]
    )

    stressberry.cli.plot([outfile1, "-f", "--temp-lims", "20", "90", "--freq-lims", "500", "2000"])
    plotoutfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.plot([outfile2, "-f", "--temp-lims", "20", "90", "--freq-lims", "500", "2000", "-o", plotoutfile])
    return
