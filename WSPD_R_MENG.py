from numpy.core.function_base import linspace
from all_functions import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data, Extract_the_shit2
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter,LatitudeLocator
import numpy as np





Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Input_Dir = '/Users/lmatak/Downloads/clz_cases/wspd_quadrant/QUADRANT_5/'

# for MYJ 'Maria','Dorian','Iota','Teddy','Lorenzo , Igor
HNS = ['Katrina','Maria','Dorian','Igor','Lorenzo']
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '8km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Time_idx = '0'
os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})
size=17

fig, ax = plt.subplots(nrows=1, ncols=5, figsize=(12.8,4.8))
# fig.subplots_adjust(hspace=0.3,wspace=0.2)

# show = 'xkzm'
show = 'xkzm'

CLS = ['Clz_0p0001','Clz_0p0100','Clz_1p0000','Clz_100p0000',]
# plot_order = [0,3,1]
fig_name='_lvls_'
colors = ['blue', 'green', 'black','red']
legend_names=[r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.0001',r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01',r'$Clz_{\mathrm{ YSU - 1 }}$ = 1',r'$Clz_{\mathrm{ YSU - 1 }}$ = 100',]


Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
Real_Winds=[]
row_count=0
col_count=0

for PBL in PBLS:

    for HN in HNS :

        Input_Dir_1 = Input_Dir + '/' + HN + '/'
        # Input_Dir_1='/Users/lmatak/Downloads/'
        Real_Hurricane_Data = Real_data_dir+'/Real_Data_'+HN+'.csv'


        
        cls_counter=0
        for CL in CLS:

                #by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
                Hurricane_Setting = 'WRFONLY_NoTurb_8km_isftcflx_1_change'+CL +'.csv'		




                # print(Hurricane_Setting)
                csv_file = (Input_Dir_1+Hurricane_Setting)
                # print('csv file is ::::: ',csv_file)
                # you define empty lists which will contain the extracted data from the csv file, and plot them immediatle
                WSPD = []
                rads=[]
                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')

                ax[col_count].plot(rads[0:60], WSPD[0:60], color=colors[cls_counter],  linestyle='-',
                marker='x', markersize='0',  
                    linewidth='3', label= CL,)

                print('for '+HN+' - '+CL+' max wspd is: ',np.amax(WSPD))
                
                
                # if cls_counter!=3 : cls_counter+=1
                cls_counter+=1
        # xticks=linspace(0,rads[-1],15)
        # print(xticks)
        ax[col_count].set_title(HN,size=size+1.5)
        ax[col_count].tick_params(axis='both', labelsize=size)
        # ax[row_count,col_count].set_xticklabels(xticks)
        # ax[row_count,col_count].set_yticks(wind_intensities[0:number_of_lvls])
        col_count+=1
        if col_count == 5:
            col_count =0
            row_count = 1
ax[0].set_ylabel(r'Average wind speed $\mathrm{(\,ms^{-1}) \,}$', size=size)
# ax[1,0].set_ylabel(r'Average WSPD $\mathrm{(\,ms^{-1}) \,}$',size=size)
ax[0].set_xlabel(r'Radius (km)',size=size)
ax[1].set_xlabel(r'Radius (km)',size=size)
ax[2].set_xlabel(r'Radius (km)',size=size)
ax[3].set_xlabel(r'Radius (km)',size=size)
ax[4].set_xlabel(r'Radius (km)',size=size)

# ax[2].annotate('STRONG', xy=(0.7, 1.2), xycoords='axes fraction',
#              xytext=(0, 0), textcoords='offset points',
#              ha="right", va="top",size=22,
             
            #  )
            
# ax[1,2].annotate('WEAK', xy=(0.7, 1.182), xycoords='axes fraction',
#              xytext=(0, 0), textcoords='offset points',
#              ha="right", va="top",size=22,
             
#              )
h, l = ax[0].get_legend_handles_labels()
plt.rc('legend',fontsize=size)
figl=plt.legend(h, legend_names,ncol=4,frameon=False,bbox_to_anchor=(0.9, 0.02),
          bbox_transform=fig.transFigure)
# fig.tight_layout()
# plt.show()
# print('saved as: fig9_wspd_r_boxes'+fig_name+'.eps')
plt.savefig('/Users/lmatak/Downloads/clz_cases/wspd_quadrant/QUADRANT_5/whole_dom_avg.jpg',bbox_inches='tight')
# print('saved as: figure8_WSPD_R'+name_text+PBLS[0]+'.eps')
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure8_WSPD_R'+name_text+PBLS[0]+'.eps',bbox_inches='tight')