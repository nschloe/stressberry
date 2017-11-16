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


def cooldown(interval=10):
    '''Lets the cpu cool down until the temperature does not drop anymore.
    '''
    prev_tmp = measure_temp()
    while True:
        tme.sleep(interval)
        tmp = measure_temp()
        if tmp >= prev_tmp:
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
    m = re.match('frequency\([0-9]+\)=([0-9]+)', output)
    return int(m.group(1))
