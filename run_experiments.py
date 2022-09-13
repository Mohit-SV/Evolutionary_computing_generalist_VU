import os
import sys
import train_specialist
from LinePlotter import generateLinePlots
import config as C
import time


cfg_names = ['group478m',
             'group478nm',
             'group245678m',
             'group245678nm']

out_dir = './results/'
s = time.time()
for cfg in cfg_names:
    cfg_object = getattr(C, cfg)
    for run in range(cfg_object.run):
        os.system(f'python train_specialist.py --cfg_name {cfg} --run {run+1}')
    generateLinePlots(cfg_object, out_dir=out_dir)
t = time.time()
print('Time taken to run all experiments', t-s)
