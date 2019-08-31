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
        print(
            "Current temperature: {}°C - Previous temperature: {}°C".format(
                tmp, prev_tmp
            ),
            end="\r",
        )
        if abs(tmp - prev_tmp) < 0.2:
            break
        prev_tmp = tmp
        print("")  # Ensure next message starts on a new line.
    return tmp


def measure_temp(filename="/sys/class/thermal/thermal_zone0/temp", use_vcgencmd=False):
    """Returns the core temperature in Celsius.
    """
    if use_vcgencmd:
        # Usign vcgencmd is specific to the raspberry pi
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        temp = float(out.replace("temp=", "").replace("'C", ""))
    else:
        with open(filename, "r") as f:
            temp = float(f.read()) / 1000
    return temp


def measure_core_frequency(
    filename="/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", use_vcgencmd=False
):
    """Returns the CPU frequency in MHz
    """
    if use_vcgencmd:
        # Only vcgencmd measure_clock arm is accurate on Raspberry Pi.
        # Per: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=219358&start=25
        # TODO: May also need to look at: vcgencmd get_throttled
        out = subprocess.check_output(["vcgencmd", "measure_clock arm"]).decode("utf-8")
        frequency = int(int(out.split("=")[1]) / 1000000)
    else:
        with open(filename, "r") as f:
            frequency = int(f.read()) / 1000
    return frequency


def vcgencmd_avaialble():
    """Returns true if vcgencmd is runable, false otherwise
    """
    try:
        subprocess.call(["vcgencmd"])
        return True
    except OSError:
        return False


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
