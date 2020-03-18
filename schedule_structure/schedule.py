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
