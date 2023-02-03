import os
import numpy as np
import matplotlib.pyplot as plt
from all_functions import list_csv_files_0,Extract_by_name,calculate_intensity_error,calculate_distance_error
from netCDF4 import Dataset

os.environ["PATH"]+=":/Library/TeX/texbin/"
print(os.environ["PATH"])
plt.rcParams.update({
    "text.usetex":True,
    "font.family":'Times New Roman'
})


Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data/'
os.chdir(Real_data_dir)
Input_Dir = '/Users/lmatak/Desktop/Megn_paper_figs/tropical_storm_errors/'

HNS = ['Jerry','Gabrielle','Sebastien',] #,'Sebastien',]

CLS = ['clz_0p0001','clz_0p0100','clz_1p0000','clz_100p0000',]

fig = plt.figure(figsize=(5, 5), tight_layout=True,dpi=350)

# all_cls_single_hur_track=[]
# all_cls_single_hur_wspd=[]
# all_hurs_track=[]
# all_hurs_wspd=[]

# sim_wspds_one_hur=[]
# sim_lats_one_hur=[]
# sim_longs_one_hur=[]
# error=0
# sim_wspds_all_hur=[]
# #Sebastien from 0 to 5?
# ffrom=0
# to=7
# for HN in HNS:
#     if HN=='Jerry':
#         ffrom=6
#         to=14
#     else:
#         ffrom=0
#         to=7
#     #real part
#     Real_Hurricane_Data=Real_data_dir+'/Real_Data_'+HN+'.csv'

#     Real_Winds=[]
#     real_lats=[]
#     real_longs=[]

#     Real_Winds = Extract_by_name(Real_Hurricane_Data,Real_Winds,'Wind Speed(kt)')
#     Real_Winds=Real_Winds[ffrom:to]
#     real_lats=Extract_by_name(Real_Hurricane_Data,real_lats,'Lat')
#     real_lats=real_lats[ffrom:to]
#     real_longs=Extract_by_name(Real_Hurricane_Data,real_longs,'Lon')
#     real_longs=real_longs[ffrom:to]

        
#     #sim part
#     work_dir=Input_Dir+HN+'0'
#     os.chdir(work_dir)
#     csv_files=(list_csv_files_0(work_dir,CLS))
#     print(csv_files)
#     all_cls_single_hur_track=[]
#     all_cls_single_hur_wspd=[]

#     for csv_file in csv_files:
        
#         sim_wspd=[]
#         sim_wspds_one_hur=[]
#         #list for one hur, one setting, 6 timesteps
#         sim_wspds_one_hur=Extract_by_name(csv_file,sim_wspd,'All_Max_WND_SPD_10')
#         sim_wspds_one_hur=sim_wspds_one_hur[ffrom:to]
#         sim_lats=[]
#         sim_lons=[]
        
#         sim_lats=Extract_by_name(csv_file,sim_lats,'min_lat')
#         sim_lats=sim_lats[ffrom:to]
#         sim_lons=Extract_by_name(csv_file,sim_lons,'min_long')
#         sim_lons=sim_lons[ffrom:to]

#         ##this var is error per cl per HR
#         error_track=calculate_distance_error(sim_lats,sim_lons,real_lats,real_longs)
#         error_wspd=calculate_intensity_error(sim_wspds_one_hur,Real_Winds)
#         # print(HN,error_track)
#         all_cls_single_hur_track.append(error_track)
#         all_cls_single_hur_wspd.append(error_wspd)
#     print(all_cls_single_hur_track)
#     print(all_cls_single_hur_wspd)
#     #this one makes the array   
#     all_hurs_track.append(all_cls_single_hur_track)  
#     all_hurs_wspd.append(all_cls_single_hur_wspd)

# d=np.mean(all_hurs_track,0)
# z=np.mean(all_hurs_wspd,0)
# # print(z)
# # this is the end result, averaged over 4 hurs!
# # plt.axhline(d[2], 0, 5, c='black',linestyle='--',linewidth=0.7 )
# # plt.ylim(80, 120)

## FOR PLOTTING COVARIANCE##

z=[24.29923376,	21.87118104,	17.99024592,	12.99517594]

# plt.title('Hurricane wind intensity forecast error',size=16)
# plt.ylabel(r'MAPE (\%)',size=14)
plt.ylabel(r'Coefficient of Variance (\%)',size=14)

x_axis_name=[r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.0001',r'$Clz_{\mathrm{ YSU - 1 }}$ = 0.01',r'$Clz_{\mathrm{ YSU - 1 }}$ = 1',r'$Clz_{\mathrm{ YSU - 1 }}$ = 100',]
plt.bar(x_axis_name,z,color=['blue', 'green', 'black', 'red', 'cyan'])
plt.xticks(rotation=15,size=13)
plt.yticks(size=14)
# plt.bar([0,1,2,3],z)
# print(np.mean(all_hurs_track,0))
# plt.savefig('/Users/lmatak/Desktop/Megn_paper_figs/MAPE_trop_storms.eps',bbox_inches='tight')
plt.savefig('/Users/lmatak/Desktop/Megn_paper_figs/before_momen_revieq/coeff_of_var.eps',bbox_inches='tight')
# plt.show()
        

        