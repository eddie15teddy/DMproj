# The code was used to generate the test dataset.

import csv
import numpy as np

def generate_2d_normal_data(mean_x=0, mean_y=0, std_x=1, std_y=1, n_points=100):
    x = np.random.normal(loc=mean_x, scale=std_x, size=n_points)
    y = np.random.normal(loc=mean_y, scale=std_y, size=n_points)
    data = np.column_stack((x, y))
    return data

def generate_2d_random_walk(n_points=100, step_size=1000, start_x=0, start_y=0, seed=None):
    if seed is not None:
        np.random.seed(seed)
    x, y = [start_x], [start_y]
    for _ in range(1, n_points):
        step_x = np.random.uniform(-step_size, step_size)
        step_y = np.random.uniform(-step_size, step_size)
        x.append(x[-1] + step_x)
        y.append(y[-1] + step_y)
    data = np.column_stack((x, y))
    return data

data1 = generate_2d_normal_data(mean_x=15000, mean_y=3000, std_x=2000, std_y=5000, n_points=500)
data2 = generate_2d_normal_data(mean_x=10000, mean_y=20000, std_x=7400, std_y=4400, n_points=1000)

data3 = generate_2d_random_walk(n_points=450, step_size=1200, start_x=20000, start_y=30000, seed=1)
data4 = generate_2d_normal_data(mean_x=6500, mean_y=0, std_x=7400, std_y=4400, n_points=250)

data_comp_starting = np.vstack((data1, data2))
data_comp_additional = np.vstack((data3, data4))
np.random.shuffle(data_comp_additional)

data_dict_starting = [{"X": row[0], "Y": row[1]} for row in data_comp_starting]
data_dict_additional = [{"X": row[0], "Y": row[1]} for row in data_comp_additional]

filePathStarting = "testdata.csv"

with open(filePathStarting, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["X", "Y"])
    writer.writeheader()
    writer.writerows(data_dict_starting)

filePathAdditional = "additionaldata.csv"

with open(filePathAdditional, mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["X", "Y"])
    writer.writeheader()
    writer.writerows(data_dict_additional)