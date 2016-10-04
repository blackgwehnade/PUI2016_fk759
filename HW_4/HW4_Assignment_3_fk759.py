
# coding: utf-8

# # August 2015 
# # Modified September 2016
# # Author: FBB
# 
# # reproduce the result in http://www.mdrc.org/sites/default/files/What%20Strategies%20Work%20for%20the%20Hard%20FR.pdf 
# 

# In[1]:

import os
import sys
import numpy as np
import pylab as pl
import json
import os
get_ipython().magic('pylab inline')



# In[2]:

Image(filename='../plotsforclasses/NYCReentryprogram.png')


# # NULL HYPOTHESIS: the % of former prisoners employed after release is the same or lower for candidates who participated in the program as for the control group, significance level p=0.05

# # $H_0: P_0 - P_1 \geq$    0
#     
# # $H_a: P_0 - P_1 $< 0    
#     
#     
# # $\alpha$ = 0.05    
# 
# ## this is a TEST OF PROPORTIONS. we use the Binomial distribution since it is a yes/no (bernulli) test for each subject: the former inmate was or was not ever employed in a CEO transitional job (second row in the table above):
# # $P_0=0.035, P_1=0.701$

# In[3]:


alpha=0.05
'''
We like fractions better then percentages. 
As a rule of thumb, either use fractions or counts
'''
P_0 = 3.5*0.01 
P_1 = 70.1*0.01

if P_0-P_1 >= 0:
    # we are done
    print ("the Null holds")
else:
    print ("we must assess the statistical significance")

n_0 = 409
n_1 = 564

#lets get the counts by multiplying by the sample size
Nt_0 = P_0 * n_0
Nt_1 = P_1 * n_1


# # 2 samples, categorical data
# # TWO OPTIONS z test, or chi-square test.  

# # START WITH Z TEST
# 
# ## the z test compares the stanrard deviation of the expected distribution and the observed result. it tells you literally how many standard deviations from the tail an observation is, under the _assumption of normality
# must define the sample standard deviation 

# In[4]:

#define the sample proportion first
sp = (P_0 * n_0 + P_1 * n_1) / (n_1 + n_0)
print (sp)


# # standard deviation of the sampling distribution the distribution is Binomial, the binomail stdev is 
# 
# (see a proof here!: http://stats.stackexchange.com/questions/29641/standard-error-for-the-mean-of-a-sample-of-binomial-random-variables!): 
# 
# $\sqrt{\frac{p(1 - p)}{n}}$
# 
# for 2 samples this becomes 
# 
# $\sqrt{ \frac{ \hat{p}(1 - \hat{p})} {n1} + \frac{ \hat{p}(1 - \hat{p})} {n1} }$
# 
# cfr: page 138 of Statistics in a Nutshell, eq. 5.12 and here http://stattrek.com/hypothesis-test/difference-in-proportions.aspx?Tutorial=AP
# 
# 

# In[5]:

Image("../plotsforclasses/SiNS5.13.png")


# Note that in the Image above, taken from the online version of the book, $\bar{x}$  should be  $\hat{p}$!!

# In[6]:

# I am goonna create a little one line function to calculate the standard dev, 
# it is not really needed, but just to show you how you do such a thing
sp_stdev = lambda p, n: np.sqrt( p * ( 1 - p ) / n[0] +  p * ( 1 - p ) / n[1]  )


sp_stdev_2y = sp_stdev(( Nt_0 + Nt_1) / (n_0 + n_1), [n_0, n_1])
print (P_0, n_0, n_1, sp_stdev_2y)


# # z score: how many standard deviation away from the population parameter is my statistic?
# 
# # $z=\frac{P_1-P_0}{\sigma}$

# In[14]:

zscore = lambda p0, p1, s : (p0 - p1) / s
z_2y = zscore(P_1, P_0, sp_stdev_2y)
print (z_2y)


