# -*- coding: utf-8 -*-


# imports

from View.gui import *
from Controller.controller import *
from repository import *
from Model.domain import *
import pygame
import matplotlib.pyplot as plt

# create a menu
#   1. map options:
#         a. create random map
#         b. load a map
#         c. save a map
#         d visualise map
#   2. EA options:
#         a. parameters setup
#         b. run the solver
#         c. visualise the statistics
#         d. view the drone moving on a path
#              function gui.movingDrone(currentMap, path, speed, markseen)
#              ATENTION! the function doesn't check if the path passes trough walls


#  Parameters:
seeds = [1, 20, 3, 5, 6, 2, 10, 5, 25, 26, 21, 18, 26, 13, 11, 30, 1, 2, 10, 11, 17, 19, 27, 4, 8, 3, 22, 15, 23, 28, 6,
         9, 2, 0]
populationSize = 200
inidividualSize = 200
initialCoordinates = (25, 25)
map = Map(50, 50)
# map.loadMap("bigMap1")
map.randomMap(0.1)
crossOverProb = 0.8
mutateProb = 0.04
showPath = True
nbIterations = 30


def runWithPath(screen, map, path, markSeen):
    drona = pygame.image.load("drona.png")
    for i in range(len(path)):
        if markSeen:
            brick = pygame.Surface((20, 20))
            brick.fill([100, 255, 120])
            for j in range(i + 1):
                for var in v:
                    x = path[j][0]
                    y = path[j][1]
                    while ((0 <= x + var[0] < map.n and
                            0 <= y + var[1] < map.m) and
                           map.surface[x + var[0]][y + var[1]] != 1):
                        x = x + var[0]
                        y = y + var[1]
                        screen.blit(brick, (y * 20, x * 20))

        screen.blit(drona, (path[i][1] * 20, path[i][0] * 20))
        pygame.display.flip()


def oneRun():
    screen = initPyGame((1000, 1000))

    for i in range(nbIterations):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        start = time.time()
        results = controller.solver(args)
        end = time.time()
        print("------------------------------------")
        print("Maximum Fitness:  " + str(results[2]))
        print("Average Fitness:  " + str(results[1]))
        print("Time: " + str(end - start))
        print("------------------------------------\n\n")

        if showPath:
            screen.blit(image(map), (0, 0))
            runWithPath(screen, map, results[0], True)

    plt.plot(controller.avgs)
    plt.ylabel('Average fitness per generation')
    plt.xlabel('Generation number')
    plt.show()
    return results[0]


if __name__ == '__main__':
    args = []
    args.append(populationSize)
    args.append(inidividualSize)
    args.append(initialCoordinates)
    args.append(map)
    args.append(crossOverProb)
    args.append(mutateProb)

    repository = repository()
    controller = controller(args, repository)
    # f = open("Stats/test.txt", "a")
    # f.write("-------------------------------------------------------\n")
    # f.write("|  Seed  |  Average Deviation  |  Standard Deviation  |\n")
    # f.close()
    for i in range(1):
        repository.createPopulation(args)
        path = oneRun()
        seed = seeds[i]
        random.seed(seed)
        fitAvg = repository.getFitnessAvg()
        data = np.array(fitAvg)

        # averageDev = np.average(data)
        # standardDev = data.std()
        # f = open("Stats/test.txt", "a")
        # f.write("-------------------------------------------------------\n")
        # f.write("|   " + str(seed) + "    |          " + str(int(averageDev)) + "        |        " + str(
        #     int(standardDev)) + "           |\n")
        # f.close()

    while True:
        screen = initPyGame((1000, 1000))
        screen.blit(image(map), (0, 0))
        runWithPath(screen, map, path, True)

