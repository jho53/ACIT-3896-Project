from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import ast
import csv

index_array_1 = []
time_array_1 = []

index_array_2 = []
time_array_2 = []

with open('depth_log_pop100.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for i in csv_reader:
        # get lowest score from list
        temp_score = ast.literal_eval(i[3])
        temp_index_list = []
        temp_score = temp_score[:20]
        for tup in temp_score:
            temp_index_list.append(tup[0])
        index_array_1.append(temp_index_list)

        # get time
        time_array_1.append(float(i[6]))

with open('ga_log_pop100.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for i in csv_reader:
        # get lowest score from list
        temp_score = ast.literal_eval(i[1])
        temp_index_list = []
        temp_score = temp_score[:20]
        for tup in temp_score:
            temp_index_list.append(tup[0])
        index_array_2.append(temp_index_list)

        # get time
        time_array_2.append(float(i[4]))

plt.figure(figsize=(15, 8))
for xe, ye in zip(time_array_2, index_array_2):
    plt.scatter([xe] * len(ye), ye, s=3)

plt.show()

