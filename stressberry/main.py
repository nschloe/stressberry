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
        sys_tempfile=open("/sys/class/thermal/thermal_zone0/temp", "r")
        sys_temp =sys_tempfile.read()
        sys_tempfile.close()
        temp_int = int(sys_temp)
        temp = float(temp_int/1000)
    return temp


def measure_core_frequency(filename=None):
    """Returns the CPU frequency in MHz
    """
    if filename is not None:
        with open(filename, "r") as f:
            frequency = float(f.read()) / 1000
    else:
        # Only vcgencmd measure_clock arm is accurate on Raspberry Pi.
        # Per: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=219358&start=25
        sys_freqfile=open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq", "r")
        sys_freq =sys_freqfile.read()
        sys_freqfile.close()
        freq_int = int(sys_freq)
        frequency = freq_int / 1000
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
