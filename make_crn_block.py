import json
import csv
from random import randint


def make_new_timetable():
    with open("data files/crn_file.json", "r") as data:
        crn_data = json.load(data)

    with open("ins_file.json", "r") as data:
        ins_data = json.load(data)

    with open("data files/rm_file.json", "r") as data:
        rm_data = json.load(data)

    rm_list = []
    for i in rm_data:
        rm_list.append(i)

    rm_list = sorted(rm_list)

    time_table = {}
    # (crn, ins_id, rm_id, day, time)
    room_time = []
    ins_time = []
    ins_campus = {}
    for i in ins_data:
        ins_campus[i] = {
            1: '',
            2: '',
            3: '',
            4: '',
            5: ''
        }

    course_ins = {}
    for i in ins_data:
        for j in ins_data[i]['course']:
            course_ins[j] = []

    for i in ins_data:
        for j in ins_data[i]['course']:
            course_ins[j].append(i)

    for i in crn_data:
        if i[:-3] == 'CIT':
            temp_day = randint(1, 5)
            temp_time = randint(1, 3)
            temp_rm = randint(20, 39)
            temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]

            temp_rm_d_t = [temp_rm, temp_day, temp_time]
            temp_ins_time = [temp_ins, temp_day, temp_time]

            while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time) or (ins_campus[temp_ins][temp_day] == 'B'):
                if (temp_rm_d_t in room_time) and (temp_ins_time in ins_time):
                    temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                    temp_rm = randint(20, 39)
                elif temp_rm_d_t in room_time:
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                    temp_rm = randint(20, 39)
                elif temp_ins_time in ins_time:
                    temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                else:
                    temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                    temp_rm = randint(20, 39)
                temp_rm_d_t = [temp_rm, temp_day, temp_time]
                temp_ins_time = [temp_ins, temp_day, temp_time]
        else:
            temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
            temp_day = randint(1, 5)
            temp_time = randint(1, 3)
            temp_rm = randint(0, 39)
            temp_rm_d_t = [temp_rm, temp_day, temp_time]
            temp_ins_time = [temp_ins, temp_day, temp_time]

            while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time) or \
                    (((ins_campus[temp_ins][temp_day] == 'D') and temp_rm < 20) or ((ins_campus[temp_ins][temp_day] == 'B') and temp_rm > 20)):
                if (temp_rm_d_t in room_time) and (temp_ins_time in ins_time):
                    temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                    temp_rm = randint(0, 39)
                elif temp_rm_d_t in room_time:
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                    temp_rm = randint(0, 39)
                elif temp_ins_time in ins_time:
                    temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                    temp_day = randint(1, 5)
                    temp_time = randint(1, 3)
                else:
                    if ins_campus[temp_ins][temp_day] == 'D':
                        temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
                        temp_day = randint(1, 5)
                        temp_time = randint(1, 3)
                        temp_rm = randint(20, 39)
                    elif ins_campus[temp_ins][temp_day] == 'B':
                        temp_ins = course_ins[i[:-1]][(randint(1, len(course_ins[i[:-1]])) - 1)]
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

    ins_course = {}
    for i in ins_data:
        ins_course[i] = []

    for i in time_table:
        ins_course[time_table[i][1]].append(time_table[i])

    with open('new_timetable.json', 'w') as file:
        json.dump(time_table, file)

    with open('ins_course.json', 'w') as file:
        json.dump(ins_course, file)

make_new_timetable()