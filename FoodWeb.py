# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd


class Network:
    title = None
    numberOfNodes = None
    numberOfLivingNodes = None
    meanDegreeOfNode = None
    flowMatrix = None
    nodeProperties = None
    
    def __init__(self, title = None, numberOfNodes = None, numberOfLivingNodes = None, meanDegreeOfNode = None, flowMatrix = None, nodeProperties = None):
        '''Constructor from given dataframes'''
        self.title = title
        self.numberOfNodes = numberOfNodes
        self.numberOfLivingNodes = numberOfLivingNodes
        self.meanDegreeOfNode = meanDegreeOfNode
        self.flowMatrix = flowMatrix
        self.nodeProperties = nodeProperties
        
    def calcDegreeIn(self):
        degrees = self.nodeProperties.drop(['IsLiving', 'Biomass', 'Import', 'Export', 'Respiration'], axis=1)
        degrees['meanDegrees'] = np.transpose(np.zeros(len(degrees.index)))
        for x in range(0, len(self.flowMatrix.index)):
            for y in range(0, len(self.flowMatrix.index)):
                if self.flowMatrix.iat[y, x] != 0:
                    degrees.iloc[y, 1] += 1
        #print(meanDegrees)
        return degrees
    
    def calcDegreeOut(self):
        degrees = self.nodeProperties.drop(['IsLiving', 'Biomass', 'Import', 'Export', 'Respiration'], axis=1)
        degrees['meanDegrees'] = np.transpose(np.zeros(len(degrees.index)))
        for x in range(0, len(self.flowMatrix.index)):
            for y in range(0, len(self.flowMatrix.index)):
                if self.flowMatrix.iat[x, y] != 0:
                    degrees.iloc[y, 1] += 1
        #print(meanDegrees)
        return degrees
    
    def calcWeightedDegreeIn(self):
        wDegrees = self.nodeProperties.drop(['IsLiving', 'Biomass', 'Import', 'Export', 'Respiration'], axis=1)
        wDegrees['meanDegrees'] = np.transpose(np.zeros(len(wDegrees.index)))
        for x in range(0, len(self.flowMatrix.index)):
            for y in range(0, len(self.flowMatrix.index)):
                wDegrees.iloc[y, 1] += self.flowMatrix.iat[y, x]
        #print(meanDegrees)
        return wDegrees
    
    def calcWeightedDegreeOut(self):
        wDegrees = self.nodeProperties.drop(['IsLiving', 'Biomass', 'Import', 'Export', 'Respiration'], axis=1)
        wDegrees['meanDegrees'] = np.transpose(np.zeros(len(wDegrees.index)))
        for x in range(0, len(self.flowMatrix.index)):
            for y in range(0, len(self.flowMatrix.index)):
                wDegrees.iloc[y, 1] += self.flowMatrix.iat[x, y]
        #print(meanDegrees)
        return wDegrees
    
    def calcTrophicLevel(self):
        #dataFlows=net.flowMatrix
        dataFlows = self.flowMatrix
        dataSize=len(dataFlows)
        #print(dataFlows)
        A=np.zeros([dataSize,dataSize])
        inflow=np.zeros(dataSize)
        isFixedToOne=np.zeros(dataSize, dtype=bool)
        dataTrophicLevel=np.zeros(dataSize)
        n=0 #counting the nodes with TL fixed to 1
        for i in range(0,dataSize):
            
            isFixedToOne[i] = False
            dataTrophicLevel[i] = 0.0
            for j in range(0,dataSize):
                inflow[i] += dataFlows.iloc[j,i] # sum of all incoming system flows to the compartment i
                A[i][i] += dataFlows.iloc[j,i] # the diagonal has the sum of all incoming system flows to the compartment i, except flow from i to i
                if i!=j: A[i][j] = -dataFlows.iloc[j,i]
            
            #choose the nodes that have TL=1: non-living and primary producers == inflows equal to zero         
            if (inflow[i] <= 0.0 or i >= int(self.numberOfLivingNodes)):
                isFixedToOne[i] = True
                dataTrophicLevel[i] = 1.0
                n += 1
       
        if (n != 0): # update the equation due to the prescribed trophic level 1 - reduce the dimension of the matrix
            B_tmp = np.zeros(dataSize - n)
            A_tmp = np.zeros([dataSize - n,dataSize - n])
            TL_tmp = np.zeros(dataSize - n)
            tmp_i = 0
            for i in range(0,dataSize):
                if not isFixedToOne[i]:
                    B_tmp[tmp_i] = inflow[i]
                    tmp_j = 0
                    for j in range(0,dataSize):
                        if (isFixedToOne[j]): #means also i!=j
                            B_tmp[tmp_i] -= A[i][j] #moving the contribution to the constant part, + flow(j->i)*1 to both sides of the equation
                        else:
                            A_tmp[tmp_i][tmp_j] = A[i][j]
                            tmp_j+=1
                    tmp_i+=1        
            for i in range(0,dataSize-n):
                TL_tmp[i] = 0.0
                Ainverse=np.linalg.pinv(A_tmp)
                for j in range(0,dataSize-n):
                    TL_tmp[i] += Ainverse[i][j] * B_tmp[j]
            k = 0
            for i in range(0,dataSize):
                if (not isFixedToOne[i]):
                    dataTrophicLevel[i] = TL_tmp[k]
                    k+=1    
        else:        
            try:
                A1 = np.linalg.pinv(A)    
            except:    
                print("The matrix A1 which inverse was seeked but does not exist:")
                print(A1)
                        #negative trophic levels signify some problems
        return dataTrophicLevel
    
    def calcTst(self):
        dataSize=len(self.flowMatrix)
        TST = None
        for i in range(0, dataSize):
            for j in range(0, dataSize):
                TST += self.flowMatrix.iloc[i,j]
                
        dataSize = len(self.nodeProperties)
        TST += sum(self.nodeProperties.iloc[:,3])
        return TST
    
    def calcImports(self):
        imports = sum(self.nodeProperties.iloc[:,3])
        return imports
    
    def normalizeFlowMatrix(self, divider):
        self.flowMatrix = self.flowMatrix / divider
    
    
def readExcelFile(filename):
    excel = pd.ExcelFile(filename)
    df2 = excel.parse(1)
    df3 = excel.parse(2)
    numberOfNodes = len(df3.index)-1
    numberOfLivingNodes = sum(df2.iloc[:,1])
    net = Network(title = filename, numberOfNodes = numberOfNodes, numberOfLivingNodes = numberOfLivingNodes, flowMatrix = df3, nodeProperties = df2)
    return net
       
