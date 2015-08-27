#----------------------------------------------------------------------------
# SCRIPT TO PROCESS RAW TRACE and REF CSV FILES EXPORTED FROM VS PROWESS, CREATES 2 SUBPLOTS OF REF and TRACE. GIVES THE FOLLOWING INFORMATION
# REF POSITIVE PEAK (TIMEBREAK), MAGNITUDE AND TIME
# TRACE POSTIVE BREAK (FIRST VALUE GREATER THAN 500MICROVOLT), TIME
# TRACE POSIIVE PEAK (MAXIUM POSITIVE VALUE), MAGNITUDE, TIME
# TRACE NEGATIVE PEAK (MINIUM NEGATIVE VALUE), MAGNITUDE
# ----------------------------------------------------------------------------------------------------------

import os
import os.path
import csv
import numpy as np
import matplotlib.pyplot as plt
import wx
from datetime import datetime

#-----------------------------IMPORTING TRACE DATA----------------------------------------------------------#

#Prompt user to select trace
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Select TRACE file to open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

trace = get_path('*.csv')

#parse csv file into numpy format, both columns, 2D array
trace_data = np.genfromtxt(trace,delimiter=',', dtype = float, skip_header=2)

#parse only 2nd column of csv file, skip 2 header lines, 1D scalar dataset
trace_data2 = np.genfromtxt(trace,delimiter=',', dtype = float, skip_header=2, usecols=1)


#-----------------------------IMPORTING REF DATA----------------------------------------------------------#

#Prompt user to select ref
def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
    dialog = wx.FileDialog(None, 'Select REF file to open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

ref = get_path('*.csv')

#parse csv file into numpy format, both columns, 2D array
ref_data = np.genfromtxt(ref,delimiter=',', dtype = float, skip_header=2)

#parse only 2nd column of csv file, skip 2 header lines, 1D scalar dataset
ref_data2 = np.genfromtxt(ref,delimiter=',', dtype = float, skip_header=2, usecols=1)




#-------------------------MAX AND MIN VALUES IN TRACE DATA SET-----------------------------------------------------------------------#

#find max and min voltages
max_v = trace_data2.max()
min_v = trace_data2.min()
max_mv = max_v * 1000
min_mv = min_v * 1000


#-------------------------MAX AND MIN VALUES IN REF DATA SET-----------------------------------------------------------------------#

#find max and min voltages
ref_max_v = ref_data2.max()
ref_min_v = ref_data2.min()


#-------------------------TRACE POSTIVE BREAK-----------------------------------------------------------------------#

#locates the first value in the data set thats is greater than 0.0005
pos_brk = (np.argmax(trace_data2 > 0.0005))

#convert from numpy array to list
pb = trace_data[pos_brk].tolist()

#select first number in list
pb_time = pb[0]


#------------------------------TRACE POSITIVE PEAK-------------------------------------------------------------------#

#find index of maximum value in 1st colum (only column in this case)
pp = (trace_data2.argmax(axis=0))

#select timestamp max value and convert from numpy array to list
ppk = trace_data[pp].tolist()

#select first number in list
pp_time = ppk[0]


#------------------------------REF POSITIVE PEAK-------------------------------------------------------------------#

#find index of maximum value in 1st colum (only column in this case)
pp_ref = (ref_data2.argmax(axis=0))

#select timestamp max value and convert from numpy array to list
ppk_ref = ref_data[pp_ref].tolist()

#select first number in list
pp_time_ref = ppk_ref[0]



#------------------------------RELATIVE TRAVEL TIMES-------------------------------------------------------------------#

#calculate the time difference between the positive BREAK and ref positive peak (timebreak) (millisecond)
t_pb_tx = (pb_time - pp_time_ref) * 1000

#calculate the time difference between the positive PEAK and ref positive PEAK (timebreak) (milliseconds)
t_pp_tx = (pp_time - pp_time_ref) * 1000

#calculates time differnece between positive BREAK and positive PEAK (milliseconds)
dif_pb_pp = (t_pp_tx - t_pb_tx)


#----------------------------------------LOG FILE STUFF---------------------------------------------------#

#find the orignal csv name and pull out the filename, split the file name from the path
thead, ttail = os.path.split(trace)
rhead, rtail = os.path.split(ref)


logfile = "log.csv"

#gets current date and time for the logfile
time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if os.path.isfile(logfile):
	
	with open('log.csv', 'ab') as logfile:
		logfileWriter = csv.writer(logfile)
		logfileWriter.writerow([time, ttail, rtail, t_pb_tx, t_pp_tx, dif_pb_pp])

	logfile.close()
	
	

	
	
else :
	
	with open('log.csv', 'wb') as logfile:
		logfileWriter = csv.writer(logfile)
		logfileWriter.writerow(['Log Date', 'Trace File', 'Ref File', 'Positive Break', 'Postive Peak', 'Differnce'])
		logfileWriter.writerow([time, ttail, rtail, t_pb_tx, t_pp_tx, dif_pb_pp])

	logfile.close()



#----------------------------------------GRAPH STUFF---------------------------------------------------#

#plot columns to axis for trace
trace_time = [row[0] for row in trace_data]

trace_voltage = [row[1] for row in trace_data]

#plot column to axis for ref
ref_time = [row[0] for row in ref_data]
ref_voltage = [row[1] for row in ref_data]

plt.figure(1)

#REF sub plot
plt.subplot(211)
plt.plot(ref_time,ref_voltage,'y',lw=1.3)
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.text(0.08, 3.5, "Max V = " + str(ref_max_v) + "V")
plt.text(0.08, 3, "+ve Peak = " + str(pp_time_ref) + "s")

#TRACE sub plot
plt.subplot(212)
plt.plot(trace_time,trace_voltage,'b',lw=1.3)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)
plt.text(0.08, 0.6, "Max V = " + str(max_mv) + "mV")
plt.text(0.08, 0.5, "Min V = " + str(min_mv) + "mV")
plt.text(0.08, 0.4, "+ve Break = " + str(pb_time) + "s")
plt.text(0.08, 0.3, "+ve Peak = " + str(pp_time) + "s")

plt.show()




