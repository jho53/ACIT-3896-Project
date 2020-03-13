class Timeblock:
    """Represents a timeblock within timetable"""

    def __init__(self, crn, ins_id, rm_id, day, timeslot):
        """Init
        Arguments:
            crn: String, unique ID for courses
            ins_id: int, unique ID for instructors
            rm_id: String, represents location and room
        """
        self.crn = crn
        self.ins_id = ins_id
        self.rm_id = rm_id

        self.day = day
        self.timeslot = timeslot

    def get_time_block(self):
        '''Get timeblock in tuple format'''
        return (self.crn, self.ins_id, self.rm_id, self.day, self.timeslot)

    def set_day(self, day):
        '''Sets day in timeblock'''
        self.day = day

    def set_room(self, rm_id):
        '''Sets room based on room_id'''
        self.rm_id = rm_id

    def set_timeslot(self, timeslot):
        '''Sets timeslot based on timeslot id'''
        self.timeslot = timeslot
