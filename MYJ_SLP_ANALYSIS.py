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
HNS = ['Lorenzo']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TMS = ['NoTurb']
# Choose between : 'cLh0p2', 'cLh0p5', 'cLh1p0', 'cLh1p5'
PBLS=['MYJ']
CLS = ['kmkh_0.25_lvl_8','kmkh_1.0_lvl_8','kmkh_2.0_lvl_8','kmkh_4.0_lvl_8','kmkh_6.0_lvl_8'] #,'1.0','2000']
# Choose between: '0', '1', '2', '3', '4', '5'
Time_idx = 0
row=0
column=0
cl_counter=0
# Choose the altitude:
Alt = 150
max_wspd=0
nbins=7
cmap_name='my_colors'
#coolwarm is the red-blue one
cmap=plt.get_cmap(
    'twilight_shifted')
# Create a figure               #hspace is horisontal!
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12,8), sharex=True, sharey=True,subplot_kw={'projection': crs.PlateCarree()})
plt.subplots_adjust(left=0.2, bottom=None, right=None, top=None, wspace=0.4, hspace=0.05)
# plt.subplots(constrained_layout=True)
colors=['lightyellow','indigo','lightgreen','lightblue','blue','yellow','red','black']
cm = LinearSegmentedColormap.from_list(
        cmap_name, colors, N=nbins)
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

                        #Extract the necessary data to plot the contour map.
                        slp = getvar(Data, "slp", timeidx = Time_idx)
                        z = getvar(Data, "z", timeidx = Time_idx)
                        wspd = getvar(Data, "wspd", timeidx = Time_idx)

                        print('row:',row,'column:,',column)
                        ax[row,column].stock_img()
                        ax[row,column].coastlines('50m', linewidth=0.8)

                        gl = ax[row,column].gridlines(crs=crs.PlateCarree(), draw_labels=True,
                            linewidth=0.2, color='black', alpha=0.2, linestyle='--')
                        gl.top_labels = False
                        gl.right_labels = False
                        gl.xlabel_style= {'size': 12, 'color': 'black'}
                        gl.ylabel_style= {'size': 12, 'color': 'black'}

                        # Interpolate geopotential height, u, and v winds to 500 hPa
                        wspd_500 = interplevel(wspd, z, Alt)

                        # Get the latitude and longitude points
                        lats, lons = latlon_coords(wspd_500)

                        # Get the cartopy mapping object
                        cart_proj = get_cartopy(wspd_500)
                            #this is for wind speed
                            #lvls thinh is just how many nijansi boje
                        if (float(np.amax(wspd))) > max_wspd:
                            max_wspd=float(np.amax(wspd))
                            im_cbar = ax[row,column].contourf(to_np(lons), to_np(lats), to_np(wspd_500), 30,
                                transform=crs.PlateCarree(),vmin=0 ,vmax=75,
                                cmap= cmap)
                        else:
                            im = ax[row,column].contourf(to_np(lons), to_np(lats), to_np(wspd_500), 30,
                                transform=crs.PlateCarree(),vmin=0 ,vmax=75,
                                cmap= cmap)
                            #this is for SLP countours
                        CS = ax[row,column].contour(to_np(lons), to_np(lats), to_np(slp), 6, colors="black", alpha=1,
                            transform=crs.PlateCarree(), linewidths = 1)


                        if HN == 'Iota':
                            ax[row,column].set_extent([-79,-81, 13 , 15])
                            
                        elif HN =='Lorenzo':
                            ax[row,column].set_extent([-37.25,-38.75, 13.5 , 15.05])
                            
                        elif HN=='Dorian':
                            ax[row,column].set_extent([-70.31,-71.25, 25 , 26])
                            
                        elif HN=='Laura':
                            ax[row,column].set_extent([-88.5,-90.5, 25 , 27])
                            
                        # ax[i].set_extent([-70,-72, 24.5 , 26])
                        ax[row,column].clabel(CS, CS.levels, inline=True, fontsize=8, inline_spacing=8,  use_clabeltext=True)
                        
                    #setting the counter to reset for next row if all columns are used
                    column+=1
                    if column==3:
                        column=0
                        row+=1




# ax[0,0].annotate('Dorian',
#             xy=(.08, .765), xycoords='figure fraction',
#             horizontalalignment='center', verticalalignment='baseline',rotation='vertical',
#             fontsize=20)
# ax[0,0].set_ylabel('ahain wat the fuck')

# Add a color bar
# for i in range(len(CLS)):
#     ax[0,i].set_title('HPBL - ' + CLS[i], {'size': 16})
row=0
column=0
for i in range(len(CLS)):
    ax[row,column].set_title(CLS[i])
    column+=1
    if column==3:
        column=0
        row+=1
# ax[0.0].annotate('Dorian',
#     #first numver in xy=() is x-axis
#             xy=(.16, .75), xycoords='figure fraction',
#             horizontalalignment='center', verticalalignment='baseline',rotation='vertical',
#             fontsize=20)
# ax[1,0].annotate('Iota',
#     #first numver in xy=() is x-axis
#             xy=(.16, .755-1/3), xycoords='figure fraction',
#             horizontalalignment='center', verticalalignment='baseline',rotation='vertical',
#             fontsize=20)
# ax[2,0].annotate('Lorenzo',
#     #first numver in xy=() is x-axis
#             xy=(.16, .755-2/3), xycoords='figure fraction',
#             horizontalalignment='center', verticalalignment='baseline',rotation='vertical',
#             fontsize=20)
        
# for i in range(len(HNS)):
    
#     ax[i,0].annotate(HNS[i],
#     #first numver in xy=() is x-axis
#             xy=(.14, .745-i/3.5), xycoords='figure fraction',
#             horizontalalignment='center', verticalalignment='baseline',rotation='vertical',
#             fontsize=20)
    # gl=ax[i,0].set_ylabel(HNS[i])
    # gl = ax[i,0].gridlines(crs=crs.PlateCarree(), draw_labels=True,
    #                         linewidth=0.2, color='black', alpha=0.2, linestyle='--')
    # gl.top_labels = False
    # gl.right_labels = False
    # gl.xlabel_style= False
    # gl.ylabel_style= False


# fig.subplots_adjust(right=0.8)


fig.suptitle(HN+' - '+GS+' - '+TM+' - '+PBL, fontsize=18)
#first coord is the x-axis
cbar_ax = fig.add_axes([0.91, 0.15, 0.02, 0.7])

cbar = plt.colorbar(im_cbar, cax=cbar_ax)#, label = 'Wind Speed [m/s] at 500 m Above Sea-Level')
cbar.set_label('Wind Speed [m/s] at '+str(Alt)+' m Above Sea-Level', rotation = 270, labelpad = 25, size = 'large')
cbar.ax.tick_params(labelsize=12)

plt.show()
