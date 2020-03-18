import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv

from schedule_structure.schedule import Schedule
from schedule_structure.timeblock import Timeblock
from hardreq_validation import hardreq_validation


class Fitness:
    def __init__(self, schedule):
        self.schedule = schedule
        # self.ranking = 0
        self.fitness = hardreq_validation(self.schedule)

    # def rank(self):
    #     # Calculate the total ranking score of the schedule
    #     self.ranking = 12345
    #     return self.ranking

    def scheduleFitness(self):
        # Fitness is the lower, the better
        # Maybe call validator here, if cannot pass validation, set the fitness as 1 (based on the formula we may use, it should be a large number)
        # self.fitness = 1 / float(self.rank())
        return self.fitness


class GA:
    """ GA """

    def __init__(self, popSize, eliteSize, mutationRate, generations):
        self.popSize = popSize
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
        self.generations = generations
        self.population = self._initialPopulation(popSize)

    def _createSchedule(self, schedule):
        """ generate a new schedule (which is used to add more schedule to the population) """
        # Based on the data structure, we will randomize the data in the schedule to create a new schedule
        with open("data\\crn_file.json", "r") as data:
            crn_data = json.load(data)

        with open("data\\ins_file.json", "r") as data:
            ins_data = json.load(data)

        with open("data\\rm_file.json", "r") as data:
            rm_data = json.load(data)

        rm_list = []
        for i in rm_data:
            rm_list.append(i)

        time_table = []  # (crn, ins_id, rm_id, day, time)
        room_time = []
        ins_time = []

        for i in crn_data:
            temp_ins = random.randint(1, 40)
            temp_day = random.randint(1, 5)
            temp_time = random.randint(1, 3)
            temp_rm = random.randint(0, 39)
            temp_rm_d_t = [temp_rm, temp_day, temp_time]
            temp_ins_time = [temp_ins, temp_time]
            while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time):
                if temp_rm_d_t in room_time:
                    temp_day = random.randint(1, 5)
                    temp_time = random.randint(1, 3)
                    temp_rm = random.randint(0, 39)
                    temp_rm_d_t = [temp_rm, temp_day, temp_time]
                if temp_ins_time in ins_time:
                    temp_ins = random.randint(1, 40)
                    temp_day = random.randint(1, 5)
                    temp_time = random.randint(1, 3)
                    temp_ins_time = [temp_ins, temp_day, temp_time]

            room_time.append(temp_rm_d_t)  # If room time is used
            ins_time.append(temp_ins_time)  # If instructor is already working

            temp_block = Timeblock(i, temp_ins, rm_list[temp_rm], temp_day,
                                   temp_time)
            schedule.add_timeblock(temp_block)

        return schedule

    def _initialPopulation(self, popSize):
        """ calling createSchedule function to initialize the population """
        population = []

        for i in range(0, popSize):
            temp_schedule = Schedule()
            population.append(self._createSchedule(temp_schedule))
            del temp_schedule

        return population

    def rankSchedule(self):
        """ calling the ranking system to calculate the ranking score for each schedule in the population """
        population = self.population

        fitnessResults = {}
        for i in range(0, len(population)):
            fitnessResults[i] = Fitness(population[i]).scheduleFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1))

    def selection(self):
        """ selection function I copied from other GA selection, they should all be similar"""
        selectionResults = []
        popRanked = self.rankSchedule()
        eliteSize = self.eliteSize

        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])

        return selectionResults

    def breed(self, parent1, parent2):
        """ happening in breed population function, also called crossover """
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

    def breedPopulation(self):
        """ breeding child generation """
        matingpool = self.selection()
        eliteSize = self.eliteSize

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


if __name__ == "__main__":
    ga1 = GA(100, 10, 0.1, 10)
    # print(ga1.showPopulation()[0].display_schedule())
    print(ga1.rankSchedule())
    print(ga1.selection())

# ga1.population[0].day, time, room
# ga1.population[1]