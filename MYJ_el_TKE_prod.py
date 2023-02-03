from typing import Counter
from wrf import (getvar, interplevel, smooth2d, to_np, latlon_coords, get_cartopy, cartopy_xlim, cartopy_ylim)
from Func_Extract_Data import Extract_Track_Data
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.feature import NaturalEarthFeature
from Func_List_Files import list_ncfiles
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
from netCDF4 import Dataset
import cartopy.crs as crs
import numpy as np
import math
import os


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'



# Define the hurricane's directory.
Input_Dir = '/Users/lmatak/Desktop/some_wrfout_files/'
# Choose between : 'Gustav', 'Irma', 'Katrina', 'Maria'
HNS = ['Iota']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TMS = ['NoTurb']
# Choose between : 'cLh0p2', 'cLh0p5', 'cLh1p0', 'cLh1p5'
PBLS=['MYJ']
CLS = ['1.0','el_0.25','el_2.0','el_4.0']
# Choose between: '0', '1', '2', '3', '4', '5'
Time_idx = 0
row=0
column=0
cl_counter=0

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,8))
plt.subplots_adjust(left=0.2, bottom=None, right=None, top=None, wspace=0.4, hspace=0.05)
# plt.subplots(constrained_layout=True)
for HN in HNS:
    

    for GS in GSS:
        for TM in TMS:
            i = 0
            for PBL in PBLS:
                for CL in CLS: 
                    ncfiles = []                    
                    Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL
                    Input_Dir_1 = Input_Dir +  Hurricane_Setting


                    ncfiles = list_ncfiles(Input_Dir_1, ncfiles)

                    for ncfile in ncfiles[0:1]:

                        # Set the working space.
                        os.chdir(Input_Dir_1)
                        # Open the NetCDF file
                        Data = Dataset(ncfile)
                        

                        tke_pbl=getvar(Data, 'TKE_PBL')
                        el_pbl=getvar(Data, 'EL_PBL')
                        z=np.array(getvar(Data,"z"))
                        print(tke_pbl.shape)
                        print(el_pbl.shape)
                        lvls=[]
                        tke_avg=[]
                        el_avg=[]
                        for i in range(len(el_pbl)-1):
                            lvls.append(np.average(z[i,:,:]))
                            tke_avg.append(np.average(tke_pbl[i,:,:]))
                            el_avg.append(np.average(el_pbl[i,:,:]))
                        # plt.subplot(1,1,11)
                        plt.subplot(1,2,1)
                        plt.plot(el_avg,lvls,label='EL')
                        plt.title('EL')
                        plt.subplot(1,2,2)
                        plt.plot(tke_avg,lvls,label='TKE')
                        plt.title('TKE')

                            
                       
                          
# handles, labels = fig.gca().get_legend_handles_labels()
# by_label = dict(zip(labels, handles))
# print(by_label)
# fig.legend(['EL','TKE'],loc = 'upper center',ncol=2)
plt.show()
