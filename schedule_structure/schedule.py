import pprint
from .timeblock import Timeblock


class Schedule:
    """Represents a timetable/schedule"""

    def __init__(self):
        """Initiates instance of schedule"""
        self.timeblock_list = []

    def add_timeblock(self, timeblock_obj):
        """Appends a timeblock to schedule"""
        self.timeblock_list.append(timeblock_obj)

    def display_schedule(self):
        """Prints timeblocks within schedule"""
        for timeblock in self.timeblock_list:
            print(timeblock.get_time_block())
