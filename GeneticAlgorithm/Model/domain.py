# -*- coding: utf-8 -*-
import pickle
from random import *
import random
from utils import *
import numpy as np
import time


# the glass gene can be replaced with int or float, or other types
# depending on your problem's representation

class gene:
    def __init__(self):
        # UP = 0    DOWN = 2   LEFT = 1     RIGHT = 3
        self.__g = randint(0, 3)

    def getGene(self):
        return self.__g

    def setGene(self, gene):
        self.__g = gene

    def calculateCoordinates(self, coordinates):
        x, y = coordinates
        if self.__g == 0:
            y += 1
        elif self.__g == 1:
            x -= 1
        elif self.__g == 2:
            y -= 1
        elif self.__g == 3:
            x += 1

        newCoords = (x, y)
        return newCoords


class Individual:
    def __init__(self, size=0):
        self.__size = size
        self.__chromosome = [gene() for i in range(self.__size)]
        self.__fitness = None
        self.__readingsTotal = 0
        self.__path = []

    def getPath(self):
        return self.__path

    def getFitness(self):
        return self.__fitness

    def getChromosome(self):
        return self.__chromosome

    def __getitem__(self, item):
        return self.__chromosome[item]

    def __setitem__(self, key, value):
        self.__chromosome[key] = value

    def __readUDMSensors(self, coordinates, surface, n, m):
        # coords[0] = x    coords[1] = y

        readings = 0
        # UP
        xf = coordinates[0] - 1
        while (xf >= 0) and (surface[xf][coordinates[1]] <= 0):
            if surface[xf][coordinates[1]] != -1:
                surface[xf][coordinates[1]] = -1
                readings += 1
            xf = xf - 1

        # DOWN
        xf = coordinates[0] + 1
        while (xf < n) and (surface[xf][coordinates[1]] <= 0):
            if surface[xf][coordinates[1]] != -1:
                surface[xf][coordinates[1]] = -1
                readings += 1
            xf = xf + 1

        # LEFT
        yf = coordinates[1] + 1
        while (yf < m) and (surface[coordinates[0]][yf] <= 0):
            if surface[coordinates[0]][yf] != -1:
                surface[coordinates[0]][yf] = -1
                readings += 1
            yf = yf + 1

        # RIGHT
        yf = coordinates[1] - 1
        while (yf >= 0) and (surface[coordinates[0]][yf] <= 0):
            if surface[coordinates[0]][yf] != -1:
                surface[coordinates[0]][yf] = -1
                readings += 1
            yf = yf - 1
        return readings

    def fitness(self, map, coordinates):
        # compute the fitness for the individual
        # and save it in self.__f
        mapCopy = []
        path = []

        # Create a copy of the map for each individual
        for x in map.getSurface():
            line = x.copy()
            mapCopy.append(line)

        # Copy the coordinates
        coordsCopy = coordinates
        fitness = 0

        for gene in self.__chromosome:

            fitness += self.__readUDMSensors(coordsCopy, mapCopy, map.n, map.m)    # fitness = fitness + readings
            newCoords = gene.calculateCoordinates(coordsCopy)          # calculate the new position
            if map.checkSurface(newCoords):                 # check if the new position is ok to move to
                path.append(coordsCopy)                  # add the last position to the path
                coordsCopy = newCoords                  # move to the new position

        if coordinates != coordsCopy:
            fitness = 1
        self.__fitness = fitness
        self.__path = path

    def mutate(self, mutateProbability=0.04):
        if random.random() < mutateProbability:
            indexes = random.sample(list(range(self.__size)), k=randint(1, self.__size-1))

            for index in indexes:
                self.__chromosome[index] = gene()

    def crossover(self, otherParent, crossoverProbability=0.8):
        # perform the crossover between the self and the otherParent
        offspring1, offspring2 = Individual(self.__size), Individual( self.__size)

        if random.random() < crossoverProbability:
            for i in range(self.__size):
                random_gene = randint(0,1)
                if random_gene == 1:
                    offspring1[i] = self.__chromosome[i]
                    offspring2[i] = otherParent[i]
                else:
                    offspring1[i] = otherParent[i]
                    offspring2[i] = self.__chromosome[i]

        return offspring1, offspring2


