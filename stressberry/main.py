# -*- coding: utf-8 -*-
#
import re
import subprocess
import time as tme


def stress_cpu(num_cpus, time):
    subprocess.check_call([
        'stress',
        '--cpu', str(num_cpus),
        '--timeout', '{}s'.format(time)
        ])
    return


def cooldown(interval=60):
    '''Lets the CPU cool down until the temperature does not change anymore.
    '''
    prev_tmp = measure_temp()
    while True:
        tme.sleep(interval)
        tmp = measure_temp()
        if abs(tmp - prev_tmp) < 0.2:
            break
        prev_tmp = tmp
    return tmp


def measure_temp():
    '''Returns the core temperature in Celsius.
    '''
    output = subprocess.check_output(
        ['vcgencmd', 'measure_temp']
        ).decode('utf-8')
    return float(output.replace('temp=', '').replace('\'C', ''))


def measure_core_frequency():
    '''Returns the processor frequency in Hz.
    '''
    output = subprocess.check_output(
        ['vcgencmd', 'measure_clock', 'arm']
        ).decode('utf-8')

    # frequency(45)=102321321
    m = re.match('frequency\\([0-9]+\\)=([0-9]+)', output)
    return int(m.group(1))


def test_short():
    print('Idling...')
    tme.sleep(150)
    stress_cpu(4, time=300)
    print('Idling...')
    tme.sleep(150)
    return


def test_long():
    print('Idling...')
    tme.sleep(600)
    for num_cpus in range(1, 5):
        stress_cpu(num_cpus, time=600)
        print('Idling...')
        tme.sleep(300)
    return