# note that using p0-p1 or p1-p0 at the numerator is equivalent because the standardizes normal value of z has mean 0 (see image below) so that we can use the absolute value of the z score, or equivalently look for $P[Z<z]$ if z is positive, and $P[Z>z]$ if z is negative.

# In[15]:

Image('http://intersci.ss.uci.edu/wiki/images/3/3a/Normal01.jpg')


# ## if $p<\alpha$ : reject H0
# 
# ## IMPORTANT!! note that this P in the bottom line of the table is not the p-value, but 
# ## p-value = 1-P

# In[18]:

## p-value for employment after 2 years: 
## since the largest number we read off the table for alpha=0.05 is smaller then the value for our statistic 
## our p-value will be smaller then calculated using .9998
## thus using 0.9998 is a **conservative** approach. 

p_2y = 1 - 0.9998


def report_result(p,a):
    print ('is the p value {0:.2f} smaller than the critical value {1:.2f}? '.format(p,a))
    if p < a:
        print ("YES!")
    else: 
        print ("NO!")
    
    print ('the Null hypothesis is {}'.format( 'rejected' if p < a  else 'not rejected') )

    
report_result(p_2y,alpha)


# # !!!!!!!!TODO FOR YOU
# 

# ## what if we used the values for where the former inmate was or was not "Convicted of a felony" (row 10) in the Recidivism (Years 1-3)?
# 
# # Null hypothesis?
# # $H_0$?
# # $H_a$?
# 
# # $P_0 = ??, P_1= ??$

# # look up data table and insert the appropriate values to get the appropriate result! you can use the functions I defined above, with different arguments. 

# In[15]:

import os
import sys
import numpy as np
import pylab as pl
import json
import os
get_ipython().magic('pylab inline')


# In[24]:

'''
H0: The level of employment for convicts after three years has 
been reduced or held the same.
H1: The level of employment for convicts after three years has 
increased significantly.
'''

P_0 = 11.7 * 0.01
P_1 = 10.0 * 0.01

if P_0 - P_1 >= 0:
    print ("The Null holds.")
else:
    print("We must now assess the statistical significance.")
    
n_0 = 409
n_1 = 568

Nt_0 = P_0 * n_0
Nt_1 = P_1 * n_1


# In[25]:

sp = (P_0 * n_0 + P_1 * n_1) / (n_1 + n_0)
print (sp)


# In[29]:

sp_stdev = lambda p, n: np.sqrt( p * ( 1 - p ) / n[0] +  p * ( 1 - p ) / n[1]  )


sp_stdev_3y = sp_stdev(( Nt_0 + Nt_1) / (n_0 + n_1), [n_0, n_1])
print (P_0, n_0, n_1, sp_stdev_3y)


# In[30]:

zscore = lambda p0, p1, s : (p0 - p1) / s
z_3y = (((zscore(P_1, P_0, sp_stdev_3y))**2)**0.5)
print (z_3y)


# In[32]:

p_3y = 1 - 0.7995

def report_result(p, a):
    print ('Is the p-value of {0:.2f} smaller than the critical value of {1:.2f}?'.format(p, a))
    if p < a:
        print ("Yes")
    else:
        print ("No")
        
    print ('The Null Hypothesis is {}'.format('rejected.' if p < a  else 'not rejected.'))

    
report_result(p_3y,alpha)


# # Now lets do it with the $\chi^2$ test

# ## this analysis can also be done with the $\chi^2$ test, and the  $\chi^2$ distribution, 
# ## see  [A. Marengo](http://www.csun.edu/~amarenco/Fcs%20682/When%20to%20use%20what%20test.pdf) on how to choose a test and "Statistics In a Nutshell Chapter 4", or http://math.hws.edu/javamath/ryan/ChiSquare.html (if you are really just interested in the formula at face value)

