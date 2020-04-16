import json

with open('ins_file.json') as json_file:
    ins_data = json.load(json_file)

temp_data = {}
for i in ins_data:
    temp_data[i] = ins_data[i]
    temp_data[i]['pref'] = {
                            "day_location": {
                                    '1': ['D', 'B'],
                                    '2': ['D', 'B'],
                                    '3': ['D', 'B'],
                                    '4': ['D', 'B'],
                                    '5': ['D', 'B'],
                            },
                            "day_time": {
                                    '1': [1, 2, 3],
                                    '2': [1, 2, 3],
                                    '3': [1, 2, 3],
                                    '4': [1, 2, 3],
                                    '5': [1, 2, 3],
                            },
                            }


with open("ins_file.json", "w") as write_file:
    json.dump(temp_data, write_file)