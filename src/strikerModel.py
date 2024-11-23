#!/usr/local/bin/python3

#import matplotlib.pyplot as plt
#import matplotlib.patches as patches
#import numpy as np
#import pandas as pd
import requests
import json
import csv
#import strikerImage as image
import os
#from sklearn.linear_model import LinearRegression
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.metrics import mean_squared_error, r2_score

#
# Filter the list of dictionaries where "total" equals the specified value
#
def filter_csv_by_total(csv_list, total_value):
    filtered_list = [row for row in csv_list if row.get("total") == str(total_value)]
    return filtered_list

#
#
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

#
#
# Reads a CSV file into a list of dictionaries.
#
def read_csv_to_dict(filename):
    print(filename)
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

#
# Separates rows into two lists based on the value of the specified column.
#
def separate_by_third_column_dict(data, column_name):
    zero_list = []
    one_list = []

    for row in data:
        row_copy = {key: value for key, value in row.items() if key != column_name}  # Remove the specified column
        if row[column_name] == '0':
            zero_list.append(row_copy)
        elif row[column_name] == '1':
            one_list.append(row_copy)

    return zero_list, one_list

#
# Loads model files for all 5 hand types
#
def load_models(strategy, decks):
    hard_double, soft_double = separate_by_third_column_dict(read_csv_to_dict("./models/" + decks + "-" + strategy + "-double.csv"), 'soft')
    hard_stand, soft_stand = separate_by_third_column_dict(read_csv_to_dict("./models/" + decks + "-" + strategy + "-stand.csv"), 'soft')
    pair_split = read_csv_to_dict("./models/" + decks + "-" + strategy + "-split.csv")
    return hard_double, soft_double, hard_stand, soft_stand, pair_split