# ### The chisq statistics tests the statistics calculated as :
# 
# $$\chi^2 = \Sigma \frac{(observation - expectation)^2}{expectation}$$
# 
# ### against a chi sq distribution.
# ### If we talk about sample fractions  that is 
# 
# $$\chi^2 = \Sigma \frac{(f_{observed} - f_{expectated})^2}{f_{expected}}$$
# 
# ### turns out this quantity is distributed according to a chi square distribution, so if i get the $\chi^2$ statistics i can compare it to the full chisq distribution and see how far in the tail it is
# 
# ### The trickiest part (but not that tricky) is to figure out how to construct the table of values. please see Statistics In a Nutshell Chapter 4, for our data for example: Thisis called a CONTINGENCY TABLE

# |                 |     success         | failure|    |               
# |-----------------|:-------------------:|:-------------------:|---------------------------|
# | test sample     | number of successes in test    | number of failures in test    | number members of test sample |
# | control sample  | number of successes in control | number of failures in control | number members of control sample| 
# |                 | total successes                |  total failures               | number of all members         |
# 
# |employed in subsadized job |     employed          | not employed     |                   
# |---------------------------|:---------------------:|------------------|---------------------------|
# | test sample               | $0.701*564$           | $0.299*564$      | 564                       |
# | control sample            | $0.035*409$           | $0.965*4.09$     | 409                       |
# |                           |                       |                  |                           |
# | total                     | 409.679               |  562.912         | 973                       |

# # the expected ratio is the product of the total of all rows and all columns, devided by the total

# # expected = $\frac{row tot * col tot}{total}$

# In[33]:

chisqstat= lambda N, values, expect_num : ((values[0][0] * values[1][1]
                                            -values[0][1] * values[1][0])**2) * N / expect_num
Ntot = 973 # a + b + c + d = tot
expected_num = 564 * 409 * 409.679 * 562.912
sample_values = [[0.701 * 564, 0.299 * 564], [0.0305 * 409, 0.965 * 409]]
 

print (chisqstat(Ntot,  sample_values, expected_num))


# # This number must be compared to the chi sq distribution. 
# # You must calculate the number of degrees of freedom forthis experiment. 
# # Generally: DOF = Number of observations - number of Independent Variables
# # so here DOF = 1. Now you can look at the table below and draw conclusions about the rejection of the Null
Ntot = ...
expected = ...
sample_values = ...


chisqstat=...
print chisqstat
# In[11]:

Image("http://passel.unl.edu/Image/Namuth-CovertDeana956176274/chi-sqaure%20distribution%20table.PNG")


# 432 is hella larger then 3.84
# 
# why am i mentioning 3.84?
# 
# how does the 6mo chi square statistic that you derived compare?
# 
# please  state what that means in terms of your hypothesis in a markdown cell below!

# # !!!!!! TODO FOR YOU!
# # lets see what the chi sq statistics says about the conviction for fellonies (row 10)

# ## fill in the contingency table below
# 
# |convicted of a fellony     |     employed   | not employes   |                   
# |---------------------------|----------------|------------------|---------------------------|
# | test sample               | 0.100 * 568    |  0.900 * 568    | 568                         |
# | control sample            | 0.117 * 409    |  0.883 * 409    | 409                      |
# |                           |                |                  |                           |
# | total                     | 104.653        | 872.347          | 977         |

# In[34]:

chisqstat= lambda N, values, expect_num : ((values[0][0] * values[1][1]
                                            -values[0][1] * values[1][0])**2) * N / expect_num
Ntot = 977 # a + b + c + d = tot
expected_num = 568 * 409 * 104.653 * 872.347
sample_values = [[0.100 * 568, 0.900 * 568], [0.117 * 409, 0.883 * 409]]
 

print (chisqstat(Ntot,  sample_values, expected_num))


# 

# In[ ]:

'''
According to our result, the probability of a larger value of X-squared is between 25 and 50%.
This means that we will most likely not be able to reject the null.
'''


