# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:56:24 2017

@author: Jerome
"""
import visa
import numpy as np
import time
from decimal import Decimal
rm = visa.ResourceManager()
rm.list_resources()
dsp7265 = rm.open_resource("GPIB::12::INSTR")
dsp7265.write('DD044')

#Designed to sweep anything 
# max and min are as suspected
#sweep_item is the variable you are sweeping (ex. OA for output amplitude)

#dtbt is a string of the GPIB commands to measure the variables
# you are interested in

#dtbt_num is the number of variables for forming an array of the desired output

#Be careful with timing step, 1 second seems long enough, but may sometimes
#be too long


def sr_sweep(sweep_max,sweep_min,steps,sweep_item,dtbt,dtbt_num):

    dsp7265.write(sweep_item+str(sweep_min))
    d_sweep = abs(sweep_max-sweep_min)//steps
    total_steps = steps*2+1
    cols=dtbt_num+1
    data_array = np.zeros([total_steps+1,cols],float)
    i=0
    j=i
    amp = sweep_min
#    col_headings = dtbt.split(';')
#    print(col_headings)
#    for l in range(0,dtbt_num+1):
#        data_array[0][l] = col_headings[l]
    #Do sweep
    while (i<steps):        
        dsp7265.write(sweep_item+str(amp))
        time.sleep(1)
        mag = dsp7265.query(dtbt)
        
        time.sleep(1)
        data = mag.split('\r\n')
        data_array[j][0] = amp
        for x in range(1,cols):
            data_array[j][x] = int(data[x-1])        
        time.sleep(0.1)
        amp = amp + d_sweep
        
        i = i+1
        j=i
    while (i>=0):        
        dsp7265.write(sweep_item+str(amp))
        time.sleep(1)
        mag = dsp7265.query(dtbt)
        time.sleep(1)
        data = mag.split('\r\n')
        data_array[j][0] = amp
        for x in range(1,cols):
            data_array[j][x] = int(data[x-1])
        time.sleep(0.1)
        amp = amp - d_sweep
        i = i-1
        j=j+1
    return data_array;