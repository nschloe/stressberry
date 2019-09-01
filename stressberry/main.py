import subprocess
import time as tme
from os import cpu_count


def stress_cpu(num_cpus, time):
    subprocess.check_call(
        ["stress", "--cpu", str(num_cpus), "--timeout", "{}s".format(time)]
    )
    return


def cooldown(interval=60, filename="/sys/class/thermal/thermal_zone0/temp"):
    """Lets the CPU cool down until the temperature does not change anymore.
    """
    prev_tmp = measure_temp(filename=filename)
    while True:
        tme.sleep(interval)
        tmp = measure_temp(filename=filename)
        if abs(tmp - prev_tmp) < 0.2:
            break
        prev_tmp = tmp
    return tmp


def measure_temp(filename="/sys/class/thermal/thermal_zone0/temp"):
    """Returns the core temperature in Celsius.
    """
    with open(filename, "r") as f:
        temp = float(f.read()) / 1000

    # Usign vcgencmd is specific to the raspberry pi
    # out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
    # temp = float(out.replace("temp=", "").replace("'C", ""))

    return temp


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