class Population:
    def __init__(self ,populationSize=0, individualSize=0):
        self.__populationSize = populationSize
        self.__v = [Individual(individualSize) for x in range(populationSize)]

    def __getitem__(self, item):
        return self.__v[item]

    def getPopulation(self):
        return self.__v

    def setPopulation(self, population):
        self.__v = population

    def recombination(self, offspring):
        for x in offspring:
            self.__v.append(x)

    def evaluate(self, map, coordinates):
        # evaluates the population
        fit = []
        for x in self.__v:
            x.fitness(map, coordinates)
            fit.append(x.getFitness())
            if max(fit) == x.getFitness():
                path = x.getPath()
            # if min(fit) == x.getFitness():
            #     path = x.getPath()
        avg = sum(fit)/len(fit)
        return [path, avg, max(fit)]



    def mutate(self, mutateProb):
        for x in self.__v:
            x.mutate(mutateProb)

    def selection(self, N=0):
        # selects N chromosomes from the population
        wheel = self.__makeWheel()
        stepSize = 1.0 / N  # the size of a step when selecting from the wheel
        answer = []
        r = random.random()     # we start at a random value in the wheel
        answer.append(self.__binSearch(wheel, r))   # we get the chromosome where r landed
        while len(answer) < N:                      # while we can still get N-r chromosomes
            r += stepSize                           # recalculate the landing point
            if r > 1:                               # if it goes beyond our wheel
                r %= 1
            answer.append(self.__binSearch(wheel, r))   # search again for the chromosome where r landed
        return answer   # returns a list of chromosomes

    def __makeWheel(self):
        # creates the wheel used for selection
        wheel = []
        total = sum(p.getFitness() for p in self.__v)  # the total fitness
        top = 0
        for p in self.__v:
            f = p.getFitness() / total      # for a chromosome we reserve fitness/total space on the wheel
            wheel.append((top, top + f, p))     # top = where the portion of the wheel starts / top+f where it ends
            top += f                # we recalculate the starting point for the next chromosome
        return wheel

    def __binSearch(self, wheel, num):
        mid = len(wheel) // 2
        low, high, answer = wheel[mid]      # unpack the 3 values
        if low <= num <= high:          # if num is between the start and end point of a chromosome =>
            return answer               # return the chromosome itself
        elif high < num:
            return self.__binSearch(wheel[mid + 1:], num)
        else:
            return self.__binSearch(wheel[:mid], num)



class Map:
    def __init__(self, n=20, m=20):
        self.n = n
        self.m = m
        self.surface = np.zeros((self.n, self.m))

    def getSurface(self):
        return self.surface

    def checkSurface(self, coords):
        x, y =coords
        if x < 0 or y < 0:
            return False
        if x >= self.n or y >= self.m:
            return False
        if self.surface[x][y] == 1:
            return False
        return True

    def randomMap(self, fill=0.2):
        for i in range(self.n):
            for j in range(self.m):
                if random.random() <= fill:
                    self.surface[i][j] = 1

    def loadMap(self, numfile):
        with open(numfile, "rb") as f:
            dummy = pickle.load(f)
            self.n = dummy.n
            self.m = dummy.m
            self.surface = dummy.surface
            f.close()

    def saveMap(self, numFile="test.map"):
        with open(numFile, 'wb') as f:
            pickle.dump(self, f)
            f.close()

    def __str__(self):
        string = ""
        for i in range(self.n):
            for j in range(self.m):
                string = string + str(int(self.surface[i][j]))
            string = string + "\n"
        return string
