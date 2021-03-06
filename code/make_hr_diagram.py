import numpy as np
import matplotlib.pyplot as plt
from astropy.io import ascii
from scipy.stats import gaussian_kde
from scipy import stats
import pandas as pd
import math
# plt.rc('font', family='serif')
# plt.rc('text', usetex=True)
plt.rc('font', size=15)                  # controls default text sizes
plt.rc('axes', titlesize=15)             # fontsize of the axes title
plt.rc('axes', labelsize=15)             # fontsize of the x and y labels
plt.rc('xtick', labelsize=15)            # fontsize of the tick labels
plt.rc('ytick', labelsize=15)            # fontsize of the tick labels
plt.rc('axes', linewidth=1)    

gaia     =ascii.read('/Users/maryumsayeed/Desktop/HuberNess/mlearning/powerspectrum/DR2PapTable1.txt',delimiter='&')
kepler_catalogue=pd.read_csv('/Users/maryumsayeed/Desktop/HuberNess/mlearning/hrdmachine/GKSPC_InOut_V4.csv')#,skiprows=1,delimiter=',',usecols=[0,1])

gaia_stars=np.loadtxt('LLR_gaia/pande_final_sample_full.txt',usecols=[0],dtype=str)
ast_stars=np.loadtxt('LLR_seismic/astero_final_sample_full.txt',usecols=[0],dtype=str)

gaia_teff=[]
gaia_lum=[]
for file in gaia_stars:
	kic=file[0:-3].split('/')[-1].split('-')[0].split('kplr')[-1]
	kic=int(kic.lstrip('0'))
	try:
		row=kepler_catalogue.loc[kepler_catalogue['KIC']==kic]
		t  =row['iso_teff'].item()
		r  =row['iso_rad'].item()
	except:
		idx=np.where(gaia['KIC']==kic)[0]
		t=gaia['teff'][idx][0]
		r=gaia['rad'][idx][0]
	if math.isnan(r) is True:
		idx=np.where(gaia['KIC']==kic)[0]
		t=gaia['teff'][idx][0]
		r=gaia['rad'][idx][0]
	l  =r**2.*(t/5777.)**4.
	gaia_teff.append(t)
	gaia_lum.append(l)


ast_teff=[]
ast_lum=[]
for file in ast_stars:
	kic=file[0:-3].split('/')[-1].split('-')[0].split('kplr')[-1]
	kic=int(kic.lstrip('0'))
	try:
		row=kepler_catalogue.loc[kepler_catalogue['KIC']==kic]
		t  =row['iso_teff'].item()
		r  =row['iso_rad'].item()
	except:
		idx=np.where(gaia['KIC']==kic)[0]
		t=gaia['teff'][idx][0]
		r=gaia['rad'][idx][0]
	if math.isnan(r) is True:
		idx=np.where(gaia['KIC']==kic)[0]
		t=gaia['teff'][idx][0]
		r=gaia['rad'][idx][0]
	l  =r**2.*(t/5777.)**4.
	ast_teff.append(t)
	ast_lum.append(l)

print('GAIA')
print(np.min(gaia_teff),np.max(gaia_teff))
print(np.min(gaia_lum),np.max(gaia_lum))
print('SEISMIC')
print(np.min(ast_teff),np.max(ast_teff))
print(np.min(ast_lum),np.max(ast_lum))

ldot='L$_{\\odot}$'
fig=plt.figure(figsize=(5,8))
fig.text(0.01, 0.5, 'Luminosity [{}]'.format(ldot), va='center', rotation='vertical')
ax = fig.add_subplot(111)    
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.set_yticks([])
ax.set_xticks([])
# ax.set_ylabel('Luminosity [{}]'.format(ldot),labelpad=30)

ax1 = fig.add_subplot(2,1,2)
numBins=40
hb = ax1.hexbin(gaia_teff,gaia_lum,gridsize=numBins,bins='log',yscale='log',lw=0.5,edgecolor='face',cmap='viridis',mincnt=1)
ax1.set_ylim([0.15,200])
ax1.set_xlim([4225,8200])
ax1.set_yscale("log")

STR='Gaia: {} stars'.format('{:,.0f}'.format(len(gaia_teff)))
t=ax1.text(0.03,0.93,s=STR,color='k',ha='left',va='center',transform = ax1.transAxes,fontsize=11)
t.set_bbox(dict(facecolor='none',edgecolor='none'))#, alpha=0.5, edgecolor='red'))
cb = plt.colorbar(mappable=hb,pad=0.01)#,format='%.0e')
cb.set_label('Count',fontsize=12)
cb.ax.tick_params(labelsize=12)
ax1.tick_params(which='major',axis='both')
plt.gca().invert_xaxis()

ax2 = fig.add_subplot(2,1,1)
numBins=70
hb = ax2.hexbin(ast_teff,ast_lum,gridsize=numBins,bins='log',yscale='log',lw=1,edgecolor='face',cmap='viridis',mincnt=1)
ax2.set_ylim([0.05,4200])
ax2.set_xlim([3000,7100])
ax2.set_yscale("log")
ax1.set_xlabel('Effective Temperature [K]')

STR='Seismic: {} stars'.format('{:,.0f}'.format(len(ast_teff)))
t=ax2.text(0.03,0.94,s=STR,color='k',ha='left',va='center',transform = ax2.transAxes,fontsize=11)
t.set_bbox(dict(facecolor='none',edgecolor='none'))#, alpha=0.5, edgecolor='red'))
cb = plt.colorbar(mappable=hb,pad=0.01)#,format='%.0e')
# cb=fig.colorbar(hb,ax=ax2)
#cb.set_label('$\log_{10}(\mathrm{Count})$',fontsize=12)
cb.set_label('Count',fontsize=12)
cb.ax.tick_params(labelsize=12)
ax2.tick_params(which='major',axis='both')
plt.gca().invert_xaxis()
plt.tight_layout()
plt.savefig('Both_HR_Diagrams.png',dpi=100,bbox_inches='tight')
plt.show(False)


# just in case:
# xy = np.vstack([gaia_teff,gaia_lum])
# z_gaia = gaussian_kde(xy)(xy)

