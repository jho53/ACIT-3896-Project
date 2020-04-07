from schedule_structure.schedule import Schedule
from schedule_structure.timeblock import Timeblock
import time
import itertools
import make_crn_block as mk

import os
import sys

temp_info = []
sch_1 = Schedule()

def testing(current_path):
    current_path += "\\new_timetable.csv"

def testing(current_path):
    current_path += "\\timetable.csv"

    with open(current_path, "r") as read_csv_file:
        for line in read_csv_file:
            timeblock_list = line.split(",")
            temp_timeblock = Timeblock(timeblock_list[0], timeblock_list[1],
                                       timeblock_list[2], timeblock_list[3],
                                       timeblock_list[4][:-1])
            sch_1.add_timeblock(temp_timeblock)


def hardreq_validation(schedule):
    '''Checks if schedule fulfills hard requirements, returns False if no'''
    '''
    **-8:30-5:20.
    **-Instructors cannot be on 2 campuses on the same day
    **-Instructors can’t be in two rooms at once… except 5-week courses for CST and project courses for CIT maybe? Not sure on the 5-week for FSWD as we have never run it before.
    -CIT electives should be on Thursday.
    -CST DTC should be biased to 645, 655, and 665.
    -CIT DTC should be biased to the rooms in the tech hub.
    -CST and CIT bias for certain courses may be different (for example math instructors don’t live 645, 655, 665 for lecture).
    # -Students may not have more than 5 hours in a row
    -Students should not have more than a 3 hour break
    -CST lectures should be 2 hours in a row, except for lectures with 3 hours. Lectures with 3 hours should have 1 hour on Monday and the other 2 on another day.
    -CST should have labs after all lectures. If that can’t happen labs before all lectures. If it is 3 hour lecture then labs can be between the 1 and 2 hour preferred. If that can’t happen then ok, but really don’t want to e some labs lecture some labs
    -CST labs and lectures should be as close to each other as possible for a given course in terms of time
    -CST BBY should not move buildings very often, if possible
    -CST DTC should try to have the same class on the same day for both sets
    -Instructors should also not teach more than 5 hours without a break, some instructors are OK with not having a break for 8 hours though
    '''
    '''
    Jimmy's notes:
        Time based hard constraints are basically solved, just need to make sure dummy data is compatible
    '''

    violation_count = 0

    timeblock_combinations = list(
        itertools.combinations(
            sch_1.get_timeblock_list(),
            2))  # Takes all combinations of timeblocks in schedule

    violation_counter = 0

    for ele in timeblock_combinations:
        try:
            # ele[0] for 1st timeblock, ele[1] for 2nd timeblock

            # Validation 1: Instructors cannot be in two rooms at once
            if ((ele[0].get_instructor() == ele[1].get_instructor()) and
                (ele[0].day == ele[1].day)) and (
                    ele[0].timeslot == ele[1].timeslot) and (ele[0].room !=
                                                             ele[1].room):
                # print(ele[0].get_time_block(), ele[1].get_time_block())
                # print("Instructors cannot be in two rooms at once")

                violation_count += 1

            # Validation 2: Instructors cannot be on 2 campuses on same day
            if (ele[0].get_instructor() == ele[1].get_instructor()) and (
                    ele[0].day == ele[1].day) and (ele[0].room[0] !=
                                                   ele[1].room[0]):
                # print(ele[0].get_time_block(), ele[1].get_time_block())
                # print("Instructors cannot be on 2 campuses on the same day")
                violation_count += 1

            # Validation 3: Each set should only have 2 classes for CIT

            # Validation 4: Electives must be on thursday for CIT

            # Validation 5: ISSP must be on Friday for CIT for term 3 + 4

            # Validation 6: Students cannot have more than 5 hour break

            # Validation 7: Wednesday should always be a short day

        except Exception as error:
            print(error)
            return False

    return violation_count


if __name__ == "__main__":
    testing(os.getcwd())
    start_time = time.time()
    print(hardreq_validation(sch_1))
    print(sch_1.display_schedule())
    print(time.time() - start_time)

