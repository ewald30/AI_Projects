# -*- coding: utf-8 -*-

from Model.domain import *
import pickle


class repository():
    def __init__(self, toHome=True):
         
        self.populations = []
        self.cmap = Map()
        self.fitnessAvg = []
        self.toHome = toHome

    def writeFile(self, repoFile="repoFile"):
        with open(repoFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def loadFile(self, repoFile="repoFile"):
        with open(repoFile, "rb") as f:
            dummy = pickle.load(f)
            self.populations = dummy.populations
            self.cmap = dummy.cmap
            self.fitnessAvg = dummy.fitnessAvg
            f.close()

    def addFitnessAvg(self, avg):
        self.fitnessAvg.append(avg)

    def getFitnessAvg(self):
        return self.fitnessAvg
        
    def createPopulation(self, args):
        # args = [populationSize, individualSize] -- you can add more args
        return self.populations.append(Population(args[0], args[1]))

    def savePopulation(self, population):
        self.populations.append(population)

    def getLastPopulation(self):
        return self.populations.pop()
        
    # TO DO : add the other components for the repository: 
    #    load and save from file, etc
            