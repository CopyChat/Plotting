#!/usr/bin/env python

########################################
#Globale Karte fuer tests
# from Rabea Amther
########################################
# http://gfesuite.noaa.gov/developer/netCDFPythonInterface.html

import math
import numpy as np
import pylab as pl
import Scientific.IO.NetCDF as IO
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.lines as lines
from mpl_toolkits.basemap import Basemap , addcyclic
from matplotlib.colors import LinearSegmentedColormap
import textwrap

pl.close('all')

########################## for CMIP5 charactors
DIR='/Users/tang/climate/CMIP5/monthly/tas/'
VARIABLE='tas'
PRODUCT='Amon'
ENSEMBLE='r1i1p1'

AbsTemp=273.15
#AbsTemp=0
RefTemp=5
CRUmean=8.148 #1900-2100 land

TargetModel=[\
        #'CanESM2',\
        #'BCC-CSM1.1',\
        #'CCSM4',\
        #'CNRM-CM5',\
        #'CSIRO-Mk3.6.0',\
        #'EC-EARTH',\
        #'GFDL-ESM2G',\
        #'GFDL-ESM2M',\
        #'GISS-E2-H',\
        'GISS-E2-R',\
        #'HadGEM2-CC',\
        'HadGEM2-ES',\
        #'INM-CM4',\
        #'IPSL-CM5A-LR',\
        #'IPSL-CM5A-MR',\
        #'MIROC-ESM-CHEM',\
        'MIROC-ESM',\
        #'MIROC5',\
        #'MPI-ESM-LR',\
        #'MRI-CGCM3',\
        #'NorESM1-M',\
        #'MPI-ESM-LR',\
        ]

COLORtar=['darkred','black','deeppink','orange',\
        'orangered','yellow','gold','brown','chocolate',\
        'green','yellowgreen','aqua','olive','teal',\
        'blue','purple','darkmagenta','fuchsia','indigo',\
        'dimgray','black','navy']

COLORall=['darkred','darkblue','darkgreen','deeppink',\
        'red','blue','green','pink','gold',\
        'lime','lightcyan','orchid','yellow','lightsalmon',\
        'brown','khaki','aquamarine','yellowgreen','blueviolet',\
        'snow','skyblue','slateblue','orangered','dimgray',\
        'chocolate','teal','mediumvioletred','gray','cadetblue',\
        'mediumorchid','bisque','tomato','hotpink','firebrick',\
        'Chartreuse','purple','goldenrod',\
        'black','orangered','cyan','magenta']
linestyles=['_', '_', '_', '-', '-',\
    '-', '--','--','--', '--',\
    '_', '_','_','_',\
    '_', '_','_','_',\
    '_', '-', '--', ':','_', '-', '--', ':','_', '-', '--', ':','_', '-', '--', ':']
#================================================ CMIP5 models
# for rcp8.5 
# ls -l | awk '{printf "999%s998,\\\n",$NF}' | sort -n
modelist2=[\
        'ACCESS1-0',\
        'ACCESS1-3',\
        'BNU-ESM',\
        'CCSM4',\
        'CESM1-BGC',\
        'CESM1-CAM5',\
        'CMCC-CM',\
        'CMCC-CMS',\
        'CNRM-CM5',\
        'CSIRO-Mk3-6-0',\
        'CanESM2',\
        'EC-EARTH',\
        'FIO-ESM',\
        'GFDL-CM3',\
        'GFDL-ESM2G',\
        'GFDL-ESM2M',\
        'GISS-E2-R',\
        'HadGEM2-AO',\
        'HadGEM2-CC',\
        'HadGEM2-ES',\
        'IPSL-CM5A-LR',\
        'IPSL-CM5A-MR',\
        'IPSL-CM5B-LR',\
        'MIROC-ESM-CHEM',\
        'MIROC-ESM',\
        'MIROC5',\
        'MPI-ESM-LR',\
        'MPI-ESM-MR',\
        'MRI-CGCM3',\
        'NorESM1-M',\
        'NorESM1-ME',\
        'bcc-csm1-1-m',\
        'bcc-csm1-1',\
        'inmcm4',\
        ]
print "==============================================="


#=================================================== define the Plot:

fig1=plt.figure(figsize=(16,9))
ax = fig1.add_subplot(111)
plt.xlabel('Year',fontsize=16)  
#plt.ylabel('Global Surface Downwelling Solar Radiation Change (W/m2)',fontsize=16)
plt.ylabel('Global Surface Temperature Changes ($^\circ$C)',fontsize=16)
plt.title("Global Surface Tempereture Changes simulated by CMIP5 models",fontsize=18)
#plt.title('Global Surface Downwelling Solar Radiation Changes simulated by CMIP5 models (W/m2)',fontsize=18)
plt.ylim(-2,6)
plt.xlim(1961,2099)
plt.grid()

