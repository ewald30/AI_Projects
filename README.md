# AI_Projects
Contains multiple simple AI projects that I've worked on


1. Genetic Algorithm:
  It is a simple simulation of a drone that tries to explore a 2D randomized map, discovering as much as possible before returning home.
  The default settings for the simulation are as follows: - populationSize = 100 (the number of chromosomes that will run under one iteration)
                                                          - individualSize = 500 (the number of genes that a chromosome has)
                                                          - initialCoordinates = (25,25) (each chromosome will spawn at this point on the map)
                                                          - crossOverProb = 0.8 (probability of a crossover happening)
                                                          - mutateProb = 0.04 (probability of a mutation algorithm BE AWARE!!! somehow I messed up the mutation and setting it 
                                                          higher might ruing the algorithm)
                                                          - showPath (True/False) (if it is set to True, the path of the fittest individual from a generation will be displayed 
                                                          on a GUI window)
                                                          - nbIterations - 30 (the number of iterations that the algorithm will do)
  These values can be changed from the ui.py file in the view package.
  After the algorithm will finish the number of iterations it will dispplay a graph that plots the average fitness of each generation
  An iteration consists of:  
    - evaluate individuals 
    - select the individuals (using the stochastic approach for Roulette selection) 
    - crossover
    - reestablishing the population (50% selected parents, 50% children)
    - mutate
    
