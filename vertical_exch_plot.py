from netCDF4 import Dataset
from numpy.core.fromnumeric import shape, size, transpose
from wrf import getvar
import numpy as np
import math
import csv
import os
import matplotlib.pyplot as plt

def list_files_8(Dir):
	Post_Processed_Data = []
	for f in os.listdir(Dir):
		Post_Processed_Data.append(f)
	return (Post_Processed_Data)

def list_ncfiles(Dir, ncfiles):
	for f in os.listdir(Dir):
		if f.startswith('wrfout'):
			ncfiles.append(f)
	ncfiles.sort()
	return (ncfiles)


fig, ax = plt.subplots(nrows=3, ncols=6, figsize=(15,10), sharex=False, sharey=False)
#it has to be 1, bcz last ncfile doesn't have as many timesteps!
Idxs = np.arange(0,6)
print('Indexes : ',Idxs)

# Define all hurricane's settings 
Hurricane_Settings = []

Input_Dir_1 = '/Users/lmatak/Desktop/some_wrfout_files/Iota_32km_NoTurb_MYJ_hpbl_1.0'
Input_Dir_2 = '/Users/lmatak/Desktop/some_wrfout_files/Iota_32km_NoTurb_MYJ_hpbl_km_0.25'

dirs = [Input_Dir_1,Input_Dir_2]
for dir in dirs:
        print(dir)
        os.chdir(dir)
        ncfiles_first_and_last=[]
        ncfiles = []
        ncfiles = list_ncfiles (dir, ncfiles)
        ncfiles_first_and_last.append(ncfiles[0])
        ncfiles_first_and_last.append(ncfiles[3])
        print(ncfiles_first_and_last)
        ncfiles_first_and_last.append(ncfiles[-2])
        j=1
        ncfile_num=0
        for ncfile in ncfiles_first_and_last:
                ncfile=Dataset(ncfile)
                ncfile_num+=1
                for Time_Idx in Idxs:
                        print('Time idx: ',Time_Idx)
                        U10_2D = np.array(getvar(ncfile, "U10", Time_Idx))
                        V10_2D = np.array(getvar(ncfile, "V10", Time_Idx))

                        U10_1D = U10_2D.flatten()
                        V10_1D = V10_2D.flatten()
                        WND_SPD_10 = U10_1D
                        # Calculate the wind intensity at each point of the map.
                        for i in range (WND_SPD_10.size - 1):
                                WND_SPD_10[i] = math.sqrt((U10_1D[i]**2)+(V10_1D[i]**2))
                        top_100_idx = np.argsort(WND_SPD_10)[-100:]
                        EXCH_M_3D=np.array(getvar(ncfile,"AKMKL", Time_Idx))
                        lvl_heights=[]
                        exch=[]
                        z=np.array(getvar(ncfile, "z",Time_Idx))
                        for i in range(3):
                                lvl_heights.append(np.average(z[i].flatten()[top_100_idx]))
                                exch.append(np.average(EXCH_M_3D[i].flatten()[top_100_idx]))
                                # print(np.average(EXCH_M_3D[i].flatten()[top_100_idx]))
                        print('j = ',j)
                        plt.subplot(3,6,j) 
                        print(exch)
                        plt.plot(exch,lvl_heights,label=Time_Idx)
                        plt.title('ncfile '+str(ncfile_num)+' Time idx - '+str(Time_Idx))
                
                        j +=1
plt.subplot(3,6,3).legend(('km_1.0','km_0.25'),bbox_to_anchor = (0.1, 1.3), mode='expand', frameon='True',
			 ncol = 2, )
plt.show()
# handles, labels = fig.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))






