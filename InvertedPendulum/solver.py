# -*- coding: utf-8 -*-
"""
In this file your task is to write the solver function!

"""

def solver(t,w):
    """
    ABREVIATIONS:
    NVVB - NEGATIVE VERY VERY BIG
    NB   - NEGATIVE BIG
    Z/ZO - ZERO
    PB   - POSITIVE BIG
    PVVB - POSITIVE VERY VERY BIG

    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    FUZZY SETS:
    Angle - 0:NVB, 1: B, 2:N, 3:ZO, 4:P, 5:PB, 6:PVB
    Speed - 0:NB, 1:N, 2:ZO, 3:P, 4:PB
    Force - 0:NVVB, 1:NVB, 2:NB, 3:N, 4:ZO, 5:P, 6:PB, 7:PVB, 8:PVVB

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or
        None :if we have a division by zero

    """

    #   These are the fuzzy sets that will be used to transform the raw input
    angleFuzzy = {0: [-50, -25, 0], 1: [-40, -10, 0], 2: [-20, 0, 0], 3: [-5, 5, 0], 4: [0, 20, 0], 5: [10, 40, 0], 6: [25, 50, 0]}
    speedFuzzy = {0: [-10, -3, 0], 1: [-6, 0, 0], 2: [-1, 1, 0], 3: [0, 6, 0], 4: [3, 10, 0]}

    #   These are the rules that will be used to calculate the fuzzy variable for the force
    rulesFuzzy = {"PVVB": {(6,4):0, (6,3):0, (5,4):0}, "PVB":{(6,2):0, (5,3):0, (4,4):0 }, "PB":{(6,1):0, (5,2):0, (4,3):0, (3,4):0},
                  "P":{(6,0):0, (5,1):0, (4,2):0, (3,3):0, (2,4):0}, "Z":{(5,0):0, (4,1):0, (3,2):0, (2,3):0, (1,4):0},
                  "N":{(4,0):0, (3,1):0, (2,2):0, (1,3):0, (0,4):0}, "NB":{(3,0):0, (2,1):0, (1,2):0, (0,3):0}, "NVB":{(2,0):0, (1,1):0, (0,2):0},
                  "NVVB":{(1,0):0, (0,1):0, (0,0):0}}

    tableResults = {"PVVB":[], "PVB":[], "PB":[], "P":[], "Z":[], "N":[], "NB":[], "NVB":[], "NVVB":[]}

    print("GOT:(w,t)", w, t)
    for x in angleFuzzy.keys():

        a = angleFuzzy[x][0]
        c = angleFuzzy[x][1]
        b = (a+c)/2
        #   UXS = the degree of membership to each fuzzy set
        uxA = max(0, min((t-a)/(b-a), min(1, (c-t)/(c-b))))
        angleFuzzy[x][2] = uxA

    for x in speedFuzzy.keys():
        a = speedFuzzy[x][0]
        c = speedFuzzy[x][1]
        b = (a+c)/2
        #   UXS = the degree of membership to each fuzzy set
        uxS = max(0, min((w-a)/(b-a), min(1, (c-w)/(c-b))))
        speedFuzzy[x][2] = uxS

    print("ANGLE: ", angleFuzzy)
    print("SPEED: ", speedFuzzy)

    #   Populate the rule table with the minimum membership degree for each cell
    for x in rulesFuzzy.keys():
        for a in angleFuzzy.keys():
            for s in speedFuzzy.keys():
                key = (a,s)
                if key in rulesFuzzy[x]:
                    value = min(angleFuzzy[a][2], speedFuzzy[s][2])
                    rulesFuzzy[x][key] = value
                    tableResults[x].append(value)



    for x in tableResults.keys():
        tableResults[x] = max(tableResults[x])

    print("tabRES", tableResults)

    val = 32
    currentVal = 0
    sum = 0

    #   Defuzzify the calculated value
    for x in tableResults.keys():
        currentVal += tableResults[x] * val
        sum += tableResults[x]
        val -= 8
    print("\n")
    if sum == 0:
        return None
    else:
        return currentVal/sum

