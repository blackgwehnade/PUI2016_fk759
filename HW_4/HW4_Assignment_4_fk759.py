
# coding: utf-8

# In[1]:

from __future__ import print_function, division
import pylab as pl
import pandas as pd
import numpy as np
import csv
import StringIO
import requests
import zipfile
#imports downloader

get_ipython().magic('pylab inline')

import os
#this makes my plots pretty! but it is totally not mandatory to do it
import json


# In[2]:

A = '12348HJIUSDHFLASUGH'
A


# In[3]:

if os.getenv("PUIDATA") is None:
    print ("must set PUIDATA env variable")
    sys.exit()

def getCitiBikeCSV(datestring):
    '''Downloads citibike data and unzips it. If the data is downloaded by not unzippeds it zips it. Moves the data to $PUIDATA
    Arguments:
        date string as yyyymm
    '''
    print ("Downloading", datestring)
    ### First I will heck that it is not already there
    if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.csv"):
        if os.path.isfile(datestring + "-citibike-tripdata.csv"):
            # if in the current dir just move it
            if os.system("mv " + datestring + "-citibike-tripdata.csv " + os.getenv("PUIDATA")):
                print ("Error moving file!, Please check!")
        #otherwise start looking for the zip file
        else:
            if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.zip"):
                if not os.path.isfile(datestring + "-citibike-tripdata.zip"):
                    os.system("curl -O https://s3.amazonaws.com/tripdata/" + datestring + "-citibike-tripdata.zip")
                ###  To move it I use the os.system() functions to run bash commands with arguments
                os.system("mv " + datestring + "-citibike-tripdata.zip " + os.getenv("PUIDATA"))
            ### unzip the csv 
            os.system("unzip " + os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.zip")
            ## NOTE: old csv citibike data had a different name structure. 
            if '2014' in datestring:
                os.system("mv " + datestring[:4] + '-' +  datestring[4:] + 
                          "\ -\ Citi\ Bike\ trip\ data.csv " + datestring + "-citibike-tripdata.csv")
            os.system("mv " + datestring + "-citibike-tripdata.csv " + os.getenv("PUIDATA"))
    ### One final check:
    if not os.path.isfile(os.getenv("PUIDATA") + "/" + datestring + "-citibike-tripdata.csv"):
        print ("WARNING!!! something is wrong: the file is not there!")

    else:
        print ("file in place, you can continue")


# In[4]:

datestring = '201506'
getCitiBikeCSV(datestring)


# In[5]:

#!curl -O https://raw.githubusercontent.com/fedhere/PUI2016_fb55/master/HW4_fb55/getCitiBikeCSV.py


# In[6]:

df = pd.read_csv(os.getenv("PUIDATA") + "/" + datestring + '-citibike-tripdata.csv')
df.head()


# In[7]:

df.columns


# In[8]:

df['ageM'] = 2015 - df['birth year'][(df['usertype'] == 'Subscriber') & (df['gender'] == 1)]
df['ageF'] = 2015 - df['birth year'][(df['usertype'] == 'Subscriber') & (df['gender'] == 2)]


# In[9]:

df.head()


# In[10]:

df.describe()


# In[11]:

df['ageM'].dropna(inplace= True)
df['ageF'].dropna(inplace= True)


# In[12]:

bins = np.arange(10, 99, 5)
axM = df.ageM.groupby(pd.cut(df.ageM, bins)).agg([count_nonzero]).plot(kind='bar', 
                                                                legend=False)
axM.set_title("male riders")
axF = df.ageF.groupby(pd.cut(df.ageF, bins)).agg([count_nonzero]).plot(kind='bar',
                                                                legend=False)
axF.set_title("female riders")


# In[13]:

csM=df.ageM.groupby(pd.cut(df.ageM, bins)).agg([count_nonzero]).cumsum()

csF=df.ageF.groupby(pd.cut(df.ageF, bins)).agg([count_nonzero]).cumsum()

print (np.abs(csM / csM.max()-csF / csF.max()))

pl.plot(bins[:-1] + 5, csM / csM.max(), label = "M")
pl.plot(bins[:-1] + 5, csF / csF.max(), label = "F")
pl.plot(bins[:-1] + 5, np.sqrt(csF / csF.max() - csM / csM.max())**2, 'k-',
        label = "difference")
pl.xlabel("Age")
pl.ylabel("Normalized Cumulative Number")
pl.legend()


# In[14]:

import scipy.stats
ks = scipy.stats.ks_2samp(df.ageM, df.ageF)
print (ks)


# In[15]:

'''
The results of the the scripy KS test returns a p-value approaching 0.0,
which is strong evidence enough to reject the null hypothesis.
'''


# In[17]:

ageF = sort(df.ageF)
ageM = sort(df.ageM)

ageM = sort(df.ageM[:len(ageF)])


# In[18]:

scipy.stats.pearsonr(ageF, ageM)


# In[19]:

'''
The results of the the Pearson test returns a p-value approaching 0.0,
which is strong evidence enough to reject the null hypothesis.
'''


# In[20]:

scipy.stats.spearmanr(ageF,ageM)


# In[21]:

'''
The results of the the Spearman test returns a p-value approaching 0.0,
which is strong evidence enough to reject the null hypothesis.
'''


# In[ ]:



