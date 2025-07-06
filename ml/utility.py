#!/usr/local/bin/python3

import pandas as pd
import json
import csv
import constant


#
#
def load_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


#
#
# Reads a CSV file into a list of dictionaries.
#
def read_csv_to_dict(filename):
    print(filename)
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)


#
# Separates rows into two lists based on the value of the specified column.
#
def separate_by_third_column_dict(data, column_name):
    hard_list = []
    soft_list = []

    for row in data:
        row_copy = {key: value for key, value in row.items() if key != column_name}  # Remove the specified column
        if row[column_name] == "0":
            hard_list.append(row_copy)
        elif row[column_name] == "1":
            soft_list.append(row_copy)

    return hard_list, soft_list


#
# Loads model files for all 5 hand types
#
def load_models(strategy, decks):
    data_path = constant.resources_url + "/data/" + decks + "-" + strategy
    hard_double, soft_double = separate_by_third_column_dict(read_csv_to_dict(data_path + "-double.csv"), "soft")
    hard_stand, soft_stand = separate_by_third_column_dict(read_csv_to_dict(data_path + "-stand.csv"), "soft")
    hard_hit, soft_hit = separate_by_third_column_dict(read_csv_to_dict(data_path + "-hit.csv"), "soft")
    pair_split = read_csv_to_dict(data_path + "-split.csv")
    data_files = {
        "hard_double": hard_double,
        "soft_double": soft_double,
        "pair_split": pair_split,
        "soft_stand": soft_stand,
        "hard_stand": hard_stand,
        "soft_hit": soft_hit,
        "hard_hit": hard_hit,
    }
    return data_files
