# -*- coding: utf-8 -*-
#
import tempfile
import stressberry


def test_run():
    outfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.run([outfile])
    return
