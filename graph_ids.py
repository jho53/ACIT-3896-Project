from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

import csv

score_array_1 = []
time_array_1 = []

score_array_2 = []
time_array_2 = []

with open('depth_log_pop100.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for i in csv_reader:
        # get lowest score from list
        temp_score = i[3]
        temp_score = temp_score[1:-1:]
        temp_score = temp_score.split('),')
        temp_lowest = temp_score[0][1::].split(',')
        score_array_1.append(int(temp_lowest[1]))

        # get time
        time_array_1.append(float(i[6]))

with open('depth_log_pop500.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    for i in csv_reader:
        # get lowest score from list
        temp_score = i[3]
        temp_score = temp_score[1:-1:]
        temp_score = temp_score.split('),')
        temp_lowest = temp_score[0][1::].split(',')
        score_array_2.append(int(temp_lowest[1]))

        # get time
        time_array_2.append(float(i[6]))


x1 = np.array(time_array_1)
y1 = np.array(score_array_1)

x2 = np.array(time_array_2)
y2 = np.array(score_array_2)

def func(x, a, b, c):
    return a*np.exp(-b*x) + c


# popt1, pcov1 = curve_fit(func, x1, y1)
# popt2, pcov2 = curve_fit(func, x2, y2)
plt.figure(figsize=(10, 6))
idsga100_data = plt.plot(x1, y1, label="IDS-GA (Population: 100)")
idsga500_data = plt.plot(x2, y2, label="IDS-GA (Population: 500)")

# f1 = plt.plot(x1, func(x1, popt1[0], popt1[1], popt1[2]), label="Fitted Curve (GA POP100)")
# f2 = plt.plot(x2, func(x2, popt2[0], popt2[1], popt2[2]), label="Fitted Curve (GA POP500)")

plt.xlabel("Time (s)")
plt.ylabel("Fitness Score (Lower is Better)")
plt.title("IDSGA (Population: 100) vs IDSGA (Population: 500)")
plt.legend()
plt.show()

