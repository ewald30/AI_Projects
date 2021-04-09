from repository import *


class controller():
    def __init__(self, args, repository):
        # args - list of parameters needed in order to create the controller
        self.repository = repository
        self.avgs = []
        pass

    def addFitnessAvg(self, fitAvg):
        repository.addFitnessAvg(fitAvg)

    def iteration(self, args, population):
        # args - list of parameters needed to run one iteration
        # a iteration:
        # selection of the parrents
        # create offsprings by crossover of the parents
        # apply some mutations
        # selection of the survivors

        popSize, inidivdualSize, initialCoordinates, map, crossOverProb, mutateProb = args
        results = population.evaluate(map, initialCoordinates)
        population.setPopulation(population.selection(popSize/2))
        offspring = []

        # inp = input("cmd:")
        # if inp == "x":
        #     map.saveMap("bigMap1")
        for i in range(popSize//2-1):
            x = population[i]
            y = population[i+1]
            offspring1, offspring2 = x.crossover(y, crossOverProb)
            offspring.append(offspring1)
            offspring.append(offspring2)

        population.recombination(offspring)
        population.mutate(mutateProb)
        self.repository.savePopulation(population)
        self.avgs.append(results[1])
        self.repository.addFitnessAvg(results[2])
        return results



    def run(self, args, population):
        # args - list of parameters needed in order to run the algorithm
        
        # until stop condition
        #    perform an iteration
        #    save the information need it for the satistics
        
        # return the results and the info for statistics
        stats = []

        result = self.iteration(args, population)
        return result

    
    def solver(self, args):
        # args - list of parameters needed in order to run the solver
        # create the population,
        # run the algorithm
        # return the results and the statistics

        population = self.repository.getLastPopulation()
        return self.run(args, population)

       