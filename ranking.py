import json

# pref in Json file is follow format:
# [{"location": {"like": "", "disklike": ""}}, {"time": {"like": "xx,xx,xx", "dislike": "xx"}}]
# If one pref["like"] is satisfied, score + 1, else if one pref["dislike"] is matched, score -1


# Check if instructor has any preference
def has_pref(ins_id, ins_json):
    return ins_json[ins_id]["pref"] is not None and len(ins_json[ins_id]["pref"]) > 0


# Get instructor time table
def get_inst_timetable(ins_id, ins_course_table):
    return ins_course_table[ins_id]


# Get instructor pref by id
def get_inst_pref_by_id(ins_id, instructors):
    return instructors[ins_id]["pref"]


# Match pref with current row in the csv file
def match_pref(instructors, ins_course_table, score):
    for instructor_id in ins_course_table:
        if has_pref(instructor_id, instructors):
            temp_course_time = [[], [], [], [], []]
            temp_course_location = [[], [], [], [], []]
            day_list = ['1', '2', '3', '4', '5']
            ins_timetable = get_inst_timetable(instructor_id, ins_course_table)
            ins_pref = get_inst_pref_by_id(instructor_id, instructors)
            for course in ins_timetable:
                temp_course_time[course[3]-1].append(course[4])
                temp_course_location[course[3]-1].append(course[2][0])

            for i in range(len(day_list)):
                for location in temp_course_location[i]:
                    if location not in ins_pref['day_location'][day_list[i]]:
                        score += 1
                for time in temp_course_time[i]:
                    if time not in ins_pref['day_time'][day_list[i]]:
                        score += 1

    return score


# Ranking the time table
def score_time_table(ins_course_schedule):

    # initial score
    score = 0

    # Load Instructors
    with open("ins_file.json", "r") as ins_data:
        instructors = json.load(ins_data)

    # Match preferences
    score = match_pref(instructors, ins_course_schedule, score)

    return score


