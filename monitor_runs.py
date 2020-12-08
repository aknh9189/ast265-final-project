#!/usr/bin/python

from glob import glob
import os 
import time
import subprocess
import sys
last_tt = time.time()
last_percent = {}
while True:
    directories = glob("*/")
    output = ""
    for fi in directories:
        if os.path.exists(fi  +'Ice/output.txt0'):
            last_time = os.stat(fi+'Ice/output.txt0').st_mtime
            t = time.time()
            dt = t-last_tt
            last_tt = t
            if t - last_time > 30:
                continue
            with open(fi + "Ice/output.txt0", 'r') as f:
                data = f.read()
            last_idx = data.rfind('PERCENT')
            if last_idx != -1:
                trimmed = data[last_idx:]
                trimmed = trimmed.split("\n")[0]
                trimmed = trimmed.split(" ")[-1]
                perc = float(trimmed[:-1])
                eta = 0.0
                if fi in last_percent and perc - last_percent[fi] > 0:
                    eta = (100 - perc) / ((perc - last_percent[fi]) / dt) / 60
                last_percent[fi] = perc
                output += fi + " " + trimmed +  "\t"
    #sys.stdout.write("\r" + output)
    #sys.stdout.flush()
    print(str(time.time()) + " " + output)
    sys.stdout.flush()
    time.sleep(60)


