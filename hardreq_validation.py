from schedule_structure.schedule import Schedule
from schedule_structure.timeblock import Timeblock

import os

temp_info = []


def testing(current_path):
    current_path += "\\timetable.csv"

    sch_1 = Schedule()

    with open(current_path, "r") as read_csv_file:
        for line in read_csv_file:
            timeblock_list = line.split(",")
            temp_timeblock = Timeblock(timeblock_list[0], timeblock_list[1],
                                       timeblock_list[2], timeblock_list[3],
                                       timeblock_list[4][:-1])
            sch_1.add_timeblock(temp_timeblock)

        sch_1.display_schedule()


def main():
    '''
    **-8:30-5:20.
    -Instructors cannot be on 2 campuses on the same day
    -Instructors can’t be in two rooms at once… except 5-week courses for CST and project courses for CIT maybe? Not sure on the 5-week for FSWD as we have never run it before.
    -CIT electives should be on Thursday.
    -CST DTC should be biased to 645, 655, and 665.
    -CIT DTC should be biased to the rooms in the tech hub.
    -CST and CIT bias for certain courses may be different (for example math instructors don’t live 645, 655, 665 for lecture).
    -Students may not have more than 5 hours in a row
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


if __name__ == "__main__":
    testing(os.getcwd())