# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 16:19:29 2018

selfReportAnalysis.py

Analyzes entries of self reporting records to provide physicians with
visualizations of data and alerts if analysis shows imminent danger to patient.

Input: CSV records of patient's self reporting records
Output: Graphs of health trends and email notifications of for extreme trends

#"""

import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

def plotData(pData, field, startDate, endDate):
    dataToPlot = pData[(pData['Date'].between(startDate, endDate))]

    
# Reading patient data

fileName = 'selfReportData.csv'
pData = pd.read_csv(fileName)

# Converting dates to datetime format

for x in range (0, len(pData.index)):
    tempVal = pd.to_datetime(str(pData['Date'][x]), format = '%Y%m%d')
    pData['Date'][x] = tempVal

# Testing stupid data
startDate = pd.to_datetime(str(20180102), format = '%Y%m%d')
endDate = pd.to_datetime(str(20180110), format = '%Y%m%d')
field = 'Mood'
plotData(pData, field, startDate, endDate)

dateFiltered = pData[(pData['Date'].between(startDate, endDate))]
dataToPlot = pData[['Date', field]]
name = pData['Patient Surname'][0] + ', ' + pData['Patient Firstname'][0]
plt.plot(pData['Date'], pData[field])
plt.xlabel('Date')
plt.ylabel('Score')
plt.title(field + ' Scores for ' + name)
plt.grid(True)
plt.savefig(field + '_plot.png')
plt.show()



    
