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

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.8,4.8),dpi=350)
# fig.subplots_adjust(hspace=0.3,wspace=0.2)

# show = 'xkzm'
show = 'xkzm'

CLS = [r'Clz_0p0001',r'Clz_0p0100',r'Clz_1p0000',r'Clz_100p0000',]
# plot_order = [0,3,1]
fig_name='_lvls_'
colors = ['blue', 'green', 'black','red']
legend_names=['Clz0p0001','Clz0p0100','Clz1p0000','Clz100p0000']

Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,66,72,80]
Real_Winds=[]
row_count=0
col_count=0
radius_dict={}
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
                WSPD = []
                rads=[]
                rads=Extract_the_shit2(csv_file, rads,'Radiuses')
                WSPD=Extract_the_shit2(csv_file, WSPD,' Average_WSPD')
                
                radius_idx=int(np.where(WSPD==np.max(WSPD))[0])

                if CL in radius_dict:            
                    radius_dict[CL].append(rads[radius_idx])
                #DECLARE new key, and append the value
                else:
                #DECLARE key as a list, so you can append, and eventually average it
                    radius_dict[CL]=[]
                    radius_dict[CL].append(rads[radius_idx])
                # print('for '+HN+' - '+CL+' max wspd is: ',np.amax(WSPD))
                
                # if cls_counter!=3 : cls_counter+=1
                cls_counter+=1
print(radius_dict)
for key in radius_dict.keys():
    print(key)
    radius_dict[key]=np.mean(radius_dict[key])
x_axis_name=[r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.0001',r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01',r'$Clz_{\mathrm{ YSU - 1 }}$ = 1',r'$Clz_{\mathrm{ YSU - 1 }}$ = 100',]


### FOR PLTOTING COEFF OF VAR ##
# vals=[74.99333248,	72.80530542,	67.60062501,56.55370854]
# plt.bar(x_axis_name,vals,color=['blue', 'green', 'black', 'red', 'cyan'])
# plt.ylabel(r'Coefficient of Variance (\%)',size=size)

### FOR RMW BARS ###
plt.bar(x_axis_name,radius_dict.values(),color=['blue', 'green', 'black', 'red', 'cyan'])
plt.ylabel(r'RMW (km)',size=size)

# plt.bar(x_axis_name,[21.6389,	20.193188	,16.817413	,10.732139])
# plt.tick_params(axis='both', labelsize=size)
# print(radius_dict)
# plt.ylabel(r'Variance',size=size)


#              )
# h, l = ax[0].get_legend_handles_labels()
# plt.rc('legend',fontsize=size)
# figl=plt.legend(h, legend_names,ncol=4,frameon=False,bbox_to_anchor=(0.68, 0.08),
#           bbox_transform=fig.transFigure)
fig.tight_layout()
# plt.show()
# print('saved as: fig9_wspd_r_boxes'+fig_name+'.eps')
plt.savefig('/Users/lmatak/Desktop/Megn_paper_figs/rmw_change.eps',bbox_inches='tight')
# print('saved as: figure8_WSPD_R'+name_text+PBLS[0]+'.eps')
# plt.savefig('/Users/lmatak/Desktop/leo_python_scripts/Paper_Figs/figs_saved/figure8_WSPD_R'+name_text+PBLS[0]+'.eps',bbox_inches='tight')