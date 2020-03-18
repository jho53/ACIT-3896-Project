import numpy as np
import random
import operator
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
import itertools

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


class GeneticAlgorithm:
    """
    Genetic Algorithm representation for timetable problem

    Steps:
    initialPopulation -> _createSchedule
    rankSchedule
    selection
    """

    def __init__(self,
                 popSize,
                 eliteSize,
                 mutationRate,
                 generations,
                 population=[]):
        """
        Initiation of GA

        Parameters:
            popSize (int): Population size for each generation
            eliteSize (int): Number of chromosomes selected to be in next generation
            mutationRate (float): Value between 0 - 1 to determine the amount of crossover population to mutate
            generations: dont know if needed
        """
        self.popSize = popSize
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
        self.generations = generations

        if population == []:
            self.population = self.initialPopulation()
        else:
            self.population = population  # Represents current population in generation

    def initialPopulation(self):
        """
        Calls createSchedule() to initialize the population based on popSize

        Returns:
        population (Array): An initialized population in the form of array
        """
        population = []

        for i in range(0, self.popSize):
            temp_schedule = Schedule()
            population.append(self._createSchedule(temp_schedule))
            del temp_schedule

        return population

    def _createSchedule(self, schedule):
        """
        Generate a randomly created schedule

        Parameters:
            schedule (Schedule): Schedule object to append timeblock instances to

        Returns:
            schedule (Schedule): Schedule object with timeblocks filled

        """
        with open("data files\\crn_file.json", "r") as data:
            crn_data = json.load(data)

        with open("data files\\ins_file.json", "r") as data:
            ins_data = json.load(data)

        with open("data files\\rm_file.json", "r") as data:
            rm_data = json.load(data)

        rm_list = []
        for i in rm_data:
            rm_list.append(i)

        # time_table = []  # (crn, ins_id, rm_id, day, time)
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

    def rankSchedule(self):
        """ 
        Ranks current population based on fitness score (Fitness score = (# of HC violations))

        Returns:
        A sorted array of tuple containing index and fitness score (index, fitness score) of each chromosome in population
        """
        population = self.population
        fitnessResults = {}

        for i in range(0, len(population)):
            # hashmap of index and fitness scores
            fitnessResults[i] = Fitness(population[i]).scheduleFitness()
        return sorted(fitnessResults.items(), key=operator.itemgetter(1))

    def selection(self):
        """ 
        Selects the best of the best in population based on eliteSize

        Returns:
        selectionResults (Array): An array with the top {eliteSize} chromosome's index and scores in tuple form (index, fitness score) 
        """
        selectionResults = []
        popRanked = self.rankSchedule()
        eliteSize = self.eliteSize

        for i in range(0, eliteSize):
            selectionResults.append(popRanked[i][0])

        return selectionResults

    def breedPopulation(self):
        """
        Creates pools for mating based on selection results

        Returns:
        nextGenPop (Array): Next-gen population with BOB + Schedules that has been crossbred (cross-over)
        """
        matingpool = self.selection()  # best of the best (BOB)
        length = self.popSize - self.eliteSize  # num of population - len(selected)
        nextGenPop = []

        # Create separate pool to work with mating pool
        pool = list(itertools.combinations(matingpool, 2))
        pool = random.sample(pool, length)

        for i in range(0, self.eliteSize):
            nextGenPop.append(
                self.population[matingpool[i]])  # Appending BOB to next gen

        for i in range(0, length):
            child = self.breed(pool[i][0], pool[i][1])
            nextGenPop.append(child)

        del matingpool, pool

        return nextGenPop

    def breed(self, parent1_index, parent2_index):
        """ 
        ***Crossover function***
        Takes the courses, instructor id, and roomid  from parent 1 
        Match with day and time from parent 2

        Parameters:
            parent1_index (int): Index of parent 1 in current population
            parent2_index (int): Index of parent 2 in current population

        Returns:
            child (Schedule): Child that has both parent1 and parent2 genes
        """
        parent1 = self.population[parent1_index].get_timeblock_list()
        parent2 = self.population[parent2_index].get_timeblock_list()
        length = len(parent1)

        child = Schedule()
        temp_list = []

        for index in range(0, length):
            for gene in parent1[index].gene_1():
                # CRN, Instructor ID, Room ID
                temp_list.append(gene)
            for gene in parent2[index].gene_2():
                # Day, Time
                temp_list.append(gene)
            child.add_timeblock(
                Timeblock(temp_list[0], temp_list[1], temp_list[2],
                          temp_list[3], temp_list[4]))
            temp_list = []

        del parent1, parent2, length, temp_list

        return child

    def mutate(self, child):
        """ 
        Mutates individual child based on mutation rate
        If random.random <= mutation rate, mutate child
        
        Parameter:
        child (Schedule): Child Schedule instance that will be mutated

        Return:
        child (Schedule): Mutated child schedule
        """
        if random.random() <= self.mutationRate:
            return child
        else:
            return child

    def mutatePopulation(self, children):
        """ 
        mutation in the population

        Parameters:
        children (Array[Schedule])

        Returns:
        children (Array[Schedule]): Mutated children population
        """
        for index in range(0 + self.eliteSize, len(children)):
            children[index] = self.mutate(children[index])

        return children  # Returns mutated children

    def nextGeneration(self, currentGen, eliteSize, mutationRate):
        """
        child generation (finished breeding and mutation) 
        """
        # Step 1: Ranks current population
        popRanked = self.rankSchedule()
        # Step 2: Select BOB
        selectionResults = self.selection(popRanked, eliteSize)
        # Step 3:
        matingpool = self.matingPool(currentGen, selectionResults)
        # Step 4:
        nextGenPop = self.breedPopulation(matingpool, eliteSize)
        # Step 5:
        nextGeneration = self.mutatePopulation(nextGenPop, mutationRate)
        return nextGeneration

    def ga_start(self):
        """ Starts GA """
        pass


if __name__ == "__main__":
    POPULATION_SIZE = 100
    ELITE_SIZE = 20
    MUTATION_RATE = 0.1
    GENERATIONS = 10

    ga1 = GeneticAlgorithm(POPULATION_SIZE, ELITE_SIZE, MUTATION_RATE,
                           GENERATIONS)
    # print(ga1.showPopulation()[0].display_schedule())
    print(ga1.rankSchedule())
    print(ga1.selection())
    children = ga1.breedPopulation()
    # print(children[-1].display_schedule())

    ga2 = GeneticAlgorithm(POPULATION_SIZE, ELITE_SIZE, MUTATION_RATE,
                           GENERATIONS, children)
    print(ga2.rankSchedule())
    print(ga2.selection())
    # ga1.population[children[0]].display_schedule()
