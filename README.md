# AI_Projects
Contains multiple simple AI projects that I've worked on


**1. Genetic Algorithm:**
  - It is a simple simulation of a drone that tries to explore a 2D randomized map, discovering as much as possible before returning home.
  - The default settings for the simulation are as follows: 
    - populationSize = 100 (the number of chromosomes that will run under one iteration)
    - individualSize = 500 (the number of genes that a chromosome has)
    - initialCoordinates = (25,25) (each chromosome will spawn at this point on the map)
    - crossOverProb = 0.8 (probability of a crossover happening)
    - mutateProb = 0.04 (probability of a mutation algorithm BE AWARE!!! somehow I messed up the mutation and setting it higher might ruing the algorithm)
    - showPath (True/False) (if it is set to True, the path of the fittest individual from a generation will be displayed on a GUI window)
    - nbIterations - 30 (the number of iterations that the algorithm will do)
  - These values can be changed from the ui.py file in the view package.
  - After the algorithm will finish the number of iterations it will dispplay a graph that plots the average fitness of each generation
  - An iteration consists of:  
    * evaluate individuals 
    * select the individuals (using the stochastic approach for Roulette selection) 
    * crossover
    * reestablishing the population (50% selected parents, 50% children)
    * mutate


**Fuzzy control of Inverted Pendulum:**
  - Basicaly a demonstration of Knowledge Based Systems (specifically Rule Based Systems)
  - Works by having expert level knowledge on keeping the inverted pendulum in equilibrium
  - The pendulum is kept on a car that has to move forward and backwward in order to balance itself
  - The purpose of the solver is to generate the correct force in order to move the car and keep the pendulum balanced
  - The solver works as follows:
    - Gets the angular speed and the angle of the pendulum
    - Determines the degree of membership to each fuzzy set for those two variables
    - Constructs the base of rules with the previously calculated values
    - Evaluates the rules and calculates the result
    - Defuzzyfies the result in order to return it
  - There are two settings that can be configured in main: SLOW_MO and RANDOM_FACTOR
  - RANDOM_FACTOR will try to unbalance the pendulum at each run by adding a random number to the calculated force
  - This variable is used to make the simulation more realistic since by default it will stay balanced perfectly 
