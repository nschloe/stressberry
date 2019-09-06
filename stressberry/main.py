import subprocess
import time as tme
from os import cpu_count


def stress_cpu(num_cpus, time):
    subprocess.check_call(
        ["stress", "--cpu", str(num_cpus), "--timeout", "{}s".format(time)]
    )
    return


def cooldown(interval=60, filename=None):
    """Lets the CPU cool down until the temperature does not change anymore.
    """
    prev_tmp = measure_temp(filename=filename)
    while True:
        tme.sleep(interval)
        tmp = measure_temp(filename=filename)
        print(
            "Current temperature: {:4.1f}°C - Previous temperature: {:4.1f}°C".format(
                tmp, prev_tmp
            )
        )
        if abs(tmp - prev_tmp) < 0.2:
            break
        prev_tmp = tmp
    return tmp


def measure_temp(filename=None):
    """Returns the core temperature in Celsius.
    """
    if filename is not None:
        with open(filename, "r") as f:
            temp = float(f.read()) / 1000
    else:
        # Using vcgencmd is specific to the raspberry pi
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        temp = float(out.replace("temp=", "").replace("'C", ""))
    return temp


def measure_core_frequency(filename=None):
    """Returns the CPU frequency in MHz
    """
    if filename is not None:
        with open(filename, "r") as f:
            frequency = int(f.read()) / 1000
    else:
        # Only vcgencmd measure_clock arm is accurate on Raspberry Pi.
        # Per: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=219358&start=25
        out = subprocess.check_output(["vcgencmd", "measure_clock arm"]).decode("utf-8")
        frequency = int(int(out.split("=")[1]) / 1000000)
    return frequency


def test(stress_duration, idle_duration, cores):
    """Run stress test for specified duration with specified idle times
       at the start and end of the test.
    """
    if cores is None:
        cores = cpu_count()

    print(
        "Preparing to stress [{}] CPU Cores for [{}] seconds".format(
            cores, stress_duration
        )
    )
    print("Idling for {} seconds...".format(idle_duration))
    tme.sleep(idle_duration)

    stress_cpu(num_cpus=cores, time=stress_duration)

    print("Idling for {} seconds...".format(idle_duration))
    tme.sleep(idle_duration)
    return
