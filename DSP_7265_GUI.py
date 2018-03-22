# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:41:07 2017
Last edited on Thursday July 13 2017
@author: JT
Made using help from PyQt5 tutorials by ZetCode.com
"""

import visa
import sys
import numpy as np
import threading 

import time
from PyQt5.QtWidgets import (QWidget, QLabel,QCheckBox, QApplication,QComboBox
                             ,QPushButton,QLineEdit)

                                                
from SweepCode import sr_sweep
#from FakeSweep import fake_sweep
rm = visa.ResourceManager()
rm.list_resources()
dsp7265 = rm.open_resource("GPIB::12::INSTR")

#Defintions for writing values to the lock in from the main panel and for exiting
def exiter():
    dsp7265.write('DAC 2 0;DAC 1 0;OA 0')    
def write_rvf(a,b):
    dsp7265.write('OA '+a+';OF '+b)
def write_dac(a,b):
    dsp7265.write('DAC '+a+' '+b)
def write_autophase():
    dsp7265.write('AQN')
    
     
#Sets the second variable for line frequency automattically for 50Hz

class main(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):   
        
           
        
        #Dropdown box for lock-in mode 
        self.lbl = QLabel("Input Mode", self)
        self.lbl.move(140, 10)
        self.inputMODE = QComboBox(self)
        self.inputMODE.addItem("A(Single-Ended Voltage")
        self.inputMODE.addItem("-B(Inverting Single Ended Voltage)")
        self.inputMODE.addItem("A-B (Differential Voltage)")
        self.inputMODE.addItem("B Current input - High")
        self.inputMODE.addItem("B Current input - Low Noise")
        self.inputMODE.addItem("Inputs Grounded (test)")
        self.inputMODE.move(140, 25)        
        self.inputMODE.currentIndexChanged.connect(self.onActivated)
        
        #Dropdown box for connector shells  
        self.shelllbl = QLabel("Input Connector Shells", self)
        self.shelllbl.move(140, 60)
        inputLINE = QComboBox(self)
        inputLINE.addItem("Ground")
        inputLINE.addItem("Float")
        inputLINE.move(140, 75)
        inputLINE.currentIndexChanged.connect(self.lineSHELL)

        #Dropdown box for coupling 
        self.csetlbl = QLabel("Input Connector Shells", self)
        self.csetlbl.move(140, 110)
        coupling = QComboBox(self)
        coupling.addItem("AC")
        coupling.addItem("DC")
        coupling.move(140, 125)
        coupling.currentIndexChanged.connect(self.coupleSET)
        
        #Dropdown box for Input Device
        self.isetlbl = QLabel("Input Coupling", self)
        self.isetlbl.move(140, 160)
        inputDEV = QComboBox(self)
        inputDEV.addItem("Bipolar - 10k Impedance")
        inputDEV.addItem("FET - 10M Impedance")        
        inputDEV.move(140, 175)
        inputDEV.currentIndexChanged.connect(self.inputSET)
        
        #Dropdown box for Input Device
        self.lflbl = QLabel("Line Frequency", self)
        self.lflbl.move(140, 210)
        self.lf = QComboBox(self)
        self.lf.addItem("50 Hz")
        self.lf.addItem("60 Hz")        
        self.lf.move(140, 225)
        self.lf.currentIndexChanged.connect(self.lfSET)
        
        #Dropdown box for Line Frequency Rejection Filter
        self.lfrflbl = QLabel("Line Frequency Rejection Filter", self)
        self.lfrflbl.move(140, 260)
        self.lfrf = QComboBox(self)
        self.lfrf.addItem("Off")
        self.lfrf.addItem("F")
        self.lfrf.addItem("2F")
        self.lfrf.addItem("F & 2F")          
        self.lfrf.move(140, 275)
        self.lfrf.currentIndexChanged.connect(self.lfrfSET)
        
        #Dropdown box for auto ac gain
        self.gainautolbl = QLabel("Auto AC Gain", self)
        self.gainautolbl.move(140, 310)
        gainauto = QComboBox(self)
        gainauto.addItem("Off")
        gainauto.addItem("On")
        gainauto.move(140, 325)
        gainauto.currentIndexChanged.connect(self.gainautoSET)
        
        #Dropdown box for ac gain
        self.acgainlbl = QLabel("AC Gain", self)
        self.acgainlbl.move(140, 360)
        acgain = QComboBox(self)
        acgain.addItem("0 dB")
        acgain.addItem("10 dB")
        acgain.addItem("20 dB")
        acgain.addItem("30 dB")
        acgain.addItem("40 dB")
        acgain.addItem("50 dB")
        acgain.addItem("60 dB")
        acgain.addItem("70 dB")
        acgain.addItem("80 dB")
        acgain.addItem("90 dB")
        acgain.move(140, 375)
        acgain.currentIndexChanged.connect(self.acgainSET)
        
        
        
        
        
        #Dropdown for sensitivity
        self.senlbl = QLabel("Sensitivity", self)
        self.senlbl.move(360, 10)
        self.sensitivity = QComboBox(self)
        self.sensitivity.addItem("1-2nV/2fA/NA")
        self.sensitivity.addItem("2-5nV/5fA/NA")
        self.sensitivity.addItem("3-10nV/10fA/NA")
        self.sensitivity.addItem("4-20nV/20fA/NA")
        self.sensitivity.addItem("5-50nV/50fA/NA")
        self.sensitivity.addItem("6-100nV/100fA/NA")
        self.sensitivity.addItem("7-200nV/200fA/2fA")
        self.sensitivity.addItem("8-500nV/500fA/5fA")
        self.sensitivity.addItem("9-1"+chr(956)+"V/1pA/10fA")
        self.sensitivity.addItem("10-2"+chr(956)+"V/2pA/20fA")
        self.sensitivity.addItem("11-5"+chr(956)+"V/5pA/50fA")
        self.sensitivity.addItem("12-10"+chr(956)+"V/10pA/100fA")
        self.sensitivity.addItem("13-20"+chr(956)+"V/20pA/200fA")
        self.sensitivity.addItem("14-50"+chr(956)+"V/50pA/500fA")
        self.sensitivity.addItem("15-100"+chr(956)+"V/100pA/1pA")
        self.sensitivity.addItem("16-200"+chr(956)+"V/200pA/2pA")
        self.sensitivity.addItem("17-500"+chr(956)+"V/500pA/5pA")
        self.sensitivity.addItem("18-1mV/1nA/10pA")
        self.sensitivity.addItem("19-2mV/2nA/20pA")
        self.sensitivity.addItem("20-5mV/5nA/50pA")
        self.sensitivity.addItem("21-10mV/10nA/100pA")
        self.sensitivity.addItem("22-20mV/20nA/200pA")
        self.sensitivity.addItem("23-50mV/50nA/500pA")
        self.sensitivity.addItem("24-100mV/100nA/1nA")
        self.sensitivity.addItem("25-200mV/200nA/2nA")
        self.sensitivity.addItem("26-500mV/500nA/5nA")
        self.sensitivity.addItem("27-1V/1"+chr(956)+"A/10nA")
        self.sensitivity.move(360, 25)
        self.sensitivity.currentIndexChanged.connect(self.sens)
        #Button activates auto sensitivity function
        self.autosens = QPushButton('Auto Sens.', self)
        self.autosens.setCheckable(True)
        self.autosens.move(360, 60)
        self.autosens.clicked[bool].connect(self.autosensON)
        #Button activates auto sensitivity function
        self.automeas = QPushButton('Auto Meas.', self)
        self.automeas.setCheckable(True)
        self.automeas.move(360, 90)
        self.automeas.clicked[bool].connect(self.automeasON)
        
        
        #Dropdown box for time constant
        self.tclbl = QLabel("Time Constant", self)
        self.tclbl.move(550, 10)
        timeCONSTANT = QComboBox(self)
        timeCONSTANT.addItem("10 "+chr(956)+"s")
        timeCONSTANT.addItem("20 "+chr(956)+"s")
        timeCONSTANT.addItem("40 "+chr(956)+"s")
        timeCONSTANT.addItem("80 "+chr(956)+"s")
        timeCONSTANT.addItem("160 "+chr(956)+"s")
        timeCONSTANT.addItem("320 "+chr(956)+"s")
        timeCONSTANT.addItem("640 "+chr(956)+"s")
        timeCONSTANT.addItem("5 ms")
        timeCONSTANT.addItem("10 ms")
        timeCONSTANT.addItem("20 ms")
        timeCONSTANT.addItem("50 ms")
        timeCONSTANT.addItem("100 ms")
        timeCONSTANT.addItem("200 ms")
        timeCONSTANT.addItem("500 ms")
        timeCONSTANT.addItem("1 s")
        timeCONSTANT.addItem("2 s")
        timeCONSTANT.addItem("5 s")
        timeCONSTANT.addItem("10 s")
        timeCONSTANT.addItem("20 s")
        timeCONSTANT.addItem("50 s")
        timeCONSTANT.addItem("100 s")
        timeCONSTANT.addItem("200 s")
        timeCONSTANT.addItem("500 s")
        timeCONSTANT.addItem("1 ks")
        timeCONSTANT.addItem("2 ks")
        timeCONSTANT.addItem("5 ks")
        timeCONSTANT.addItem("10 ks")
        timeCONSTANT.addItem("20 ks")
        timeCONSTANT.addItem("50 ks")
        timeCONSTANT.move(550, 25)
        timeCONSTANT.currentIndexChanged.connect(self.tc)
        
        #Dropdown box for output slope
        self.slopelbl = QLabel("Slope", self)
        self.slopelbl.move(550, 60)
        slope = QComboBox(self)
        slope.addItem("6 dB/Octave")
        slope.addItem("12 dB/Octave")
        slope.addItem("18 dB/Octave")
        slope.addItem("24 dB/Octave")
        slope.move(550, 75)
        slope.currentIndexChanged.connect(self.slopeSET)
        
        #Dropdown box for output slope
        self.tcsynclbl = QLabel("Slope", self)
        self.tcsynclbl.move(550, 110)
        tcsync = QComboBox(self)
        tcsync.addItem("Off")
        tcsync.addItem("On")
        tcsync.move(550, 125)
        tcsync.currentIndexChanged.connect(self.tcsyncSET)
        
        #Dropdown box for plot Y
        self.yplotlbl = QLabel("Y-Axis Plot", self)
        self.yplotlbl.move(550, 175)
        self.yplot = QComboBox(self)
        self.yplot.addItem("X Output")
        self.yplot.addItem("Magnitude Output")
        self.yplot.addItem("Phase")
        self.yplot.addItem("ADC 1")
        self.yplot.addItem("ADC 2")
        self.yplot.move(550, 190)
        self.yplot.currentIndexChanged.connect(self.ypt)   
        
                        #Dropdown box for what to measure
                
        # Default is bias voltage
        self.sweepvarlbl = QLabel("Sweep Variable", self)
        self.sweepvarlbl.move(370, 150)
        self.sweepvar = QComboBox(self)
        self.sweepvar.addItem("Bias Voltage(microvolts)")
        self.sweepvar.addItem("Frequency(mHz)")
        self.sweepvar.addItem("DAC 1 (mV)")
        self.sweepvar.addItem("DAC 2 (mV)")
        self.sweepvar.addItem("Time (s)")            
        self.sweepvar.move(370, 165)
        self.sweepvar.currentIndexChanged.connect(self.sweepvarSET)
        
        # Text Box for max value
        self.maxlbl = QLabel("Max Sweep Value", self)
        self.maxlbl.move(370, 200)
        self.max_val = QLineEdit(self)
        self.max_val.move(370, 215)
        # Text Box for min sweep value
        self.minlbl = QLabel("Min Sweep Value", self)
        self.minlbl.move(370, 250)
        self.min_val = QLineEdit(self)
        self.min_val.move(370, 265)
        # Text Box for number of points
        self.points = QLabel("Points", self)
        self.points.move(370, 295)
        self.points = QLineEdit(self)
        self.points.move(370, 315)
        # Text box for file name
        self.fnlbl = QLabel("Enter file name", self)
        self.fnlbl.move(370, 350)
        self.fname = QLineEdit(self)
        self.fname.move(370, 365)
        
        
        #Button activates a sweep
        self.sweep = QPushButton('Start Sweep', self)
        self.sweep.setCheckable(True)
        self.sweep.move(370,395)
        self.sweep.clicked[bool].connect(self.sweepON)
        
        
        
        # Text Box for current reference voltage
        self.refVlbl = QLabel("Reference Voltage (microvolts)", self)
        self.refVlbl.move(700, 20)
        self.refV_val = QLineEdit(self)
        self.refV_val.move(700, 35)
        
        # Text Box for current reference frequency
        self.refFlbl = QLabel("Reference Frequency (mHz)", self)
        self.refFlbl.move(700, 65)
        self.refF_val = QLineEdit(self)
        self.refF_val.move(700, 80)
        
        #Button sets the reference phase and voltage
        self.setRefVF = QPushButton('Set Reference', self)
        self.setRefVF.setCheckable(True)
        self.setRefVF.move(700, 110)
        self.setRefVF.clicked[bool].connect(self.setRefVFON)
        
        #Button activates auto phase
        self.autophase = QPushButton('Auto Phase', self)
        self.autophase.setCheckable(True)
        self.autophase.move(700, 150)
        self.autophase.clicked[bool].connect(self.autophaseON)
        


        # Text Box for DAC 1
        self.dac1lbl = QLabel("DAC 1 Voltage (microvolts)", self)
        self.dac1lbl.move(700, 220)
        self.dac1_val = QLineEdit(self)
        self.dac1_val.move(700, 235)
        

        #Button sets DAC 1
        self.setdac1 = QPushButton('Set DAC 1', self)
        self.setdac1.setCheckable(True)
        self.setdac1.move(700, 255)
        self.setdac1.clicked[bool].connect(self.setdac1ON)
        
                # Text Box for DAC 2
        self.dac2lbl = QLabel("DAC 2 Voltage (microvolts)", self)
        self.dac2lbl.move(700, 305)
        self.dac2_val = QLineEdit(self)
        self.dac2_val.move(700, 320)
        
        #Button sets DAC 2
        self.setdac2 = QPushButton('Set DAC 2', self)
        self.setdac2.setCheckable(True)
        self.setdac2.move(700, 345)
        self.setdac2.clicked[bool].connect(self.setdac2ON)         
        
        #Button Exits software sets all outputs to zero
        self.exitlbl = QPushButton('Exit', self)
        self.exitlbl.setCheckable(True)
        self.exitlbl.move(700, 405)
        self.exitlbl.clicked[bool].connect(self.exit_prog) 
        
        #Button to uncheck all sweep monitor boxes
#        self.Uncheck = QPushButton('Uncheck All', self)
#        self.Uncheck.setCheckable(True)
#        self.Uncheck.move(20, 340)
#        self.Uncheck.clicked[bool].connect(self.UncheckAll)
        
        #Checkboxes for what channels to monitor when sweeping
        self.cb = QCheckBox('X Output', self)
        self.cb.move(20, 20)
        self.cb.toggle()

        
        self.cb2 = QCheckBox('Y Output', self)
        self.cb2.move(20, 40)
        self.cb2.toggle()

        
        self.cb3 = QCheckBox('Magnitude Output', self)
        self.cb3.move(20, 60)
        self.cb3.toggle()

        
        self.cb4 = QCheckBox('Phase', self)
        self.cb4.move(20, 80)
        self.cb4.toggle()

        
        self.cb5 = QCheckBox('Sensitivity', self)
        self.cb5.move(20, 100)
        self.cb5.toggle()

        
        self.cb6 = QCheckBox('ADC1', self)
        self.cb6.move(20, 120)
        self.cb6.toggle()

        
        self.cb7 = QCheckBox('ADC2', self)
        self.cb7.move(20, 140)
        self.cb7.toggle()

        
        self.cb8 = QCheckBox('ADC3', self)
        self.cb8.move(20, 160)
        self.cb8.toggle()

        
        self.cb9 = QCheckBox('DAC1', self)
        self.cb9.move(20, 180)
        self.cb9.toggle()

        
        self.cb10 = QCheckBox('DAC2', self)
        self.cb10.move(20, 200)
        self.cb10.toggle()

        
        self.cb11 = QCheckBox('Noise', self)
        self.cb11.move(20, 220)
        self.cb11.toggle()

        
        self.cb12 = QCheckBox('Ratio', self)
        self.cb12.move(20, 240)
        self.cb12.toggle()

        
        self.cb13 = QCheckBox('Log Ratio', self)
        self.cb13.move(20, 260)
        self.cb13.toggle()

        
        self.cb14 = QCheckBox('Event Var.', self)
        self.cb14.move(20, 280)
        self.cb14.toggle()

        
        self.cb15 = QCheckBox('Ref. FREQ', self)
        self.cb15.move(20, 300)
        self.cb15.toggle()
        
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()
    
    
            
    #Definition for lock-in mode list
    def onActivated(self,i):
#       self.lbl.setText(str(i))
       if (i==0):
           dsp7265.write('IMODE0;VMODE1')
       elif (i==1):  
           dsp7265.write('IMODE0;VMODE2')
       elif (i==2):
           dsp7265.write('IMODE0;VMODE3')
       elif (i==3):  
           dsp7265.write('IMODE1')
       elif (i==4):
           dsp7265.write('IMODE2')
       elif (i==5):  
           dsp7265.write('IMODE0;VMODE0')
       else:
           self.lbl.setText('Mode Setting Failed') 

    #Definition for setting line grounding  
    def lineSHELL(self,i):
#       self.shelllbl.setText('FET'+str(i))
       dsp7265.write('FET'+str(i))
    #Sets input impedance
    def inputSET(self,i):
#       self.isetlbl.setText('FLOAT'+str(i))
       dsp7265.write('FLOAT'+str(i+1))
    #Sets AC or DC coupling
    def coupleSET(self,i):
#       self.csetlbl.setText('CP'+str(i))
      dsp7265.write('CP'+str(i))

    #Definitions for setting line frequency rejection filter
    def lfSET(self,i):
#       self.lflbl.setText(str(self.lf.currentIndex()))
       self.lfrflbl.setText('LF '+str(self.lfrf.currentIndex())+" "+str(self.lf.currentIndex()))       
       dsp7265.write('LF '+str(self.lfrf.currentIndex())+" "+str(self.lf.currentIndex()))
       
    def lfrfSET(self,i):
#       self.lfrflbl.setText('LF '+str(i)+" "+str(self.lf.currentIndex()))
       dsp7265.write('LF '+str(i)+" "+str(self.lf.currentIndex()))

    #Definitions for setting ac auto gain
    def gainautoSET(self,i):
#       self.gainautolbl.setText('AUTOMATIC'+str(i))
       dsp7265.write('AUTOMATIC'+str(i))
    def acgainSET(self,i):
#       self.acgainlbl.setText('ACGAIN'+str(i*10))
       dsp7265.write('ACGAIN'+str(i*10))


    def sens(self,i):
#       self.senlbl.setText('SEN'+str(i+1))
       dsp7265.write('SEN'+str(i+1))
    #Button activates auto sensitivity calibration then unpresses the button    
    def autosensON(self,pressed):
       if pressed:
           dsp7265.write('AS')
           time.sleep(20)
           rsensvalue = dsp7265.query('SEN')
           sensvalue = rsensvalue.split('\r\n')
           self.sensitivity.setCurrentIndex(int(sensvalue[0]))
           self.autosens.setChecked(False)
    #Button activates auto sensitivity calibration then unpresses the button    
    def automeasON(self,pressed):
       if pressed:
           dsp7265.write('ASM')
           time.sleep(20)
           rsensvalue = dsp7265.query('SEN')
           sensvalue = rsensvalue.split('\r\n')
           self.sensitivity.setCurrentIndex(int(sensvalue[0]))
           self.automeas.setChecked(False)
           
    def sweepvarSET(self,i):
       self.sweepvarlbl.setText(str(i))
      
    #Controls sweeping
    
    def sweepON(self,pressed):
       if pressed:
           measure_value = ''
           sweep_value = ''
           dtbt_cols = 0
           y_plot_var = 0
           if self.cb.isChecked():
               measure_value = measure_value + 'X '
               dtbt_cols=dtbt_cols+1
               if self.yplot.currentIndex() == 0:
                   y_plot_var = dtbt_cols
           if self.cb2.isChecked():
               measure_value = measure_value + ';Y '
               dtbt_cols=dtbt_cols+1
           if self.cb3.isChecked():
               measure_value = measure_value + ';MAG '
               dtbt_cols=dtbt_cols+1
               if self.yplot.currentIndex() == 1:
                   y_plot_var = dtbt_cols
           if self.cb4.isChecked():
               measure_value = measure_value + ';PHA '
               dtbt_cols=dtbt_cols+1
               if self.yplot.currentIndex() == 2:
                   y_plot_var = dtbt_cols
                   
           if self.cb5.isChecked():
               measure_value = measure_value + ';SEN '
               dtbt_cols=dtbt_cols+1
               
           if self.cb6.isChecked():
               measure_value = measure_value + ';ADC1 '
               dtbt_cols=dtbt_cols+1               
               if self.yplot.currentIndex() == 3:
                   y_plot_var = dtbt_cols  
                   
           if self.cb7.isChecked():
               measure_value = measure_value + ';ADC2 '
               dtbt_cols=dtbt_cols+1
               if self.yplot.currentIndex() == 4:
                   y_plot_var = dtbt_cols               
           if self.cb8.isChecked():
               measure_value = measure_value + ';ADC3 '
               dtbt_cols=dtbt_cols+1
           if self.cb9.isChecked():
               measure_value = measure_value + ';DAC1 '
               dtbt_cols=dtbt_cols+1
           if self.cb10.isChecked():
               measure_value = measure_value + ';DAC2 '
               dtbt_cols=dtbt_cols+1
           if self.cb11.isChecked():
               measure_value = measure_value + ';NN '
               dtbt_cols=dtbt_cols+1
           if self.cb12.isChecked():
               measure_value = measure_value + ';RT '
               dtbt_cols=dtbt_cols+1
           if self.cb13.isChecked():
               measure_value = measure_value + ';LR '
               dtbt_cols=dtbt_cols+1
           if self.cb14.isChecked():
               measure_value = measure_value + ';ENBW '
               dtbt_cols=dtbt_cols+1
           if self.cb15.isChecked():
               measure_value = measure_value + ';FRQ '
               dtbt_cols=dtbt_cols+1
           print(measure_value)
           
           #What you want to sweep
           if self.sweepvar.currentIndex() == 0:
               sweep_value = 'OA '
               x_var = 0
           elif self.sweepvar.currentIndex() == 1:
               sweep_value = 'OF '
               x_var = 1
           elif self.sweepvar.currentIndex() == 2:
              sweep_value = 'DAC 1 '
              x_var = 2
           elif self.sweepvar.currentIndex() == 3:
               sweep_value = 'DAC 2 '
               x_var = 3
           else:
               sweep_value = 'TIME '
               x_var = 4
           print(sweep_value)
           
           #calculate modifiers for sensitivity setting
           sens_index = self.sensitivity.currentIndex()
           #first check for multiplier of 2, 5, or 10
           if((sens_index%3) == 1):
               modifier_1 = 5
           elif((sens_index%3) == 2):
               modifier_1 = 10
           else:
               modifier_1 = 2

            # check for the input mode and add appropriate modifier  
           imode_index =  self.inputMODE.currentIndex()
           if(imode_index == 3):
               modifier_2 = 1000000
           elif(imode_index == 4):
               modifier_2 = 100000000
           else:
               modifier_2 = 1
               
           #Check for order of magnitude
           if(sens_index<3):
               modifier_3 = 1e-9
           elif(sens_index<6):
               modifier_3 = 1e-8
           elif(sens_index<9):
               modifier_3 = 1e-7
           elif(sens_index<12):
               modifier_3 = 1e-6
           elif(sens_index<15):
               modifier_3 = 1e-5
           elif(sens_index<18):
               modifier_3 = 1e-4
           elif(sens_index<21):
               modifier_3 = 1e-3           
           elif(sens_index<24):
               modifier_3 = 1e-2               
           else:
               modifier_1 = 1e-1            
            
           sens_mod = modifier_3*modifier_1/(10000*modifier_2)
           
           #Actually do the sweep
           data = sr_sweep(int(self.max_val.text()),int(self.min_val.text()),
                           int(self.points.text()),sweep_value,measure_value,dtbt_cols,x_var,y_plot_var,sens_mod)
           #data = np.zeros((4,16))
           np.savetxt(self.fname.text(), data, delimiter=",")

#           dats = fake_sweep(int(self.points.text()))
           
           self.sweep.setChecked(False)
           
    #The check box definitions, on(1) means measure, off(0) means ignore  
    

    def tc(self,i):
#       self.tclbl.setText('TC'+str(i))
       dsp7265.write('TC'+str(i))       
    def slopeSET(self,i):
#       self.slopelbl.setText('SLOPE'+str(i))
       dsp7265.write('SLOPE'+str(i))
    def tcsyncSET(self,i):
#       self.tcsynclbl.setText('SYNC'+str(i))
       dsp7265.write('SYNC'+str(i))

    def ypt(self,i):   
        self.yplotlbl.setText('ypt'+str(i))
    #Reference channel settings
    def setRefVFON(self,pressed):
       if pressed:
           t2 = threading.Thread(target = write_rvf,args=(self.refV_val.text(),self.refF_val.text()))            
           t2.start()            
           t2.join()           
           #dsp7265.write('OA '+self.refV_val.text()+';OF '+self.refF_val.text())
           time.sleep(3)
#           self.refVlbl.setText(self.refV_val.text())
           self.setRefVF.setChecked(False)  
           
    def autophaseON(self,pressed):
       if pressed:
           t2 = threading.Thread(target = write_autophase)
           t2.start()
           t2.join()
           time.sleep(10)
           self.automeas.setChecked(False)

    #DAC 1 set
    def setdac1ON(self,pressed):
       if pressed:
           j="1"
           t2 = threading.Thread(target = write_rvf,args=(j,self.dac1_val.text()))            
           t2.start()            
           t2.join()            
           dsp7265.write('DAC 1 '+self.dac1_val.text())
           time.sleep(3)
#           self.refVlbl.setText(self.refV_val.text())
           self.setdac1.setChecked(False)

    #DAC 2 set
    def setdac2ON(self,pressed):
       if pressed:
           j="2"
           t2 = threading.Thread(target = write_rvf,args=(j,self.dac2_val.text()))            
           t2.start()            
           t2.join() 
           dsp7265.write('DAC 2 '+self.dac2_val.text())
           time.sleep(3)
#           self.refVlbl.setText(self.refV_val.text())
           self.setdac2.setChecked(False)
           
    #Exit prog
    def exit_prog(self,pressed):
       if pressed:
           
           t2 = threading.Thread(target = exiter)            
           t2.start()            
           t2.join()
           #dsp7265.write('DAC 2 0;DAC 1 0;OA 0')
#           time.sleep(3)
#           self.refVlbl.setText(self.refV_val.text())
           sys.exit(app.exec_())
           self.exitlbl.setChecked(False)           


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    window = main()
    window.resize(900, 450)
    window.setWindowTitle('DSP 7265')
    sys.exit(app.exec_())