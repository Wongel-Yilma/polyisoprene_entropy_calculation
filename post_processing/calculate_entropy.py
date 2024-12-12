
import numpy as np
from scipy.integrate import trapezoid
import seaborn as sns

#######################################
######## Loading postprocessed data####
####################################### 

data_290 = np.load('data_290K.npy')
data_300 = np.load('data_300K.npy')
data_310 = np.load('data_310K.npy')


mol = 1.22e-20
t = np.linspace(0,95,20)



P_ave = (data_300[:,6] + data_290[:,6]+data_310[:,6])/3
volume = np.hstack((data_290[:,10:11],data_300[:,10:11],data_310[:,10:11]))

dVdT = np.gradient(volume,axis = 1)

#######################################
######## Calculating Entropy ##########
#######################################

dVdT_ave = np.zeros_like(P_ave)
product = np.zeros_like(P_ave)
dP = np.zeros_like(P_ave)
for i in range(len(dP)):
    dP[i] = P_ave[i]-P_ave[0]
    if i==0: dVdT_ave[i] = dVdT[0,1]
    else: dVdT_ave[i] = (dVdT[i-1,1] + dVdT[i,1])/2
    product[i] = dVdT_ave[i] *dP[i] 
Delta_S  = np.cumsum(product)*10e-25/mol
l0 = data_300[0,3]

# plt.plot(data_290[:,0],dVdT_ave)
experimetal_value = -(data_300[:,3]/l0 -1)**2

#####################################
########### Plotting ################
#####################################

import matplotlib.pyplot as plt
from matplotlib import rcParams

# figure size in inches
rcParams['figure.figsize'] = 24,16
plt.rcParams.update({'font.size': 24}) 
sns.set_theme(style="darkgrid", palette="muted",font_scale=3)
fig, ax1 = plt.subplots()
ax1 = sns.lineplot(x=t, y=data_290[:,6], label=r'$290K$', color='cornflowerblue', ax=ax1)
sns.lineplot(x=t, y=data_300[:,6], label=r'$300K$', color='plum', ax=ax1)
sns.lineplot(x=t, y=data_310[:,6], label=r'$310K$', color='salmon', ax=ax1)
ax1.set_xlabel(r"Time, $ps$")
ax1.set_ylabel(r"Pressure, $atm$")
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)
plt.savefig("pressure.png", dpi=300)
plt.show()



fig, ax4 = plt.subplots()
ax4 = sns.lineplot(x=data_290[:,11], y=Delta_S, color='cornflowerblue',label = 'Calculated from MD')
ax4.set_xlabel(r"Stain, $\epsilon_{xx}$")
ax4.set_ylabel(r"Change in Entropy, $\Delta s(\frac{J}{K\cdot mol})$")
ax4.legend(loc='lower left')
ax5 = ax4.twinx()
ax5.grid(False)
sns.lineplot(x=data_290[:,11], y=experimetal_value, label='Ideal Elastomer', color='forestgreen', ax=ax5)
ax5.set_ylabel(r"$\Delta S/k L_0$")
plt.savefig("entropy_change.png", dpi=300)
plt.show()


