import json

with open('courses-202010.json') as json_file:
    c_data = json.load(json_file)

with open('schedule-202010.json') as json_file:
    s_data = json.load(json_file)


p = 'programs'
c = 'courses'
s = 'sets'

cr = 'crns'

ins = 'instructors'
rm = 'rooms'


def get_crn_list():
    # Return list of all CRNs
    crn_list = []
    for crn in c_data[cr]:
        crn_list.append(crn)
    return crn_list


def get_course_list():
    # Return list of all Courses
    course_list = []
    for course in c_data[c]:
        course_list.append(course)
    return course_list


def get_ins_crn_list(ins_id):
    # Return list of CRNs the instructor teaches(from example schedule)
    if type(ins_id) is str:
        return s_data[ins][ins_id][cr]
    return s_data[ins][str(ins_id)][cr]


def get_course_by_crn(crn):
    # Return the course code by crn
    if type(crn) is str:
        return c_data[cr][crn]['course']
    return c_data[cr][str(crn)]['course']


def get_set_by_crn(crn):
    # Return the Set number of the crn
    if type(crn) is str:
        return c_data[cr][crn]['program']['sets']
    return c_data[cr][str(crn)]['program']['sets']


def get_program_by_crn(crn):
    # Return the program prefix of the crn
    if type(crn) is str:
        return c_data[cr][crn]['program']['prefix']
    return c_data[cr][str(crn)]['program']['prefix']


def get_crn_by_course_id(course_id):
    # Return list of CRNs with the course_id
    return c_data[c][course_id][cr]

