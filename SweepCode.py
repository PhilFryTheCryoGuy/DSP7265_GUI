# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:56:24 2017

@author: Jerome
"""
import visa
import numpy as np
import time
import threading 

rm = visa.ResourceManager()
rm.list_resources()
dsp7265 = rm.open_resource("GPIB::12::INSTR")
dsp7265.write('DD044')

import pyqtgraph as pg;

global curve, ptr

#data taking subroutine
def take_data(y,z,ampl,sw_item,dbt,cols,dat_array,a,b,var,sensmod):
    dsp7265.write(sw_item+str(ampl))
    time.sleep(0.1)    
    print(dbt)        
    mag = dsp7265.query(dbt)
    time.sleep(0.1)
    #split apart and store recorded data
    data = mag.split('\r\n')
    print(mag)
    dat_array[z][0] = ampl

    for x in range(1,cols-1):
        dat_array[z][x] = int(data[x-1])      
    a[z] = ampl
    b[z] = dat_array[z][var]*sensmod  
    time.sleep(0.002)            
    return dat_array,a,b;

def take_data_time(y,z,d_step,dbt,cols,dat_array,a,b,var,sensmod):            

    time.sleep(d_step)
    mag = dsp7265.query(dbt)
    #split apart and store recorded data
    data = mag.split('\r\n')
    dat_array[z][0] = time.time()
    for x in range(1,cols-1):
        dat_array[z][x] = int(data[x-1])      
    a[z] = dat_array[z][0]
    b[z] = dat_array[z][var]*sensmod  
    time.sleep(0.002)            
    return dat_array,a,b; 


def plotter(a,b,sweepplot):
    sweepplot.plot(a,b,clear=True)
    return;  
#Designed to sweep anything 
# max and min are as suspected
#sweep_item is the variable you are sweeping (ex. OA for output amplitude)

#dtbt is a string of the GPIB commands to measure the variables
# you are interested in

#dtbt_num is the number of variables for forming an array of the desired output

#Be careful with timing step, 1 second seems long enough, but may sometimes
#be too long

#Pre factor on voltage data is from

def sr_sweep(sweep_max,sweep_min,steps,sweep_item,dtbt,dtbt_num,xvar,yvar,sensmod):

    dsp7265.write(sweep_item+str(sweep_min))
    d_sweep = abs(sweep_max-sweep_min)/steps
    if xvar<4:
        total_steps = steps*2+1 
    else:
        total_steps = steps+2
    print(total_steps) 
    print(xvar)

    cols=dtbt_num+1
    print(sensmod)
    data_array = np.zeros([total_steps,cols],float)
    x = np.zeros(total_steps,float)
    y = np.zeros(total_steps,float)
    i=0
    j=i
    amp = sweep_min
#    col_headings = dtbt.split(';')
#    print(col_headings)
#    for l in range(0,dtbt_num+1):
#        data_array[0][l] = col_headings[l]

    sweepplot = pg.plot(title="Three plot curves")
    sweepplot.plot(x[0:2],y[0:2])
    pg.QtGui.QApplication.processEvents()
    time.sleep(1)
    #Do sweep
    if xvar<4:
        while (i<steps):
            t1 = threading.Thread(target = take_data,args=(i,j,amp,sweep_item,dtbt,cols,data_array,x,y,yvar,sensmod))
            
            t2 = threading.Thread(target = plotter,args=(x[0:j],y[0:j],sweepplot))
            
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()

            pg.QtGui.QApplication.processEvents()
            time.sleep(0.002)
            amp = amp + d_sweep

            i = i+1
            j=i
            
        pg.QtGui.QApplication.processEvents()
        while (i>=0):        
            t1 = threading.Thread(target = take_data,args=(i,j,amp,sweep_item,dtbt,cols,data_array,x,y,yvar,sensmod))
            t2 = threading.Thread(target = plotter,args=(x[0:j],y[0:j],sweepplot))
            
            t1.start()
            t2.start()
            
            t1.join()
            t2.join()
            
            pg.QtGui.QApplication.processEvents()
            time.sleep(0.002)
            amp = amp - d_sweep
            i = i-1
            j=j+1
    
    
    #This loop is for time measurements
    else:
        while (j<steps):
            t1 = threading.Thread(target = take_data_time,args=(j,j,d_sweep,dtbt,cols,data_array,x,y,yvar,sensmod))

            t2 = threading.Thread(target = plotter,args=(x[0:j],y[0:j],sweepplot))

            t1.start()
            t2.start()
            
            t1.join()
            t2.join()            
            
            pg.QtGui.QApplication.processEvents()
            time.sleep(0.002)
            j = j+1
            
            
    return data_array;
        
    