# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sci
import scipy.stats as scistat

def drawHistogram(array):
    plt.hist(array, normed = True, bins = 5)
    plt.ylabel('Probability')
    
def fitDistr(array, plotName, saveDestination):
    plt.hist(array, normed = True)
    dist = getattr(scistat, 'lognorm')
    param = dist.fit(array)
    maxVal = np.max(array)
    pdf_fitted = dist.pdf(sci.arange(maxVal*1.5), *param[:-2], loc = param[-2], scale = param[-1])
    plt.plot(pdf_fitted, label ='lognorm')
    plt.xlim(0,maxVal*1.5)
    plt.title(plotName)
    plt.xlabel('InDegree')
    plt.ylabel('Density')
    plt.savefig(saveDestination)
    plt.show()
    
def fitLogDistr(array, plotName, saveDestination):
    array = [x if x != 0 else 1 for x in array]
    array = np.log10(array)
    print(array)
    plt.hist(array, normed = True)
    dist = getattr(scistat, 'lognorm')
    param = dist.fit(array)
    maxVal = np.max(array)
    if maxVal == 0:
        maxVal = 1
    pdf_fitted = dist.pdf(sci.arange(maxVal*1.5), *param[:-2], loc = param[-2], scale = param[-1])
    plt.plot(pdf_fitted, label ='lognorm')
    plt.xlim(0,maxVal*1.5)
    plt.title(plotName)
    plt.xlabel('InDegree')
    plt.ylabel('Density')
    plt.savefig(saveDestination)
    plt.show()