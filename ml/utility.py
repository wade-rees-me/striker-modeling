#!/usr/local/bin/python3

import pandas as pd
import json
import csv

#
# Filter the list of dictionaries where "total" equals the specified value
#
def filter_csv(csv_list, tag, value):
    print("Filtered list for " + tag + " = " + value)
    #filtered_list = [row for row in csv_list if row.get(tag) == str(total_value)]
    filtered_list = [row for row in csv_list if row == value]
    #print("Shape of filtered list:", filtered_list.shape)
    return filtered_list

#
# Filter the list of dictionaries where "total" equals the specified value
#
def filter_csv_by_total(csv_list, tag, total_value):
    #print("Filtered list for ", total_value)
    #filtered_list = [row for row in csv_list if row.get(tag) == str(total_value)]
    filtered_list = [row for row in csv_list if row == str(total_value)]

    ## Initialize counts dictionary
    #counts = {str(up): {'4': 0, '3': 0, '2': 0, '0': 0, '-2': 0, '-3': 0, '-4': 0} for up in range(13)}
#
#    # Count occurrences
#    for entry in filtered_list:
#        up = entry['up']
#        win = entry['win']
#        if up in counts and win in counts[up]:
#            counts[up][win] += 1
#
#    # Print the counts
#    #for up, win_counts in counts.items():
#    #    print(f"Up={up}: {win_counts}")

    #print("Shape of filtered list:", filtered_list.shape)
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
    hard_list = []
    soft_list = []

    for row in data:
        row_copy = {key: value for key, value in row.items() if key != column_name}  # Remove the specified column
        if row[column_name] == '0':
            hard_list.append(row_copy)
        elif row[column_name] == '1':
            soft_list.append(row_copy)

    return hard_list, soft_list

#
# Loads model files for all 5 hand types
#
def load_models(strategy, decks):
    hard_double, soft_double = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-double.csv"), 'soft')
    hard_stand, soft_stand = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-stand.csv"), 'soft')
    hard_hit, soft_hit = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-hit.csv"), 'soft')
    pair_split = read_csv_to_dict("./data/" + decks + "-" + strategy + "-split.csv")
    data_files = {
        'hard_double': hard_double,
        'soft_double': soft_double,
        'pair_split': pair_split,
        'soft_stand': soft_stand,
        'hard_stand': hard_stand,
        'soft_hit': soft_hit,
        'hard_hit': hard_hit
    }
    return data_files

