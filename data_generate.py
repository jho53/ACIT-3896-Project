import json

num_ins = 40
num_rm = 20
num_term = 4
cit_num_set = 3
cst_num_set = 6
num_course = 7

# Instructor
ins_list = {}
for i in range(num_ins):
    temp_ins = {"id": i + 1, "course": [], "pref": []}
    ins_list[i + 1] = temp_ins

# with open("ins_file.json", "w") as write_file:
#     json.dump(ins_list, write_file)

# Room
rm_list = {}

for i in range(num_rm):
    if i > 13:
        temp_cap = 60
    else:
        temp_cap = 30

    temp_id_D = 'D' + str(i + 1)
    temp_id_B = 'B' + str(i + 1)

    temp_rm_D = {"id": temp_id_D, "cap": temp_cap}

    temp_rm_B = {"id": temp_id_B, "cap": temp_cap}
    rm_list[temp_id_D] = temp_rm_D
    rm_list[temp_id_B] = temp_rm_B

# with open("rm_file.json", "w") as write_file:
#    json.dump(rm_list, write_file)

# Set
set_list = {}
for term in range(num_term):
    for set1 in range(cit_num_set):
        temp_set_id = "CIT" + str(term + 1) + str(set1 + 1)
        temp_set = {"set": temp_set_id, "program": "CIT", "crns": []}
        set_list[temp_set_id] = temp_set
    for set2 in range(cst_num_set):
        temp_set_id = "CST" + str(term + 1) + str(set2 + 1)
        temp_set = {"set": temp_set_id, "program": "CST", "crns": []}
        set_list[temp_set_id] = temp_set

# Crn(Course)
crn_list = {}

for term in range(num_term):
    for course in range(num_course):
        for set1 in range(cit_num_set):
            temp_cit_crn = "CIT" + str(term + 1) + str(course + 1) + str(set1 +
                                                                         1)
            temp_cap = 30
            temp_crn_cit = {
                "crn": temp_cit_crn,
                "course": "CIT" + str(term + 1) + str(course + 1),
                "cap": temp_cap
            }
            crn_list[temp_cit_crn] = temp_crn_cit
            set_list["CIT" + str(term + 1) +
                     str(set1 + 1)]["crns"].append(temp_cit_crn)

        for set2 in range(cst_num_set):
            temp_cst_crn = "CST" + str(term + 1) + str(course + 1) + str(set2 +
                                                                         1)
            temp_cap = 30
            temp_crn_cst = {
                "crn": temp_cst_crn,
                "course": "CST" + str(term + 1) + str(course + 1),
                "cap": temp_cap
            }
            crn_list[temp_cst_crn] = temp_crn_cst
            set_list["CST" + str(term + 1) +
                     str(set2 + 1)]["crns"].append(temp_cst_crn)

# with open("crn_file.json", "w") as write_file:
#     json.dump(crn_list, write_file)
# with open("set_file.json", "w") as write_file:
#     json.dump(set_list, write_file)

# Empty preference

pref_data = {}
for i in range(1, 10):
    pref_data[i] = {'id':i, 'desc':''}

with open("pref_file.json", "w") as write_file:
    json.dump(pref_data, write_file)
