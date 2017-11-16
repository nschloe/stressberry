# -*- coding: utf-8 -*-
#
import subprocess
from time import sleep


def start_stressing(num_cpus, time):

    p = subprocess.Popen([
        'stress',
        '--cpu', str(num_cpus),
        '--timeout', '{}s'.format(time)
        ])

    while p.poll() is None:
        print('Still stressing', measure_temp())
        sleep(1)

    assert p.returncode == 0, \
        'Error! (return code {})'.format(p.returncode)

    # p = subprocess.Popen(
    #     cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    #     )
    # if verbose:
    #     while True:
    #         line = p.stdout.readline()
    #         if not line:
    #             break
    #         print(line.decode('utf-8'), end='')

    # p.communicate()
    # assert p.returncode == 0, \
    #     'Gmsh exited with error (return code {}).'.format(p.returncode)
    return


def measure_temp():
    p = subprocess.Popen('vcgencmd measure_temp', stdout=subprocess.PIPE)
    output, _error = p.communicate()
    return output.replace('temp=', '')
