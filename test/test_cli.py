# -*- coding: utf-8 -*-
#
import tempfile
import stressberry


def test_run():
    temperature_file = tempfile.NamedTemporaryFile().name
    with open(temperature_file, "w") as f:
        f.write("12345")

    outfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.run([outfile, temperature_file])
    return
