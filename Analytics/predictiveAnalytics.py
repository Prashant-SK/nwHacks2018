# -*- coding: utf-8 -*-
"""
predictiveAnalytics.py: Script to analyze a patient's self reporting history to
generate statistcs for predictive analysis
"""
import Tkinter
import tkMessageBox
import tkFileDialog
import pandas as pd
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
import os

fileName = 'selfReportData.csv'
peerFileName = 'referenceStatsP.csv'
academicFileName = 'referenceStatsA.csv'
selfHarmFileName = 'referenceStatsSH.csv'

pData = pd.read_csv(fileName)
refDataP = pd.read_csv(peerFileName)
refDataA = pd.read_csv(academicFileName)
refDataSH = pd.read_csv(selfHarmFileName)


markerData = pData
pData['depEp'] = 0
pData['depSum'] = 0
pData['weightDiff'] = float(0)
pData['Self-Harm Probability'] = float(0)
pData['Academic Struggle Probability'] = float(0)
pData['Peer Conflict Probability'] = float(0)

# Changing date to datetime format
for x in range (0, len(pData.index)):
    tempVal = pd.to_datetime(str(pData['Date'][x]), format = '%Y%m%d')
    pData['Date'][x] = tempVal
         
numDepEps = 0
depEpStreak = 0

# Converting weight to weight change
# First weight has no reference, so is set as zero change

for i in range (1, len(pData.index)):
    pData['weightDiff'][i] = pData['Weight'][i] - pData['Weight'][i-1]

# Adding column to sum days with more than desp5 depressive symptoms present
for i in range (0, len(pData.index)):
    pData['depSum'][i] = sum([(pData['Mood'][i] < 5 ),
                              (pData['Energy'][i] < 5 ),
                              (pData['Concentration'][i] < 5 ),
                              (pData['Interest In Activities'][i] < 5 ),
                              (pData['Agitation'][i] > 5 ),
                              (pData['Guilt'][i] > 5 ),
                              (pData['Suicidality'][i] > 5),
                              (pData['weightDiff'][i] < 0)])
    
    # If more than 5 symptoms present, guidelines indicate depressive episode
    if pData['depSum'][i] > 5:
        pData['depEp'][i] = 1
        firstDepEp = pData['Date'][i]
        
        # Keeping a counter on number of depressive episodes and longest interval
        numDepEps += 1
        depEpStreak += 1
    else:
        depEpStreak = 0

# Computing predictive statistics for mood as predictive behavior for self harm
# Visualization of a sample computation
refMoodMean = refDataP['Mood'].mean()
refMoodVar = refDataP['Mood'].var()
plt.figure(figsize = (12,5))
n, bins, patches = plt.hist(refDataP['Mood'], 100, normed = 1, facecolor = 'blue', alpha = 0.75)
gFit = mlab.normpdf(bins, refMoodMean, math.sqrt(refMoodVar))
gPlot = plt.plot(bins, gFit, 'r--', linewidth = 1)
plt.xlabel('Mood Score')
plt.ylabel('Proportion in Reference Data')
plt.title('Histogram of Mood Scores for Self-Harming Patients')
plt.savefig('moodHist.jpg')

# Computing probability of self harm, poor academic performance, and peer
# conflict from each mood value using Gaussian
# cumulative probability functions

for i in range (0, len(pData.index)):
    cdfCountSH = 0
    cdfCountA = 0
    cdfCountP = 0
    for j in range (0, len(refDataSH.index)):
        if refDataSH['Mood'][j] > pData['Mood'][i]:
            cdfCountSH += 1
    for j in range (0, len(refDataA.index)):
        if refDataA['Mood'][j] > pData['Mood'][i]:
            cdfCountA += 1
    for j in range (0, len(refDataP.index)):
        if refDataP['Mood'][j] > pData['Mood'][i]:
            cdfCountP += 1
            
    probSH = float(cdfCountSH) / float(len(refDataSH.index))
    probA = float(cdfCountA) / float(len(refDataA.index))
    probP = float(cdfCountP) / float(len(refDataP.index))
    
    # Updating dataframe with probabilities of concerning outcomes
    pData['Self-Harm Probability'][i] = probSH
    pData['Academic Struggle Probability'][i] = probA
    pData['Peer Conflict Probability'][i] = probP    

# Saving plots and reports
subdirectory = 'reports/'
# Creating new subdirectory if it doesn't already exist
try:
    os.stat(subdirectory)
except:
    os.mkdir(subdirectory) 
            
plt.figure(figsize = (12,5))
plt.plot(pData['Date'], pData['Self-Harm Probability'], 'r--', label = 'Self-Harm Probability')
plt.plot(pData['Date'], pData['Academic Struggle Probability'], 'b--', label = 'Academic Struggle Probability')
plt.plot(pData['Date'], pData['Peer Conflict Probability'], 'g--', label = 'Peer Conflict Probability')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Probability')
plt.title('Probability of Adverse Events')
f = tkFileDialog.asksaveasfilename(defaultextension=".jpg")
plt.savefig(f)
tkMessageBox.showinfo("Save", "Figure saved as " + str(f))

if(depEpStreak):
    depEpStatus = "YES"
else:
    depEpStatus = "NO"
    
popupMessage = "Depressive Episode Detected: " + depEpStatus + "\nFirst date of depressive episode: " + str(firstDepEp) + "\n" + "Longest depressive episode interval: " + str(depEpStreak) + "\n"
                
tkMessageBox.showinfo("Analytics", popupMessage)



