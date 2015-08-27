#----------------------------------------------------------------------------
# SCRIPT TO PROCESS RAW .CSV FILES EXPORTED FROM ISOTECH OSCILLSCOPE, CREATES TRACE PLOTS FOR BOTH TIMEBREAK AND HYDRO CHANNELS
# ----------------------------------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import wx


#-----------------------------IMPORTING CHANNEL 1 TIMEBREAK DATA----------------------------------------------------------#

#Promt user to select scope trace for analysis
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, "Choose Channel 1 Data File", wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

traceC1 = get_path('*.csv')


#parse in the scope csv data file, skip header and use first column for data.
ds = np.genfromtxt(traceC1,delimiter=',', dtype = float, skip_header=14, usecols=0)

#adjust voltages for scale (channel 1 = 5V), in this case multiply by 1/5 = 0.2, see header file for scale.
dataC1 = ds * 0.2




#-----------------------------IMPORTING CHANNEL 2 HYDROPHONE DATA----------------------------------------------------------#

#Promt user to select scope trace for analysis
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, "Choose Channel 2 Data File", wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

traceC2 = get_path('*.csv')


#parse in the scope csv data file, skip header and use first column for data.
ds = np.genfromtxt(traceC2,delimiter=',', dtype = float, skip_header=14, usecols=0)

#adjust voltages for scale (channel 2 = 0.02), in this case multiply by 1/0.002 = 50, see header file for scale.
dataC2 = ds * 0.002


#-----------------------------RESHAPING AND TIMESTAMPING DATA INTO A 2D ARRAY----------------------------------------------------------#

# create a 1d time array and reshape to 1d vertical column
ts = np.linspace(0.00000, 0.01996, num=500)
ts2 = ts.reshape((500,1))

#rearrange Channel 1 and 2 array to 1D vertical column

dataC1_2 = dataC1.reshape((500,1))
dataC2_2 = dataC2.reshape((500,1))

#merge to 2 verical time and data columns
dataframeC1 = np.hstack((ts2,dataC1_2))
dataframeC2 = np.hstack((ts2,dataC2_2))



#-------------------------MAX AND MIN VALUES IN TRACE DATA SET-----------------------------------------------------------------------#

#find max C1 Max
C1_max_v = dataC1.max()
C2_max_v = dataC2.max()

#-------------------------CHANNEL 2 HYDROPHONE POSTIVE BREAK-----------------------------------------------------------------------#

#locates the first value in the data set thats is greater than 0.0005
pos_brk = (np.argmax(dataC2_2 > 15))

#convert from numpy array to list
pb = dataframeC2[pos_brk].tolist()

#select first number in list
pb_time = pb[0]


#------------------------------CHANNEL 1 TIMEBREAK POSITIVE PEAK-------------------------------------------------------------------#

#find index of maximum value in 1st colum (only column in this case)
C1_pp = (dataC1_2.argmax(axis=0))

#select timestamp max value and convert from numpy array to list
C1_ppk = dataframeC1[C1_pp].tolist()
C1_pp_timez = C1_ppk[0]

#select first number in list
C1_pp_time = C1_pp_timez[0]


#------------------------------CHANNEL 2 HYDROPHONE POSITIVE PEAK-------------------------------------------------------------------#

#find index of maximum value in 1st colum (only column in this case)
C2_pp = (dataC2_2.argmax(axis=0))

#select timestamp max value and convert from numpy array to list
C2_ppk = dataframeC2[C2_pp].tolist()
C2_pp_timez = C2_ppk[0]

#select first number in list
C2_pp_time = C2_pp_timez[0]








#----------------------------------------GRAPH STUFF---------------------------------------------------#



#Set up your x-axis timeseries data, 500 samples @ 0.00004 second/sample
timestamp = np.linspace(0.00000, 0.01996, num=500)


#plot columns to axis
time = [row for row in timestamp]
voltageC1 = [row for row in dataC1]
voltageC2 = [row for row in dataC2]



plt.figure(1)

#REF sub plot
plt.subplot(211)
plt.plot(time,voltageC1,'y',lw=1.3)
plt.ylabel('Voltage (V)')
plt.title('Scope: Timebreak')
plt.grid(True)
#plt.text(0.0002, 100, "Max V = " + str(C1_max_v) + "V")
#plt.text(0.0002, 80, "+ve Peak = " + str(C1_pp_time) + "s")

#TRACE sub plot
plt.subplot(212)
plt.plot(time,voltageC2,'g',lw=1.3)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Scope: Hydrophone')
plt.grid(True)

#plt.text(0.0003, 50, "+ve Break = " + str(pb_time) + "s")
#plt.text(0.0003, 40, "+ve Peak = " + str(C2_pp_time) + "s")

plt.show()



