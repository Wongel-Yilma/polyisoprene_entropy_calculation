import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

#############################
### Loading the data  ######
############################
with open('./stretch_3.log','r')as f:
    lines = f.readlines()

description = lines[27].split()
data_lines = lines[28:2029]
data = np.zeros((len(data_lines), len(description)))
for i in range(len(data_lines)):
    data[i,:]= [float(value) for value in data_lines[i].rsplit()]

data_red = np.zeros((data.shape[0]//100, data.shape[1]))
l0 = data[0,3:6]
data_red[0,7] = 0
#############################
#### Calculating strain #####
#############################
strain = np.zeros((data.shape[0]//100,3))
for i in range(data_red.shape[0]):
    start, stop = i*100, (i+1)*100
    data_red[i,1:] = np.mean(data[start: stop+1,1:],axis=0)
    data_red[i,0] = i*100
    strain[i,:] = (data_red[i,3:6]-l0)/l0
    
t = np.linspace(0,95,20)
np.save('data_290K.npy',np.hstack((data_red,strain)))

print(description)

###############################
######## Plotting #############
###############################

plt.rcParams.update({'font.size': 18}) 
from matplotlib import rcParams

# figure size in inches
rcParams['figure.figsize'] = 16,24
sns.set_theme(style="darkgrid", palette="muted",font_scale=2)

# Plot 1: Strain and Volume vs. Time
fig, ax1 = plt.subplots(figsize=(8, 6))
ax1 = sns.lineplot(x=t, y=strain[:, 0], label=r'$\epsilon_{xx}$', color='cornflowerblue', ax=ax1)
sns.lineplot(x=t, y=strain[:, 1], label=r'$\epsilon_{yy}$', color='plum', ax=ax1)
sns.lineplot(x=t, y=strain[:, 2], label=r'$\epsilon_{zz}$', color='salmon', ax=ax1)

# Customize primary y-axis
ax1.set_xlabel(r"Time, $ps$")
ax1.set_ylabel(r"Strain, $\epsilon$")
ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=3)

# Add secondary y-axis for volume
ax2 = ax1.twinx()
sns.set_theme(style="darkgrid", palette="muted",font_scale=2)

sns.lineplot(x=t, y=data_red[:, 10], label='Volume', color='forestgreen', ax=ax2)
ax2.set_ylabel(r'Volume, $\mathring{A}^3$', color='forestgreen')
ax1.grid(True)  # Enable grid for primary y-axis
ax2.grid(False)
plt.savefig("strain_volume.png", dpi=300)
plt.show()

# Plot 2: Stress-Strain Curve
fig, ax3 = plt.subplots(figsize=(8, 6))
ax3 = sns.lineplot(x=strain[:, 0], y=-data_red[:, 7] / 10000, color='cornflowerblue', ax=ax3)

# Customize stress-strain plot
ax3.set_xlabel(r"Strain, $\epsilon_{xx}$")
ax3.set_ylabel(r"Stress, $\tau_{xx}$ (GPa)")
ax3.text(0.35, 0.05, r'Strain rate, $\dot{\epsilon}_{xx}=1\times10^{10}/s$', fontsize=16)

plt.savefig("stress_strain.png", dpi=300)
plt.show()
