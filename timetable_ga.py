import numpy as np
import random
from random import randint
import operator
import pandas as pd
import matplotlib.pyplot as plt
import json
import csv
import itertools
from time import time

from schedule_structure.schedule import Schedule
from schedule_structure.timeblock import Timeblock
from hardreq_validation import hardreq_validation
from ranking import score_time_table


class Fitness:
    def __init__(self, schedule):
        self.schedule = schedule
        # self.ranking = 0
        self.fitness = self.checkValidation()

    def checkValidation(self):
        if hardreq_validation(self.schedule) is False:
            return 999 - score_time_table(self.schedule.get_schedule())
        else:
            return score_time_table(self.schedule.get_schedule())

    def scheduleFitness(self):
        # Fitness is the lower, the better
        return self.fitness


class GeneticAlgorithm:
    """Genetic Algorithm representation for timetable problem"""

    def __init__(self, popSize, eliteSize, mutationRate, population=[]):
        """
        Initiation of GA

        Parameters:
            popSize (int): Population size for each generation
            eliteSize (int): Number of chromosomes selected to be in next generation
            mutationRate (float): Value between 0 - 1 to determine the amount of crossover population to mutate
            population (Array[Schedule]): Will contain an array of chromosomes (Schedule)
        """
        self.popSize = popSize
        self.eliteSize = eliteSize
        self.mutationRate = mutationRate
        self.stat = []

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

    def schedule_maker(self):
        with open("data files/crn_file.json", "r") as data:
            crn_data = json.load(data)

        with open("ins_file.json", "r") as data:
            ins_data = json.load(data)

        with open("data files/rm_file.json", "r") as data:
            rm_data = json.load(data)

        rm_list = []
        for num_rm in rm_data:
            rm_list.append(num_rm)

        rm_list = sorted(rm_list)

        time_table = {}
        # (crn, ins_id, rm_id, day, time)
        room_time = []
        ins_time = []
        ins_campus = {}
        for ins in ins_data:
            ins_campus[ins] = {
                1: '',
                2: '',
                3: '',
                4: '',
                5: ''
            }

        course_ins = {}

        for ins in ins_data:
            for j in ins_data[ins]['course']:
                course_ins[j] = []

        for ins in ins_data:
            for j in ins_data[ins]['course']:
                course_ins[j].append(ins)

        for i in crn_data:
            loop_count = 0
            if i[:-3] == 'CIT':
                temp_day = randint(1, 5)
                temp_time = randint(1, 3)
                temp_rm = randint(20, 39)
                temp_ins = course_ins[i[:-1]
                                      ][(randint(1, len(course_ins[i[:-1]])) - 1)]

                temp_rm_d_t = [temp_rm, temp_day, temp_time]
                temp_ins_time = [temp_ins, temp_day, temp_time]

                while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time) or (
                        ins_campus[temp_ins][temp_day] == 'B'):
                    loop_count += 1
                    if loop_count > 1000:
                        return None
                    if (temp_rm_d_t in room_time) and (temp_ins_time in ins_time):
                        temp_ins = course_ins[i[:-1]
                                              ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(20, 39)
                    elif temp_rm_d_t in room_time:
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(20, 39)
                    elif temp_ins_time in ins_time:
                        temp_ins = course_ins[i[:-1]
                                              ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                    else:
                        temp_ins = course_ins[i[:-1]
                                              ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(20, 39)
                    temp_rm_d_t = [temp_rm, temp_day, temp_time]
                    temp_ins_time = [temp_ins, temp_day, temp_time]
            else:
                temp_ins = course_ins[i[:-1]
                                      ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                temp_day = randint(1, 5)
                temp_time = randint(1, 3)
                temp_rm = randint(0, 39)
                temp_rm_d_t = [temp_rm, temp_day, temp_time]
                temp_ins_time = [temp_ins, temp_day, temp_time]

                while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time) or \
                        (((ins_campus[temp_ins][temp_day] == 'D') and temp_rm < 20) or (
                            (ins_campus[temp_ins][temp_day] == 'B') and temp_rm > 20)):
                    loop_count += 1
                    if loop_count > 1000:
                        return None
                    if (temp_rm_d_t in room_time) and (temp_ins_time in ins_time):
                        temp_ins = course_ins[i[:-1]
                                              ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(0, 39)
                    elif temp_rm_d_t in room_time:
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(0, 39)
                    elif temp_ins_time in ins_time:
                        temp_ins = course_ins[i[:-1]
                                              ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                    else:
                        if ins_campus[temp_ins][temp_day] == 'D':
                            temp_ins = course_ins[i[:-1]
                                                  ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                            temp_day = randint(1, 5)
                            temp_time = randint(1, 3)
                            temp_rm = randint(20, 39)
                        elif ins_campus[temp_ins][temp_day] == 'B':
                            temp_ins = course_ins[i[:-1]
                                                  ][(randint(1, len(course_ins[i[:-1]])) - 1)]
                            temp_day = randint(1, 5)
                            temp_time = randint(1, 3)
                            temp_rm = randint(0, 19)
                    temp_rm_d_t = [temp_rm, temp_day, temp_time]
                    temp_ins_time = [temp_ins, temp_day, temp_time]

            room_time.append(temp_rm_d_t)
            ins_time.append(temp_ins_time)
            ins_campus[temp_ins][temp_day] = rm_list[temp_rm][0]
            temp_block = [i, temp_ins, rm_list[temp_rm], temp_day, temp_time]
            time_table[i] = temp_block

        return time_table

    def _createSchedule(self, schedule):
        """
        Generate a randomly created schedule

        Parameters:
            schedule (Schedule): Schedule object to append timeblock instances to

        Returns:
            schedule (Schedule): Schedule object with timeblocks filled

        """
        # with open("data files\\crn_file.json", "r") as data:
        #     crn_data = json.load(data)
        #
        # with open("data files\\ins_file.json", "r") as data:
        #     ins_data = json.load(data)
        #
        # with open("data files\\rm_file.json", "r") as data:
        #     rm_data = json.load(data)
        #
        # rm_list = []
        # for i in rm_data:
        #     rm_list.append(i)
        #
        # # time_table = []  # (crn, ins_id, rm_id, day, time)
        # room_time = []
        # ins_time = []
        #
        # for i in crn_data:
        #     temp_ins = random.randint(1, 40)
        #     temp_day = random.randint(1, 5)
        #     temp_time = random.randint(1, 3)
        #     temp_rm = random.randint(0, 39)
        #     temp_rm_d_t = [temp_rm, temp_day, temp_time]
        #     temp_ins_time = [temp_ins, temp_time]
        #     while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time):
        #         if temp_rm_d_t in room_time:
        #             temp_day = random.randint(1, 5)
        #             temp_time = random.randint(1, 3)
        #             temp_rm = random.randint(0, 39)
        #             temp_rm_d_t = [temp_rm, temp_day, temp_time]
        #         if temp_ins_time in ins_time:
        #             temp_ins = random.randint(1, 40)
        #             temp_day = random.randint(1, 5)
        #             temp_time = random.randint(1, 3)
        #             temp_ins_time = [temp_ins, temp_day, temp_time]
        #
        #     room_time.append(temp_rm_d_t)  # If room time is used
        #     ins_time.append(temp_ins_time)  # If instructor is already working

        temp_timetable = self.schedule_maker()
        while temp_timetable is None:
            temp_timetable = self.schedule_maker()

        for crn in temp_timetable:
            temp_data = temp_timetable[crn]
            temp_block = Timeblock(
                temp_data[0], temp_data[1], temp_data[2], temp_data[3], temp_data[4])
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

        result = sorted(fitnessResults.items(), key=operator.itemgetter(1))
        self.stat.append(result)

        return result

    def selection(self):
        """
        Selects the best of the best in population based on eliteSize

        Returns:
        selectionResults (Array): An array with the top {eliteSize} chromosome's index and scores in tuple form (index, fitness score)
        """
        selectionResults = []
        popRanked = self.rankSchedule()

        for i in range(0, self.eliteSize):
            selectionResults.append(popRanked[i][0])

        self.stat.append(selectionResults)

        return selectionResults

    def breedPopulation(self, dirty_status=False):
        """
        Creates pools for mating based on selection results

        Returns:
        nextGenPop (Array): Next-gen population with BOB + Schedules that has been crossbred (cross-over)
        """
        matingpool = self.selection()  # best of the best (BOB)

        # clean/dirty mating pool
        if dirty_status:
            matingpool = matingpool[0:int(0.75 * self.eliteSize)]  # 75% of BOB
            for i in range(0, int(0.25 * self.eliteSize)):  # appending 25% of random
                while True:
                    rand_value = random.randint(0, self.popSize - 1)
                    if random.randint(0, self.popSize - 1) not in matingpool:
                        continue
                    else:
                        matingpool.append(rand_value)
                        break
        # num of population - len(selected)
        length = self.popSize - self.eliteSize
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
        Randomly assigns a course, instructor, room block with a day, time that's not being used to 5 timeblocks

        Parameter:
        child (Schedule): Child Schedule instance that will be mutated

        Return:
        child (Schedule): Mutated child schedule or untouched child schedule
        """
        NUM_OF_MUTATATION = 5

        if random.random() <= self.mutationRate:
            child_timeblock_list = child.get_timeblock_list()
            temp_crn_ins_rm = []

            for i in range(0, NUM_OF_MUTATATION):
                random_child_index = random.randint(
                    0,
                    len(child_timeblock_list) - 1)

                temp_crn_ins_rm = child_timeblock_list[
                    random_child_index].gene_1()
                temp_crn_ins_rm.append(random.randint(
                    1, 5))  # Randomly appends a day
                temp_crn_ins_rm.append(random.randint(
                    1, 3))  # Randomly appends a timeslot
                while (temp_crn_ins_rm in child_timeblock_list):
                    temp_crn_ins_rm.pop().pop()
                    temp_crn_ins_rm.append(random.randint(
                        1, 5))  # Randomly appends a day
                    temp_crn_ins_rm.append(random.randint(
                        1, 3))  # Randomly appends a timeslot

                child_timeblock_list.pop(
                    random_child_index)  # Removes the original timeblock
                child_timeblock_list.insert(
                    random_child_index,
                    Timeblock(temp_crn_ins_rm[0], temp_crn_ins_rm[1],
                              temp_crn_ins_rm[2], temp_crn_ins_rm[3],
                              temp_crn_ins_rm[4]))  # Inserts mutated timeblock

                temp_crn_ins_rm = []

            # Create new schedule instance to replace original
            temp_schedule = Schedule()
            for ele in child_timeblock_list:
                temp_schedule.add_timeblock(ele)

            return temp_schedule
        else:
            return child

    def mutatePopulation(self, next_gen_pop):
        """
        Mutates the crossover portion of the population

        Parameters:
        next_gen_pop (Array[Schedule])

        Returns:
        next_gen_pop (Array[Schedule]): Mutated next_gen_pop population
        """
        for index in range(0, len(next_gen_pop)):
            next_gen_pop[index] = self.mutate(
                next_gen_pop[index])

        return next_gen_pop  # Returns mutated children

    def generate_NextGenPop_clean(self):
        """
        Generates the next "clean" generation's population, automatically runs selection/crossover/mutation functions in class

        Returns:
        nextGeneration(Array[Schedules]): Next generation of schedules
        """
        # Step 1, 2, 3: Finds BOB (Selection) + Crossover for next-gen population
        nextGenPop = self.breedPopulation()
        # Step 4: Mutates Crossovered population based on mutation rate
        nextGeneration = self.mutatePopulation(nextGenPop)

        return nextGeneration, self.stat

    def generate_NextGenPop_dirty(self):
        """
        Generates the next "dirty" generation's population, automatically runs selection/crossover/mutation functions in class

        Returns:
        nextGeneration(Array[Schedules]): Next generation of schedules
        """
        # Step 1, 2, 3: Finds BOB (Selection) + Crossover for next-gen population
        nextGenPop = self.breedPopulation(True)
        # Step 4: Mutates Crossovered population based on mutation rate
        nextGeneration = self.mutatePopulation(nextGenPop)

        return nextGeneration, self.stat


def create_log(gen_depth, init_time, curr_time, stats, filename, index=None, status=None):
    """ Creates a log entry for current generation """
    if filename == "depth_log.txt":
        if gen_depth == 1:
            with open(filename, "w") as txt_file:
                txt_file.write("------Depth " +
                               str(gen_depth) + "------\n")
                txt_file.write("(Ranking)---\n")
                txt_file.write(str(stats[0]) + "\n")
                txt_file.write("(Selection)---\n")
                txt_file.write(str(stats[1]) + "\n")
                txt_file.write("Time: " + str(curr_time) + "\n\n")
        else:
            if status == "dirty":
                with open(filename, "a") as txt_file:
                    txt_file.write("Time (Dirty): " + str(curr_time) + "\n\n")
            else:
                with open(filename, "a") as txt_file:
                    txt_file.write("------Depth " + str(gen_depth) +
                                   " Node " + str(index) + " ------\n")
                    txt_file.write("(Ranking)---\n")
                    txt_file.write(str(stats[0]) + "\n")
                    txt_file.write("(Selection)---\n")
                    txt_file.write(str(stats[1]) + "\n")
                    txt_file.write("Time (Clean): " + str(curr_time) + "\n")
    if filename == "ga_log.txt":
        if gen_depth == 0:
            with open(filename, "w") as txt_file:
                txt_file.write("------Generation " +
                               str(gen_depth + 1) + "------\n")
                txt_file.write("(Ranking)---\n")
                txt_file.write(str(stats[0]) + "\n")
                txt_file.write("(Selection)---\n")
                txt_file.write(str(stats[1]) + "\n")
                txt_file.write("Time: " + str(curr_time) + "\n\n")
        else:
            with open(filename, "a") as txt_file:
                txt_file.write("------Generation " +
                               str(gen_depth + 1) + "------\n")
                txt_file.write("(Ranking)---\n")
                txt_file.write(str(stats[0]) + "\n")
                txt_file.write("(Selection)---\n")
                txt_file.write(str(stats[1]) + "\n")
                txt_file.write("Time: " + str(curr_time) + "\n\n")
    if "depth" in filename:
        if gen_depth == 1:
            with open(filename, "w", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Depth", "Node", "Type", "Ranking", "BOBs",
                                 "Time for Generation", "Time since Initiation"])
                writer.writerow([gen_depth, index, status, stats[0],
                                 stats[1], curr_time, init_time])
        else:
            with open(filename, "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([str(gen_depth), index, status, stats[0],
                                 stats[1], curr_time, init_time])
    if "ga" in filename:
        if gen_depth == 0:
            with open(filename, "w", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Generation", "Ranking", "BOBs",
                                 "Time for Generation", "Time since Initiation"])
                writer.writerow(
                    [gen_depth + 1, stats[0], stats[1], curr_time, init_time])
        else:
            with open(filename, "a", newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    [gen_depth + 1, stats[0], stats[1], curr_time, init_time])


if __name__ == "__main__":
    POP_SIZE = 100
    ELITE_SIZE = int(POP_SIZE * 0.2)
    MUTATION_RATE = 0.15

    GA_TERMINATION_CRITERION = 0
    IDS_TERMINATION_RATIO = 0.2

    ids_termination_criterion = False
    depth_count = 0
    next_gen_pop = []
    temp_next_gen_pop = []  # Container for temp population storage
    initial_fitness = None  # Comparison for termination criterion

    stats = [[[0, 999]]]
    reset_stat = []
    init_time = time()

    USE_IDS = False

    # depth_log_name = "depth_log.csv"
    # ga_log_name = "ga_log.csv"

    ga_log_name = "ga_log_pop" + str(POP_SIZE) + ".csv"
    depth_log_name = "depth_log_pop" + str(POP_SIZE) + ".csv"

    if USE_IDS:
         # for each layer/depth level, append each node/population into next_gen_pop
        while ids_termination_criterion is False:
            if time() - init_time > 4800:
                break
            next_gen_pop = temp_next_gen_pop
            temp_next_gen_pop = []  # resets temp container
            depth_count += 1

            if depth_count is 1:
                print("Depth", str(depth_count), "in progress")
                s_time = time()
                tt_ga = GeneticAlgorithm(POP_SIZE, ELITE_SIZE,
                                         MUTATION_RATE)
                # Mating pool 1
                results = tt_ga.generate_NextGenPop_clean()
                temp_next_gen_pop.append(results[0])
                stats = results[1]
                initial_fitness = stats[0][0][1]
                create_log(depth_count, time() - init_time, time() -
                           s_time, stats, depth_log_name)
                # Mating pool 2
                results_1 = tt_ga.generate_NextGenPop_dirty()
                temp_next_gen_pop.append(results_1[0])
                stats = results_1[1]
                create_log(depth_count, time() - init_time, time() -
                           s_time, stats, depth_log_name)
            elif (depth_count % 5) is 0:
                # Resets IDS node population every 4 depth
                print("Depth", str(depth_count), "in progress")
                s_time = time()
                min_index = reset_stat.index(min(reset_stat))
                reset_pop = next_gen_pop[min_index]

                # Mating pool 1
                results = tt_ga.generate_NextGenPop_clean()
                temp_next_gen_pop.append(results[0])
                stats = results[1]
                initial_fitness = stats[0][0][1]
                create_log(depth_count, time() - init_time, time() -
                           s_time, stats, depth_log_name)

                # Mating pool 2
                results_1 = tt_ga.generate_NextGenPop_dirty()
                temp_next_gen_pop.append(results_1[0])
                stats = results_1[1]
                create_log(depth_count, time() - init_time, time() -
                           s_time, stats, depth_log_name)

            else:
                for i, pop in enumerate(next_gen_pop):
                    s_time = time()
                    print("Depth", str(depth_count),
                          "Node", str(i), "in progress")
                    del tt_ga
                    tt_ga = GeneticAlgorithm(POP_SIZE, ELITE_SIZE,
                                             MUTATION_RATE, pop)

                    # Mating pool 1
                    results = tt_ga.generate_NextGenPop_clean()
                    temp_next_gen_pop.append(results[0])
                    stats = results[1]
                    create_log(depth_count, time() - init_time, time() - s_time,
                               stats, depth_log_name, i, "clean")
                    if (depth_count % 5) is 4:
                        reset_stat.append(stats[0][0][1])
                    if (1 - (stats[0][0][1] / initial_fitness) > IDS_TERMINATION_RATIO):
                        ids_termination_criterion = True
                        print("IDS Termination Criterion fulfilled---")
                        print("Current Depth:", str(depth_count))
                        print("Current Node:", str(i))
                        next_gen_pop = results[0]
                        stats = stats
                        break

                    # Mating pool 2
                    s_time = time()
                    results_1 = tt_ga.generate_NextGenPop_dirty()
                    temp_next_gen_pop.append(results_1[0])
                    stats_1 = results_1[1]
                    if (depth_count % 5) is 4:
                        reset_stat.append(stats_1[0][0][1])
                    create_log(depth_count, time() - init_time, time() - s_time,
                               stats_1, depth_log_name, i, "dirty")
                    if (1 - (stats_1[0][0][1] / initial_fitness) > IDS_TERMINATION_RATIO):
                        ids_termination_criterion = True
                        print("IDS Termination Criterion fulfilled---")
                        print("Current Depth:", str(depth_count))
                        print("Current Node:", str(i))
                        next_gen_pop = results_1[0]
                        stats = stats_1
                        break
    else:
        gen_count = 0

        while stats[0][0][1] > GA_TERMINATION_CRITERION:
            if time() - init_time > 4800:
                break
            s_time = time()
            print("Generation", str(gen_count + 1), "in progress")
            if next_gen_pop == []:  # For first generation
                tt_ga = GeneticAlgorithm(POP_SIZE, ELITE_SIZE,
                                         MUTATION_RATE)
                results = tt_ga.generate_NextGenPop_clean()
                next_gen_pop = results[0]
                stats = results[1]
            else:
                del tt_ga
                tt_ga = GeneticAlgorithm(POP_SIZE, ELITE_SIZE,
                                         MUTATION_RATE, next_gen_pop)
                results = tt_ga.generate_NextGenPop_clean()
                next_gen_pop = results[0]
                stats = results[1]
            create_log(gen_count, time() - init_time,
                       time() - s_time, stats, ga_log_name)
            gen_count += 1

        for i, schedule in enumerate(next_gen_pop):
            if score_time_table(schedule) is 0 and i is 0:
                with open("schedule.txt", "w") as txt_file:
                    txt_file.write("------Schedule " + str(i) + " ------\n")
                    for timeblock in schedule.get_timeblock_list():
                        txt_file.write("[%s, %s, %s, %s, %s]\n" % (
                            timeblock[0], timeblock[1], timeblock[2], timeblock[3], timeblock[4]))
                    txt_file.write("\n")
            else:
                with open("schedule.txt", "a") as txt_file:
                    txt_file.write("------Schedule " + str(i) + " ------\n")
                    for timeblock in schedule.get_timeblock_list():
                        txt_file.write("[%s, %s, %s, %s, %s]\n" % (
                            timeblock[0], timeblock[1], timeblock[2], timeblock[3], timeblock[4]))
                    txt_file.write("\n")
        print("GA Termination Criterion fulfilled---")
        print("Generation count: ", str(gen_count))
