import subprocess
import time as tme
from os import cpu_count


def stress_cpu(num_cpus, time):
    subprocess.check_call(["stress", "--cpu", str(num_cpus), "--timeout", f"{time}s"])
    return


def cooldown(interval=60, filename=None):
    """Lets the CPU cool down until the temperature does not change anymore."""
    prev_tmp = measure_temp(filename=filename)
    while True:
        tme.sleep(interval)
        tmp = measure_temp(filename=filename)
        print(
            f"Current temperature: {tmp:4.1f}°C - "
            f"Previous temperature: {prev_tmp:4.1f}°C"
        )
        if abs(tmp - prev_tmp) < 0.2:
            break
        prev_tmp = tmp
    return tmp


def measure_temp(filename=None):
    """Returns the core temperature in Celsius."""
    if filename is not None:
        with open(filename) as f:
            temp = float(f.read()) / 1000
    else:
        # Using vcgencmd is specific to the raspberry pi
        out = subprocess.check_output(["vcgencmd", "measure_temp"]).decode("utf-8")
        temp = float(out.replace("temp=", "").replace("'C", ""))
    return temp


def measure_core_frequency(filename=None):
    """Returns the CPU frequency in MHz"""
    if filename is not None:
        with open(filename) as f:
            frequency = float(f.read()) / 1000
    else:
        # Only vcgencmd measure_clock arm is accurate on Raspberry Pi.
        # Per: https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=219358&start=25
        out = subprocess.check_output(["vcgencmd", "measure_clock arm"]).decode("utf-8")
        frequency = float(out.split("=")[1]) / 1000000
    return frequency


def measure_ambient_temperature(sensor_type="2302", pin="23"):
    """Uses Adafruit temperature sensor to measure ambient temperature"""
    try:
        import Adafruit_DHT  # Late import so that library is only needed if requested
    except ImportError as e:
        print("Install adafruit_dht python module: pip install Adafruit_DHT")
        raise e

    sensor_map = {
        "11": Adafruit_DHT.DHT11,
        "22": Adafruit_DHT.DHT22,
        "2302": Adafruit_DHT.AM2302,
    }
    try:
        sensor = sensor_map[sensor_type]
    except KeyError as e:
        print("Invalid ambient temperature sensor")
        raise e
    _, temperature = Adafruit_DHT.read_retry(sensor, pin)
    # Note that sometimes you won't get a reading and the results will be null (because
    # Linux can't guarantee the timing of calls to read the sensor).  The read_retry
    # call will attempt to read the sensor 15 times with a 2 second delay.  Care should
    # be taken when reading if on a time sensitive path Temperature is in °C but can
    # also be None
    return temperature


def test(stress_duration, idle_duration, cores):
    """Run stress test for specified duration with specified idle times
    at the start and end of the test.
    """
    if cores is None:
        cores = cpu_count()

    print(f"Preparing to stress [{cores}] CPU Cores for [{stress_duration}] seconds")
    print(f"Idling for {idle_duration} seconds...")
    tme.sleep(idle_duration)

    stress_cpu(num_cpus=cores, time=stress_duration)

    print(f"Idling for {idle_duration} seconds...")
    tme.sleep(idle_duration)
