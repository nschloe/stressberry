import tempfile
import pytest
import stressberry


def pytest_namespace():
    return {"outfile": None}


def test_run():
    temperature_file = tempfile.NamedTemporaryFile().name
    with open(temperature_file, "w") as f:
        f.write("12345")

    frequency_file = tempfile.NamedTemporaryFile().name
    with open(frequency_file, "w") as f:
        f.write("1500000")

    # TODO: Need to mock call to subprocess.check_output
    # outfile1 = tempfile.NamedTemporaryFile().name
    # stressberry.cli.run(
    #     [outfile1, "-d", "12", "-i", "2", "--cooldown", "1"]
    # )

    pytest.outfile = tempfile.NamedTemporaryFile().name

    stressberry.cli.run(
        [
            pytest.outfile,
            "-t",
            temperature_file,
            "-f",
            frequency_file,
            "-d",
            "12",
            "-i",
            "2",
            "--cooldown",
            "1",
        ]
    )
    return


def test_plot():
    stressberry.cli.plot(
        [pytest.outfile, "-f", "--temp-lims", "20", "90", "--freq-lims", "500", "2000"]
    )


def test_plot_output_to_file():
    plotoutfile = tempfile.NamedTemporaryFile().name
    stressberry.cli.plot(
        [
            pytest.outfile,
            "-f",
            "--temp-lims",
            "20",
            "90",
            "--freq-lims",
            "500",
            "2000",
            "-o",
            plotoutfile,
        ]
    )
    return


def test_plot_line_widths():
    stressberry.cli.plot(
        [
            pytest.outfile,
            "-f",
            "--temp-lims",
            "20",
            "90",
            "--freq-lims",
            "500",
            "2000",
            "-lw",
            "0.5",
        ]
    )
    return


def test_plot_hide_legend():
    stressberry.cli.plot(
        [
            pytest.outfile,
            "-f",
            "--temp-lims",
            "20",
            "90",
            "--freq-lims",
            "500",
            "2000",
            "--hide-legend",
        ]
    )
    return


def test_plot_not_transparent():
    stressberry.cli.plot(
        [pytest.outfile, "-f", "--temp-lims", "20", "90", "--freq-lims", "500", "2000",]
    )
    return


def test_plot_legacy_style():
    stressberry.cli.plot(
        [
            pytest.outfile,
            "-f",
            "--temp-lims",
            "20",
            "90",
            "--freq-lims",
            "500",
            "2000",
            "--legacy-style",
        ]
    )
    return


def test_plot_legacy_style_color_blind_friendly():
    stressberry.cli.plot(
        [
            pytest.outfile,
            "-f",
            "--temp-lims",
            "20",
            "90",
            "--freq-lims",
            "500",
            "2000",
            "--legacy-style",
            "--color-blind-friendly",
        ]
    )
    return
