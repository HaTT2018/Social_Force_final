# -*- coding: utf-8 -*-
from concurrent.futures import ProcessPoolExecutor, wait
import sys
import os
import math
import time
import fire

def e(n):
    e=0
    for i in range(2,n):
        e += 1/i/math.log(i)
    sys.stdout.write('process %s n=%d result=%.20f\n'%(os.getpid(),n,e))
    return e

def ee(n):
    ee=0
    for i in range(2,n):
        ee += 1/i/math.log(i)/i
    sys.stdout.write('process %s n=%d result=%.20f\n'%(os.getpid(),n,ee))
    return ee

def main(process_num, *ns):
    executor = ProcessPoolExecutor(process_num)
    start = time.time()
    fs = []
    fs.append(executor.submit(e,ns[0]))
    fs.append(executor.submit(ee,ns[1]))
    fs.append(executor.submit(e,ns[2]))
    fs.append(executor.submit(ee,ns[3]))
    print(fs[0].result())
    wait(fs)
    end = time.time()
    duration  = end-start
    print('Total time%.2f'%duration)
    executor.shutdown()

if __name__ == '__main__':
    fire.Fire(main)