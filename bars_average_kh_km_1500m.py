from Func_Extract_Data import Extract_by_name,variance
from Func_List_Files import list_csv_files_0
import matplotlib.gridspec as gridspec
import os
import numpy as np
import matplotlib.pyplot as plt
import statistics



Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'
os.chdir(Real_data_dir)
Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
# Choose between : 'Dorian','Laura','Lorenzo','Maria','Irma','Iota'
HNS = ['Maria','Teddy','Lorenzo','Dorian']

GSS = ['8km']

TM = 'NoTurb'

PBLS = ['MYJ']
CLS = ['1.0','kmkh_0.25','kmkh_2.0','kmkh_4.0','kmkh_6.0']
# CLS = ['1.0','xkzm_0.25','xkzm_2.0','xkzm_4.0','xkzm_6.0','xkzm_8.0']
# CLS_MYJ=['1.0','KH_0.25','KH_2.0','KH_4.0','KH_6.0','KH_8.0']
# colors = ['blue', 'orange', 'red', 'green', 'purple', 'magenta','yellow']
colors = ['darkblue', 'lightblue','darkgreen', 'lightgreen', 'magenta','yellow','blue']
colors_per_CLS=['red','blue','black','grey','cyan']
#make the figure
fig= plt.figure(figsize=(8, 8), tight_layout=True)
#add the gridspec for easier hadnling
gs = gridspec.GridSpec(1,1,figure=fig,wspace=0.2,top=0.8)
#this you need for plotting at the end of script
bar_counter=0
PBL_counter=0

height_under_which_to_average=500
#initate subplots
Time_Idx = 0
ax1 = fig.add_subplot(gs[0,0])

kh_over_km_average_all_hur=[]
for PBL in PBLS:
    for HN in HNS:
        kh_over_km_average_single_hur=[]
    
        for GS in GSS:
            List_for_CSV_files=[]
            #this will iterate through directories which will have simulation otput files in them
            # e.g. /Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls/Dorian/8km/NoTurb/Standard/
            ####
            Hurricane_Dir =Input_Dir + '/' + HN + '/' + GS + '/' + TM +'/Standard/'
            for CL in CLS:
            #get the second part of the simulation name in list e.g. 'MYJ_hpbl_250'
                List_for_CSV_files.append(PBL+'_hpbl_'+CL)
                csv_files=list_csv_files_0(Hurricane_Dir,List_for_CSV_files)
                
    
    #loop through all the csv files in the directory of certein HN
            for csv_file in csv_files:
                #make empty lists
                lvl_heights=[]
                exch_m=[]
                exch_h=[]
                kh_over_km=[]
                
                #get the data from .csv for every hurricane case e.g. hbl=250
                lvl_heights = Extract_by_name(csv_file, lvl_heights, 'lvl_heights')
                #get the index of the element in lvl_heights that is larger than 1500m
                
                height_index=(next(x[0] for x in enumerate(lvl_heights) if x[1] > height_under_which_to_average))
            
                exch_m=Extract_by_name(csv_file,exch_m,'avg_vert_exch_momentum')[:height_index]
                exch_h=Extract_by_name(csv_file,exch_h,'avg_vert_exch_scalar')[:height_index]
                #calculate kh/km for first ~10 lvls, add them all in a list kh_over_km
                for i in range(height_index):
                    #try is here to catch division by 0!
                    try:
                        kh_over_km.append(exch_h[i]/exch_m[i])
                    except:
                        kh_over_km.append(0)
                #append the averaged value of list kh_over_km for every CLS case of single hurricane
                kh_over_km_average_single_hur.append(np.average(kh_over_km))
            #append the list of averaged values of single hurricane into an array which will hold all the hurricanes
            kh_over_km_average_all_hur.append(kh_over_km_average_single_hur)
    #turn the list of all hurricanes into np.array to make it easier to handle
    kh_over_km_average_all_hur=np.array(kh_over_km_average_all_hur)
    #make i in the range of x axis values
    print(kh_over_km_average_all_hur)
    for i in range(len(CLS)):
        c=0.1
        #get the stddev
        std_dev=statistics.stdev(kh_over_km_average_all_hur[:,i])
        #bar_counter sets the distance between bars, the height of the bar is he avg of a column of all hurs/cases, make sure to set correct labels!
        ax1.bar(i+bar_counter,np.average(kh_over_km_average_all_hur[:,i]),width=0.2, \
                edgecolor='black', color=colors[PBL_counter],label=PBLS[PBL_counter], \
                    yerr=std_dev)
    bar_counter+=0.2
    PBL_counter+=1
    kh_over_km_average_all_hur=[]
x_ticks=[]
for i in range(len(CLS)):
    x_ticks.append(len(CLS)/10-0.5+i)

##### HERE SET THE XTICKS

ax1.set_xticks(x_ticks)
ax1.set_xticklabels(CLS)
ax1.set_title('Kh/Km avg first ~'+str(height_under_which_to_average))
ax1.yaxis.grid(True)

fig.suptitle(', '.join(HNS)+' -- '+', '.join(GSS), fontsize=16)


handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
fig.legend(by_label.values(), by_label.keys(), loc = 'upper center',ncol = 2, bbox_to_anchor=(0.65, 0.92, -0.3, 0),frameon = True)

plt.show()


        