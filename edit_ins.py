import json

with open("ins_file.json", "r") as data:
    ins_data = json.load(data)

total_course_list = {}
for i in ins_data:
    for j in ins_data[i]['course']:
        if j not in total_course_list:
            total_course_list[j] = 1
        else:
            total_course_list[j] += 1

for i in total_course_list:
    if total_course_list[i] > 3:
        print(i, total_course_list[i])

# with open("ins_file2.json", "w") as write_file:
#     json.dump(ins_data, write_file)