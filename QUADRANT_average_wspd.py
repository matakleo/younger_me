import numpy as np
from all_functions import Calculate_Distance_Haversine, hurricane_eye_3
from wrf import getvar,interplevel
from netCDF4 import Dataset
from collections import OrderedDict
import matplotlib.pyplot as plt
file='/Users/lmatak/Downloads/wrfout_d01_2019_dorian'
file=Dataset(file)

radius_band=8

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
QUAD_select=2
radius_dict={}

if QUAD_select==1:
                                                ##i is for LONG to go from EYE to the end of domain
                                                for i in range(len(Lons)-int(eye_lon_idx)):
                                                ##j is for LATS to go from EYE to the end of domain
                                                        for j in range(len(Lats)-int(eye_lat_idx)):

                                                                #iterate through all the FIRST QUADRANT quarter of domain points,
                                                                #calculate the distance using the formule
                                                                distance_from_eye=Calculate_Distance_Haversine(Lats[int(eye_lat_idx+j)]\
                                                                ,Lons[(int(eye_lon_idx)+i)],Eye_Xlat,Eye_Xlon)

                                                                #add the values to the DICTIONARY
                                                                #if the radius has already been established, just append the value
                                                                if str(int(distance_from_eye/8)) in radius_dict:            
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(eye_lat_idx+j),int(eye_lon_idx)+i])
                                                                #DECLARE new key, and append the value
                                                                else:
                                                                #DECLARE key as a list, so you can append, and eventually average it
                                                                        radius_dict[ (int(distance_from_eye/8)) ]=[]
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(eye_lat_idx+j),int(eye_lon_idx)+i])
                                                        #loop through the radiuses/keys, and average all the values for that radius
elif QUAD_select==2:
                                                ##i is for LONG to go from EYE to the end of domain
                                                for i in range(0,int(eye_lon_idx)):
                                                ##j is for LATS to go from EYE to the end of domain
                                                        for j in range(len(Lats)-int(eye_lat_idx)):

                                                                #iterate through all the FIRST QUADRANT quarter of domain points,
                                                                #calculate the distance using the formule
                                                                distance_from_eye=Calculate_Distance_Haversine(Lats[int(eye_lat_idx+j)]\
                                                                ,Lons[(i)],Eye_Xlat,Eye_Xlon)

                                                                #add the values to the DICTIONARY
                                                                #if the radius has already been established, just append the value
                                                                if (int(distance_from_eye/8)) in radius_dict:            
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(eye_lat_idx+j),i])
                                                                #DECLARE new key, and append the value
                                                                else:
                                                                #DECLARE key as a list, so you can append, and eventually average it
                                                                        radius_dict[ (int(distance_from_eye/8)) ]=[]
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(eye_lat_idx+j),+i])
elif QUAD_select==3:
                                                ##i is for LONG to go from EYE to the end of domain
                                                for i in range(0,int(eye_lon_idx)):
                                                ##j is for LATS to go from EYE to the end of domain
                                                        for j in range(0,int(eye_lat_idx)):

                                                                #iterate through all the FIRST QUADRANT quarter of domain points,
                                                                #calculate the distance using the formule
                                                                distance_from_eye=Calculate_Distance_Haversine(Lats[int(j)]\
                                                                ,Lons[(i)],Eye_Xlat,Eye_Xlon)

                                                                #add the values to the DICTIONARY
                                                                #if the radius has already been established, just append the value
                                                                if str(int(distance_from_eye/8)) in radius_dict:            
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),i])
                                                                #DECLARE new key, and append the value
                                                                else:
                                                                #DECLARE key as a list, so you can append, and eventually average it
                                                                        radius_dict[ (int(distance_from_eye/8)) ]=[]
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),+i])
                                                        #loop through the radiuses/keys, and average all the values for that radius
else:
                                                ##i is for LONG to go from EYE to the end of domain
                                                for i in range(len(Lons)-int(eye_lon_idx)):
                                                ##j is for LATS to go from EYE to the end of domain
                                                        for j in range(int(eye_lat_idx)):

                                                                #iterate through all the FIRST QUADRANT quarter of domain points,
                                                                #calculate the distance using the formule
                                                                distance_from_eye=Calculate_Distance_Haversine(Lats[int(j)]\
                                                                ,Lons[(int(eye_lon_idx)+i)],Eye_Xlat,Eye_Xlon)

                                                                #add the values to the DICTIONARY
                                                                #if the radius has already been established, just append the value
                                                                if str(int(distance_from_eye/8)) in radius_dict:            
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),int(eye_lon_idx)+i])
                                                                #DECLARE new key, and append the value
                                                                else:
                                                                #DECLARE key as a list, so you can append, and eventually average it
                                                                        radius_dict[ (int(distance_from_eye/8)) ]=[]
                                                                        radius_dict[ (int(distance_from_eye/8)) ].append(total_wspd[int(j),int(eye_lon_idx)+i])
                                                
                                        
                                        

                                        
                                        
#loop through the radiuses/keys, and average all the values for that radius

# d = {2:3, 1:89, 4:5, 3:0}
# >>> dict(sorted(d.items()))
# {1: 89, 2: 3, 3: 0, 4: 5}
# OrderedDict(sorted(d.items())
# OrderedDict(sorted(d.items(), key=lambda t: t[0]))
for key in (sorted(radius_dict.keys())):
    print(key)
    radius_dict[key]=np.mean(radius_dict[key])
    #append the averaged radius values to a list
    line_of_wspds.append(radius_dict[key])

dict2={'3':'da','1':'bla','2':'z'}
# sorted(key_value.keys()
print(sorted(dict2.keys()))

plt.plot(np.arange(0,8*50,8),line_of_wspds[:50])
plt.show()
