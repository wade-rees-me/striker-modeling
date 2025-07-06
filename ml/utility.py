import os
import json
import csv
import pandas as pd
import constant


#
# Load a JSON file from disk and return its contents.
#
def load_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


#
# Reads a CSV file and returns a list of dictionaries, one per row.
#
def read_csv_to_dict(filename):
    print(f"Reading: {filename}")
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)


#
# Splits a list of dictionaries into two lists based on the value of a specified column.
# If column_name value is "0", row goes to hard_list; if "1", to soft_list.
#
def separate_by_third_column_dict(data, column_name):
    hard_list = []
    soft_list = []

    for row in data:
        # Exclude the split key from the returned row
        row_copy = {key: value for key, value in row.items() if key != column_name}
        if row[column_name] == "0":
            hard_list.append(row_copy)
        elif row[column_name] == "1":
            soft_list.append(row_copy)

    return hard_list, soft_list


#
# Load training data from CSV files for all 5 hand types (double, stand, hit, split),
# split into soft and hard variants when applicable.
#
def load_models(strategy, decks):
    base_path = os.path.join(constant.resources_url, "data")
    base_file = os.path.join(base_path, f"{decks}-{strategy}")

    hard_double, soft_double = separate_by_third_column_dict(read_csv_to_dict(f"{base_file}-double.csv"), column_name="soft")
    hard_stand, soft_stand = separate_by_third_column_dict(read_csv_to_dict(f"{base_file}-stand.csv"), column_name="soft")
    hard_hit, soft_hit = separate_by_third_column_dict(read_csv_to_dict(f"{base_file}-hit.csv"), column_name="soft")
    pair_split = read_csv_to_dict(f"{base_file}-split.csv")

    return {
        "hard_double": hard_double,
        "soft_double": soft_double,
        "pair_split": pair_split,
        "soft_stand": soft_stand,
        "hard_stand": hard_stand,
        "soft_hit": soft_hit,
        "hard_hit": hard_hit,
    }
