
from matplotlib.markers import MarkerStyle
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

###############################################################################################
# This function checks if a file name exists in the output directory otherwise it creates it. #
###############################################################################################


#check the output folder!!!!

Input_Dir = '/Users/lmatak/Desktop/Lorenzo_Sims/Lorenzo_32km_vert_test'

# Choose between : 'Gustav', 'Irma', 'Katrina', 'Maria'
HNS = ['Irma']
# Choose between : '32km','8km'
GSS = ['32km']
# Choose between : 'NoTurb','TKE2D'
TMS = ['NoTurb']
# Choose between : 'YSU', 'MYJ', 'ACM2'
PBLS = ['MYJ']
# Choose between: '0.25' , '0.5', '1.0' , '2.0' , '4.0' , '8,0'
CLS = ['250','500','1000','2000']
spec_name = ['hpbl_0.5','hpbl_fix_400','hpbl_1.0','hpbl_2.0','kpbl_0.5','kpbl_2.0','hpbl_fix_1200','hpbl_fix_800',]
# Identify the time step
Time_Step = 6 
a=0
# Identify the time index
Time_Idx = 0 

# Define all hurricane's settings 
Hurricane_Settings = []
PBL='s'


Input_Dir_1 = '/Users/lmatak/Desktop/some_wrfout_files/Iota_32km_NoTurb_MYJ_hpbl_lvl_2'

csv_files = []
ncfiles = []

ncfiles = list_ncfiles (Input_Dir_1, ncfiles)
print(ncfiles)

#list of pblh lvls
average_kpbls=[]
#list for actual heights [m]
average_PBLHS=[]
#list for wspsds
All_Max_WND_SPD_10=[]
#list for vertical exchange coefficients
average_exch_ms=[]
exch_m=[]
exch_m_mid_pbl=[]
average_exch_ms_mid_pbl=[]
# initiate the list that will contain the hurricane-track data
min_slp = []
min_lat = []
min_long = []
lvl_heights=[]
idx=[1]
os.chdir(Input_Dir_1)

ncfile=Dataset(ncfiles[0])



z=np.array(getvar(ncfile,"z", Time_Idx))
# el_pbl=np.array(getvar(ncfile,"EL_PBL", Time_Idx))
akmk=np.array(getvar(ncfile,"AKMKL", Time_Idx))


PBLH_2D = np.array(getvar(ncfile,"PBLH", Time_Idx))
# U10_2D = np.array(getvar(ncfile, "U10", Time_Idx))
# V10_2D = np.array(getvar(ncfile, "V10", Time_Idx))
# PBLH_1D=PBLH_2D.flatten()
# U10_1D = U10_2D.flatten()
# V10_1D = V10_2D.flatten()
EXCH_H_3D=np.array(getvar(ncfile,"EXCH_H", Time_Idx))
EXCH_M_3D=np.array(getvar(ncfile,"AKMKL", Time_Idx))
for i in range(len(EXCH_M_3D)):
	print(np.average(EXCH_M_3D[i,:,:]),np.average(EXCH_H_3D[i,:,:]))

# WND_SPD_10 = U10_1D
el=[]
exch=[]
lvls=[]
# Calculate the wind intensity at each point of the map.
# for i in range (WND_SPD_10.size - 1):
# 		WND_SPD_10[i] = math.sqrt((U10_1D[i]**2)+(V10_1D[i]**2))
# for i in range(len(el_pbl)-1):
# 	lvls.append(np.average(z[i,:,:].flatten()[np.argsort(WND_SPD_10)[-100:]]))
# 	el.append(np.average(el_pbl[i,:,:].flatten()[np.argsort(WND_SPD_10)[-100:]]))
# 	exch.append(np.average(EXCH_M_3D[i,:,:].flatten()[np.argsort(WND_SPD_10)[-100:]]))
# # plt.plot(el,lvls,label='el')
# plt.plot(exch,lvls,label='exch')
# plt.legend()
# plt.show()     
        

                
        
                
