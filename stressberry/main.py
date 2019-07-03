import subprocess
import time as tme


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


def test(duration):
    print("Idling...")
    tme.sleep(0.25 * duration)
    stress_cpu(4, time=0.5 * duration)
    print("Idling...")
    tme.sleep(0.25 * duration)
    return
