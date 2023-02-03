
import os
from all_functions import list_ncfiles , Calculate_Distance_Haversine, create_file,hurricane_eye_3
import numpy as np
from wrf import getvar
from netCDF4 import Dataset




#choose ['Lorenzo'] #,'Dorian','Iota','Lorenzo','Igor','Maria']
HNS = ['Katrina','Maria','Dorian','Igor','Lorenzo',]
# Choose between : '2km', '4km', '8km', '16km', '32km'
GSS = ['8km']
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TMS = ['NoTurb']
# Choose between : 'YSU', 'MYJ', 'ACM2'
PBLS = ['MYJ']
# Choose between : 'cLh0p2', 'cLh0p5', 'cLh1p0', 'cLh1p5'


def get_cv_band(dict_with_wspd):
        working_dict=dict_with_wspd
        temp_dict={}
        total_cv=0
        for key in (sorted(working_dict.keys()))[5:51]:
                # print('mean',np.mean(working_dict[key]))
                # print('std dev',np.std(working_dict[key],ddof=0))
                # print('cv? ',100*np.std(working_dict[key])/np.mean(working_dict[key]))
                temp_dict[key]=cv(working_dict[key])
                # print()
                # print('radius: ',key*8,'using cv : ',temp_dict[key])
                total_cv+=temp_dict[key]
        # print(temp_dict.keys())
        # print(total_cv)
        
        
        return total_cv/len(temp_dict)

CLS         = ['changeClz_0p0001','changeClz_0p0100','changeClz_1p0000','changeClz_100p0000',]
# Set the input directory.
Input_Dir    = '/project/momen/Lmatak/WRF_COAWST/Hurricanes/cases_10_to_20/'
Output_Dir = '/project/momen/Lmatak/WRF_COAWST/outputs/'

# Choose between: '0', '1', '2', '3', '4', '5'
Time_idxs = [0]
#Choose a radius interval
all_hurricane_all_clz=[]
one_hurricane_all_clz=[]

cv = lambda x: np.std(x, ddof=1) / np.mean(x) * 100 
# Check the simulations to be working on.

variance_to_write=[]

for HN in HNS:
        variance_per_hur=[]
        one_hurricane_all_clz=[]
        for CL in CLS:
                one_hur_one_timestep=0
                
                variance_per_clz=[]
                Hurricane_Setting = 'WRFONLY_NoTurb_8km_isftcflx_1_' + CL
                Input_Dir_1 = Input_Dir + HN + '/8km/' + Hurricane_Setting
                ncfiles = []
                print(Input_Dir_1)
                ncfiles = list_ncfiles (Input_Dir_1, ncfiles)
                os.chdir(Input_Dir_1)

                # ncfiles='/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/BEM_default/wrfout_d03_2019-04-01_18/00/00'
                # os.chdir('/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/BEM_default/')
                # ncfiles=[0,1,2]
                for ncfile in ncfiles:
                        radius_dict={}
                        wspd_vals_list=[]
                        # ncfile='/Users/lmatak/Downloads/URBAN_SCHEME_CONTOURING/BEM_default/wrfout_d01_2005-08-28.nc'
                        file=Dataset(ncfile)

                        u10=np.array(getvar (file, 'U10'))
                        v10=np.array(getvar (file, 'V10'))
                        total_wspd=np.sqrt(u10**2+v10**2)
                        line_of_wspds=[]
                        # slp=getvar(file,'SLP',0)
                        Lats = np.array(getvar (file, 'XLAT')[:,0])
                        Lons = np.array(getvar (file, 'XLONG')[0,:])

                        (Eye_Slp, Eye_Idx, Eye_Xlat, Eye_Xlon) = hurricane_eye_3(file, 0)
                        eye_lon_idx=Eye_Idx[1]
                        eye_lat_idx=Eye_Idx[0]

                        # print('lon',eye_lon_idx,'lat',eye_lat_idx)


                        # print(Calculate_Distance_Haversine(Lats[int(172)]\
                                        # ,Lons[(int(317))],Eye_Xlat,Eye_Xlon))

                        #get  the wspd values for the bands of 8km 
                        for i in range(len(Lons)):
                                for j in range(len(Lats)):
                                        distance_from_eye=Calculate_Distance_Haversine(Lats[int(j)]\
                                        ,Lons[(int(i))],Eye_Xlat,Eye_Xlon)
                                        # print(distance_from_eye)

                                        if (int(distance_from_eye/8)) in radius_dict:            
                                                radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),int(i)])
                                        #DECLARE new key, and append the value
                                        else:
                                        #DECLARE key as a list, so you can append, and eventually average it
                                                radius_dict[ (int(distance_from_eye/8)) ]=[]
                                                radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),int(i)])
                        # print(get_cv_band(radius_dict))
                        one_hur_one_timestep+=get_cv_band(radius_dict)
                        print('HN',HN,'CL',CL)
                        print('one_hur_one_timestep ',one_hur_one_timestep)
                one_hurricane_all_clz.append(one_hur_one_timestep/len(ncfiles))
                print('one_hurricane_all_clz',one_hurricane_all_clz)
        all_hurricane_all_clz.append(one_hurricane_all_clz)
        print('all_hurricane_all_clz',all_hurricane_all_clz)

print('all_hurricane_all_clz average', np.mean(all_hurricane_all_clz,0))
                                                



variance_to_write=np.mean(all_hurricane_all_clz)


# Exporting the data in a csv format.
create_file (Output_Dir, 'assymetry')
create_file (Output_Dir + 'assymetry/', 'assymetry_file')


MyFile=open("COEFFICIENT_OF_VAR_LATEST_November.csv",'w')
MyFile.write ("Clz_0p0001, Clz_0p0100, Clz_1p0000, Clz_100p0000" + "\n")
for n in range (len(variance_to_write)):
        MyFile.write ((str(variance_to_write[n])) + ',' )



