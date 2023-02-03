from numpy.core.function_base import linspace
from Func_Extract_Data import Extract_by_name,Extract_Coordinates_2,Extract_Track_Data,flatten_the_curve
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec
#from Func_Map_Setting import map_setting
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs






Real_data_dir='/Users/lmatak/Desktop/leo_simulations/Real_Data'

Input_Dir = '/Users/lmatak/Desktop/leo_simulations/WRF_Output_PBLHS/diff_hpbls'
# Choose between : 'Dorian','Iota','Irma','Laura','Lorenzo','Maria','Matthew','Michael'
# for MYJ 'Maria','Dorian','Irma','Laura'
HN = 'Iota'
# Choose between : '2km', '4km', '8km', '16km', '32km'
GS = '32km'
# Choose between : 'NoTurb', 'Smag2D', 'TKE2D'
TM = 'NoTurb'
# Choose between : 'YSU_wrf_42',YSU_lin_63'
PBLS = ['YSU']
# PBLS = ['YSU_additional_changs']
				#######
				# MYJ #
				#######
# CLS = ['1.0','m_250','m_2000']
# CLS= ['1.0','m_akm_0.25','m_akm_4.0']
				#######
				# MYJ #
				#######
# CLS = ['1.0','250','2000']
CLS = ['1.0','xkzm_0.25'] #,'el_2.0','el_4.0','vonkarman_0.2','vonkarman_0.6','q_4.0']
# CLS=['1.0','lvl_2','lvl_4','lvl_8']
# CLS = ['1.0','lvl_2','lvl_4','lvl_8']


Time_idx = '0'

fig = plt.figure(figsize=(18, 9))
# fig.tight_layout()


gs = gridspec.GridSpec(2,2,figure=fig,wspace=0.3,hspace=0.6)
#normaln ones
ax1 = fig.add_subplot(gs[:2,0])
ax2 =fig.add_subplot(gs[:2,1])





colors = ['blue', 'orange', 'red', 'green', 'purple', 'magenta','yellow']
line_stylez= ['-','--','-.']
c=0

Input_Dir_1 = Input_Dir + '/' + HN + '/' + GS + '/' + TM + '/Standard/'
# os.chdir(Input_Dir_1)
print('Input dir: ',Input_Dir_1)

Times = [0,6, 12, 18, 24, 30, 36, 42, 48,54,60,64,72,80]
csv_files=[]
dummy_list=[]
# # # #REAL DATA FOR HURRICANE TRACK#




PBL_counter=0
for PBL in PBLS:
	cls_counter=0
	for CL in CLS:

		#by hurricane setting you define the name of the csv file e.g. /Irma_32km_NoTurb_YSU_hpbl_250.csv/
		Hurricane_Setting = HN + '_' + GS + '_' + TM + '_' + PBL +'_hpbl_'+CL +'.csv'		
		# print(Hurricane_Setting)
		csv_file = (Input_Dir_1+Hurricane_Setting)
		lvl_heights=[]
		lvl_heights = Extract_by_name(csv_file, lvl_heights, 'lvl_heights')
		el_pbl=[]
		tke_pbl=[]
		el_pbl= Extract_by_name(csv_file, el_pbl, 'EL_pbl')
		tke_pbl=Extract_by_name(csv_file, tke_pbl, 'TKE_pbl')



		
		
		# Times=linspace(0,Times[len(Real_slp)-1],num=len(Eye_Lats))


		ax1.plot(el_pbl[0:15], lvl_heights[0:15], color=colors[c], linestyle=line_stylez[PBL_counter], marker='.', 
			linewidth='1',markersize='7', label= (PBL+'-'+CLS[cls_counter]))
		ax1.set_title('EL_pbl')



		# min_slp_simulation=flatten_the_curve(min_slp_simulation)
		ax2.plot(tke_pbl[0:15], lvl_heights[0:15], color = colors[c] , linestyle=line_stylez[PBL_counter],
		linewidth='2', marker='.', markersize='10',label=(PBL+' hpbl - '+CLS[cls_counter]))
		ax2.set_xlabel('tke_pbl')
		# ax2.set_ylabel('[mb]')
		ax2.set_title('TKE')
							

		

		cls_counter+=1
		c+=1
	PBL_counter+=1
xticks=[]
# for i in range(len(el_pbl)):
# 	time_idx=i*6
# 	xticks.append(time_idx)

handles, labels = fig.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
# ax1.set_xticks(xticks)
# ax2.set_xticks(xticks)


fig.legend(by_label.values(), by_label.keys(), loc = 'upper center', mode='expand',
			 ncol = 3, bbox_to_anchor=(0.65, 0.96, -0.3, 0),frameon = False)
fig.suptitle(HN+' - '+GS+' - '+TM+' - '+PBL, fontsize=18)
plt.show()