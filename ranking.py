import json
import csv

# pref in Json file is follow format:
# [{"location": {"like": "", "disklike": ""}}, {"time": {"like": "xx,xx,xx", "dislike": "xx"}}]
# If one pref["like"] is satisfied, score + 1, else if one pref["dislike"] is matched, score -1


# Check if instructor has any preference
def has_pref(ins_id, ins_data):
    return ins_data[ins_id]["pref"] is not None and len(ins_data[ins_id]["pref"]) > 0

#
# Match pref with current row in the csv file
def match_pref(row, ins_data, score):

    return score


# Ranking the time table
def score_time_table():
    score = 0
    # Load Instructors
    with open("ins_file.json", "r") as data:
        ins_data = json.load(data)

    time_table = []
    # Load time table
    with open('new_timetable.csv', "r") as csvfile:
        csv_data = csv.reader(csvfile, delimiter=',')
        for course in csv_data:
            time_table.append(course)

    for ins_id in ins_data:
        ins_course = []
        if has_pref(ins_id, ins_data):
            for course in time_table:
                if course[1] == ins_id:
                    ins_course.append(course)
            for i in ins_course:
                print(i)
            print('-----------------')


    # Output score
    print("total score is: " + str(score))


def main():
    score_time_table()


if __name__ == "__main__":
    main()
