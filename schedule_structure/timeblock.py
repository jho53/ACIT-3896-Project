class Timeblock:
    """Represents a timeblock within timetable"""

    def __init__(self, crn, ins_id, rm_id, day, timeslot):
        """Init
        Arguments:
            crn: String, unique ID for courses
            ins_id: int, unique ID for instructors
            rm_id: String, represents location and room
        """
        self._crn = crn
        self._ins_id = ins_id
        self._rm_id = rm_id

        self._day = day
        self._timeslot = timeslot

    def get_time_block(self):
        '''Get timeblock in tuple format'''
        return (self._crn, self._ins_id, self._rm_id, self._day,
                self._timeslot)

    def get_time_block_2(self):
        '''Get timeblock in list format'''
        return [self._crn, self._ins_id, self._rm_id, self._day,
                self._timeslot]

    def get_crn(self):
        """Returns CRN"""
        return self._crn

    def get_instructor(self):
        """Returns instructor ID"""
        return self._ins_id

    @property
    def day(self):
        """Returns day in timeblock"""
        return self._day

    @day.setter
    def day(self, day):
        '''Sets day in timeblock'''
        self._day = day

    @property
    def room(self):
        '''Sets room based on room_id'''
        return self._rm_id

    @room.setter
    def room(self, rm_id):
        '''Sets room based on room_id'''
        self._rm_id = rm_id

    @property
    def timeslot(self):
        '''Sets timeslot based on timeslot id'''
        return self._timeslot

    @timeslot.setter
    def timeslot(self, timeslot):
        '''Sets timeslot based on timeslot id'''
        self._timeslot = timeslot

    def gene_1(self):
        """Used for crossover, returns array of CRN, Instructor ID and Room ID"""
        return [self._crn, self._ins_id, self._rm_id]

    def gene_2(self):
        """Used for crossover, returns array of day and timeslot"""
        return [self.day, self.timeslot]

    def __lt__(self, other):
        """Custom lt for timeblocks based on day and timeslot"""
        return (self.get_crn(),
                self.get_instructor()) < (other.get_crn(),
                                          other.get_instructor())

        # return (int(self._day), int(self._timeslot)) < (int(other._day),
        #                                                 int(other._timeslot))
