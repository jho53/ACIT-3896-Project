import json
import csv

# pref in Json file is follow format:
# [{"location": {"like": "", "disklike": ""}}, {"time": {"like": "xx,xx,xx", "dislike": "xx"}}]
# If one pref["like"] is satisfied, score + 1, else if one pref["dislike"] is matched, score -1


# Check if instructor has any preference
def has_pref(ins_id, ins_data):
    return ins_data[ins_id]["pref"] is not None and len(ins_data[ins_id]["pref"]) > 0


# Match pref with current row in the csv file
def match_pref(row, ins_data, score):
    # row[1] is the instructor id
    instructor_id = row[1]
    preferences = ins_data[instructor_id]["pref"]
    # preferences[0] - first element is location
    if preferences[0]["location"]["like"] != "":
        if preferences[0]["location"]["like"] in row[2]:
            score += 1
        elif preferences[0]["location"]["dislike"] in row[2]:
            score -= 1

    time_str = row[3] + row[4]

    # preferences[1] - second element is time
    if preferences[1]["time"]["like"] != "":
        if time_str in preferences[1]["time"]["like"]:
            score += 1
        elif time_str in preferences[1]["time"]["dislike"]:
            score -= 1

    return score


# Ranking the time table
def score_time_table():
    score = 0
    # Load Instructors
    with open("./data files/ins_file.json", "r") as data:
        ins_data = json.load(data)

    # Load time table
    with open('timetable.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # print(ins_data["1"])
        for row in readCSV:
            if has_pref(row[1], ins_data):
                # Match preference
                score = match_pref(row, ins_data, score)

    # Output score
    print("total score is: " + str(score))


# def main():
#     score_time_table()
#
#
# if __name__ == "__main__":
#     main()
