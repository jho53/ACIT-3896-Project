import json
import csv
from random import randint

with open("crn_file.json", "r") as data:
    crn_data = json.load(data)

with open("ins_file.json", "r") as data:
    ins_data = json.load(data)

with open("rm_file.json", "r") as data:
    rm_data = json.load(data)

rm_list = []
for i in rm_data:
    rm_list.append(i)

time_table = []
# (crn, ins_id, rm_id, day, time)
room_time = []
ins_time = []

for i in crn_data:
    temp_ins = randint(1, 40)
    temp_day = randint(1, 5)
    temp_time = randint(1, 3)
    temp_rm = randint(0, 39)
    temp_rm_d_t = [temp_rm, temp_day, temp_time]
    temp_ins_time = [temp_ins, temp_time]
    while (temp_rm_d_t in room_time) or (temp_ins_time in ins_time):
        if temp_rm_d_t in room_time:
            temp_day = randint(1, 5)
            temp_time = randint(1, 3)
            temp_rm = randint(0, 39)
            temp_rm_d_t = [temp_rm, temp_day, temp_time]
        if temp_ins_time in ins_time:
            temp_ins = randint(1, 40)
            temp_day = randint(1, 5)
            temp_time = randint(1, 3)
            temp_ins_time = [temp_ins, temp_day, temp_time]

    room_time.append(temp_rm_d_t)
    ins_time.append(temp_ins_time)
    temp_block = [i, temp_ins, rm_list[temp_rm], temp_day, temp_time]
    time_table.append(temp_block)

with open('timetable.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in time_table:
        writer.writerow(i)
