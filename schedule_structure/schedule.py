from .timeblock import Timeblock
import operator


class Schedule:
    """Represents a timetable/schedule"""

    def __init__(self):
        """Initiates instance of schedule"""
        self.timeblock_list = []

    def add_timeblock(self, timeblock_obj):
        """Appends a timeblock to schedule"""
        self.timeblock_list.append(timeblock_obj)

    def get_timeblock_list(self):
        """Returns timeblock list sorted by day and timeslot"""
        return sorted(self.timeblock_list)

    def display_schedule(self):
        """Prints timeblocks within schedule"""
        for timeblock in self.get_timeblock_list():
            print(timeblock.get_time_block())
        return True

    def get_schedule(self):
        """Prints timeblocks within schedule"""
        num_ins = 40
        temp_schedule = {}
        for i in range(1, num_ins+1):
            temp_schedule[i] = []

        for timeblock in self.get_timeblock_list():
            temp_block = timeblock.get_time_block_2()
            temp_schedule[temp_block[1]].append(temp_block)
        return temp_schedule
