from FoodWebCharts import drawHistogram as hist, fitDistr as fitD, fitLogDistr as fitLD
import os
import numpy as np
import pandas as pd
from FoodWeb import readExcelFile

#MainFunction calling other scripts
CumulArray = []
for filename in os.listdir('Data/XLS/'):
    nameToImp = 'Data/XLS/' + filename
    net = readExcelFile(nameToImp)
    df = net.calcDegreeIn()
    tl_frame = pd.DataFrame(net.calcTrophicLevel())
    tl_frame.index += 1
    new = pd.concat([df,tl_frame], axis = 1, sort = False)
    fileToSave = 'Data/Recalced/' + filename
    new.columns = ['Name', 'DegreeIn', 'TrophicLevel']
    new.to_excel(fileToSave, index = True)
    array = new.iloc[:, 1].values
    CumulArray.extend(array)
    pltName= 'Data/Recalced/Plots/' + filename[:-4] + '.png'
    fitD(array, filename[:-4], pltName)
    
pltName = 'Data/Recalced/Plots/AllFwAggregated.png'
plt = fitD(CumulArray, 'AllFWAggregated', pltName)