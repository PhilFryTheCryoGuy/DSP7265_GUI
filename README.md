# DSP7265_GUI
Control software for Signal Recovery DSP 7265 Lock-in Amplifier
Currently works with National Instruments GPIB-USB-HS usb module

Dependencies are:
-pyvisa 
-pyqt5
-numpy
-pyqtgraph

The exported data(X,Y, and MAG) are not scaled, only the plotted data.
To scale the data you must divide by 10000 and then multiply by the sensitivity used. 
The reason for this factor is that the data as read from the lock-in is scaled to 10000 where 10000 is the sensitivity level. The lock in will however output values up to 30000 in relation to the 10000(see DSP 7265 manual GPIB command descriptions).

MIT License

Copyright (c) 2017 J T M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
