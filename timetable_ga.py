import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt

from schedule_structure.schedule import Schedule
from hardreq_validation import hardreq_validation


class Fitness:
    def __init__(self, schedule):
        self.schedule = schedule
        self.ranking = 0
        self.fitness = 0.0

    def rank(self):
        # Calculate the total ranking score of the schedule
        self.ranking = 12345
        return self.ranking

    def scheduleFitness(self):
        # Fitness is the lower, the better
        # Maybe call validator here, if cannot pass validation, set the fitness as 1 (based on the formula we may use, it should be a large number)
        self.fitness = 1 / float(self.rank())
        return self.fitness


class GA:
    """ GA """

    def __init__(self, population, popSize, eliteSize, mutationRate,
                 generations):
        self.population = population
        self.popSize = popSize
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
        self.generations = generations

    def createSchedule(self, schedule):
        """ generate a new schedule (which is used to add more schedule to the population) """
        # Based on the data structure, we will randomize the data in the schedule to create a new schedule
        schedule = random.sample(schedule, len(schedule))
        return schedule

    def initialPopulation(self, popSize, schedule):
        """ calling createSchedule function to initialize the population """
        population = []
        for i in range(0, popSize):
            population.append(self.createSchedule(schedule))
        return population

    def rankSchedule(self, population):
        """ calling the ranking system to calculate the ranking score for each schedule in the population """
        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).scheduleFitness()
        return sorted(
            fitnessResults.items(), key=operator.itemgetter(1), reverse=True)

    def selection(self, popRanked, eliteSize):
        """ selection function I copied from other GA selection, they should all be similar"""
        selectionResults = []
        df = pd.DataFrame(np.array(popRanked), columns=["Index", "Fitness"])
        df['cum_sum'] = df.Fitness.cumsum()
        df['cum_perc'] = 100 * df.cum_sum / df.Fitness.sum()

        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])
        for i in range(0, len(popRanked) - eliteSize):
            pick = 100 * random.random()
            for i in range(0, len(popRanked)):
                if pick <= df.iat[i, 3]:
                    selectionResults.append(popRanked[i][0])
                    break
        return selectionResults

    def matingPool(self, population, selectionResults):
        """ creating mating pool based on the selection result """
        matingpool = []
        for i in range(0, len(selectionResults)):
            index = selectionResults[i]
            matingpool.append(population[index])
        return matingpool

    def breed(self, parent1, parent2):
        """ happening in breedpopulation function, also called crossover """
        child = []
        childP1 = []
        childP2 = []

        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))

        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(parent1[i])

        childP2 = [item for item in parent2 if item not in childP1]

        child = childP1 + childP2
        return child

    def breedPopulation(self, matingpool, eliteSize):
        """ breeding child generation """
        children = []
        length = len(matingpool) - eliteSize
        pool = random.sample(matingpool, len(matingpool))

        for i in range(0, eliteSize):
            children.append(matingpool[i])

        for i in range(0, length):
            child = self.breed(pool[i], pool[len(matingpool) - i - 1])
            children.append(child)
        return children

    def mutate(self, individual, mutationRate):
        """ individual mutation """
        # Based on data structure, lets decide how will we do the mutation
        return individual

    def mutatePopulation(self, population, mutationRate):
        """ mutation in the population """
        mutatedPop = []

        for ind in range(0, len(population)):
            mutatedInd = self.mutate(population[ind], mutationRate)
            mutatedPop.append(mutatedInd)
        return mutatedPop

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        """ child generation (finished breeding and mutation) """
        popRanked = self.rankSchedule(currentGen)
        selectionResults = self.selection(popRanked, eliteSize)
        matingpool = self.matingPool(currentGen, selectionResults)
        children = self.breedPopulation(matingpool, eliteSize)
        nextGeneration = self.mutatePopulation(children, mutationRate)
        return nextGeneration