plt.xticks(np.arange(1961, 2093+10, 20))
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)

# vertical at 2005
plt.axvline(x=2005.5,linewidth=2, color='gray')
plt.axhline(y=0,linewidth=2, color='gray')

#plt.plot(x,y,color="blue",linewidth=4)
########################## for historical
########################## for historical

print "========== for rcp85 ==============="

EXPERIMENT='historical-rcp85'
PRODUCT='Amon'
ENSEMBLE='r1i1p1'

TIME='196101-209912'

filetag="globalmean"

YEAR=range(1960,2099)
Nmonth=1668
SumTemp=np.zeros(Nmonth/12)
K=0

for Model in modelist2:
#define the K-th model input file:
    K=K+1 # for average 
    infile1=DIR+'rcp8.5'+'/'+Model+'/'\
            +VARIABLE+'_'+PRODUCT+'_'+Model+'_'+EXPERIMENT+'_'+ENSEMBLE+'_'+TIME+'.'+filetag+'.nc'
                #an example: tas_Amon_CanESM2_historical-rcp85_r1i1p1_200601-210012.globalmean.nc & \
                    #this file was copied locally for tests in this book
    print('the file is == ' +infile1)

    #open input files
    infile=IO.NetCDFFile(infile1,'r')

    # read the variable tas
    TAS=infile.variables[VARIABLE][:,:,:].copy()
    print 'the variable tas ===============: ' 
    print TAS

    # calculate the annual mean temp:
    TEMP=range(0,Nmonth,12) 
    for j in range(0,Nmonth,12):
        TEMP[j/12]=np.mean(TAS[j:j+11][:][:])-AbsTemp

    print " temp ======================== absolut"
    print TEMP

    # reference temp: mean of 1996-2005
    RefTemp=np.mean(TEMP[len(TEMP)-94-10+1:len(TEMP)-94])

    if K==1:
        ArrRefTemp=[RefTemp]
    else:
        ArrRefTemp=ArrRefTemp+[RefTemp]
        print 'ArrRefTemp ========== ',ArrRefTemp

    TEMP=[t-RefTemp for t in TEMP]
    print " temp ======================== relative to mean of 1986-2005"
    print TEMP

    ##quit()
    # for std

    # get array of temp K*TimeStep
    if K==1:
        ArrTemp=[TEMP]
    else:
        ArrTemp=ArrTemp+[TEMP]


    SumTemp=SumTemp+TEMP
    print SumTemp

#=================================================== to plot
    print "======== to plot =========="
    print len(TEMP)

    print 'NO. of year:',len(YEAR)
    #quit()

    #plot only target models
    if  Model in TargetModel:
        plt.plot(YEAR,TEMP,\
                label=Model,\
                #linestyles[TargetModel.index(Model)],\
                color=COLORtar[TargetModel.index(Model)],\
                linewidth=2)




    #if Model=='CanESM2':
        #plt.plot(YEAR,TEMP,color="red",linewidth=1)
    #if Model=='MPI-ESM-LR':
        #plt.plot(YEAR,TEMP,color="blue",linewidth=1)
    #if Model=='MPI-ESM-MR':
        #plt.plot(YEAR,TEMP,color="green",linewidth=1)

#=================================================== for ensemble mean
AveTemp=[e/K for e in SumTemp]
ArrTemp=list(np.array(ArrTemp))
print 'shape of ArrTemp:',np.shape(ArrTemp)
StdTemp=np.std(np.array(ArrTemp),axis=0)
print 'shape of StdTemp:',np.shape(StdTemp)

print "ArrTemp ========================:"
print ArrTemp

print "StdTemp ========================:"
print StdTemp

# 5-95% range ( +-1.64 STD)
StdTemp1=[AveTemp[i]+StdTemp[i]*1.64 for i in range(0,len(StdTemp))]
StdTemp2=[AveTemp[i]-StdTemp[i]*1.64 for i in range(0,len(StdTemp))]

print "Model number for historical is :",K

print "models for historical:";print  modelist2


plt.plot(YEAR,AveTemp,label='ensemble mean',color="black",linewidth=4)
plt.plot(YEAR,StdTemp1,color="black",linewidth=0.1)
plt.plot(YEAR,StdTemp2,color="black",linewidth=0.1)
plt.fill_between(YEAR,StdTemp1,StdTemp2,color='black',alpha=0.3)



# draw NO. of model used:
plt.text(2015,2,str(K)+' models',size=16,rotation=0.,
        ha="center",va="center",
        #bbox = dict(boxstyle="round",
            #ec=(1., 0.5, 0.5),
            #fc=(1., 0.8, 0.8),
            )


print "==============================================="
plt.legend(loc=2)
plt.show()
quit()

