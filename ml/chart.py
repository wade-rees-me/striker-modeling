import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential, load_model

# Project imports
import neural
import model
import utility
import constant


#
# Build a complete strategy chart using stored model predictions (non-neural)
#
def build_charts(strategy, decks):
    print(f"  Building chart files ({strategy} {decks})...")

    f1 = open_chart(decks, strategy)

    # Double strategy decisions (soft/hard hands)
    build_charts_double(f1, 12, 22, strategy, decks, "soft")
    build_charts_double(f1, 4, 22, strategy, decks, "hard")

    # Pair splitting decisions
    f1.write('  "pair-split":{\n')
    for pair in range(2, 12):
        f1.write(f'    "{constant.pairs[pair]}": [ ')
        build_charts_pair_split_row(f1, strategy, decks, pair)
        f1.write(" ]")
        if pair != 11:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")

    # Stand decisions (soft/hard hands)
    build_charts_stand(f1, 12, 22, strategy, decks, "soft")
    build_charts_stand(f1, 4, 22, strategy, decks, "hard")

    close_chart(f1)


#
# Write full "double" decision table to file
#
def build_charts_double(f1, beg, end, strategy, decks, option):
    f1.write(f'  "{option}-double":{{\n')
    for total in range(beg, end):
        f1.write(f'    "{total}": [ ')
        build_charts_double_row(f1, decks, strategy, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
# Write full "stand" decision table to file
#
def build_charts_stand(f1, beg, end, strategy, decks, option):
    f1.write(f'  "{option}-stand":{{\n')
    for total in range(beg, end):
        f1.write(f'    "{total}": [ ')
        build_charts_stand_row(f1, decks, strategy, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
# Write a single row of double decisions for one total
#
def build_charts_double_row(f1, decks, strategy, total, option):
    models_path = f"{constant.resources_url}/models/"
    model_double = utility.load_json_file(f"{models_path}{decks}/{strategy}-double-{option}-{total}.json")
    model_stand = utility.load_json_file(f"{models_path}{decks}/{strategy}-stand-{option}-{total}.json")
    model_hit = utility.load_json_file(f"{models_path}{decks}/{strategy}-hit-{option}-{total}.json")

    model_split = None
    if total == 12:
        model_split = utility.load_json_file(f"{models_path}{decks}/{strategy}-pair-split-A.json")

    for up in range(2, 12):
        predict_double = model_double["predictions"][up - 2]
        predict_stand = model_stand["predictions"][up - 2]
        predict_hit = model_hit["predictions"][up - 2]
        predict_split = model_split["predictions"][up - 2] if model_split else -99.0

        best = predict_double >= max(predict_stand, predict_hit, predict_split)
        f1.write(f'"{"Y" if best else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Write a single row of pair-split decisions
#
def build_charts_pair_split_row(f1, strategy, decks, pair):
    models_path = f"{constant.resources_url}/models/"
    model_split = utility.load_json_file(f"{models_path}{decks}/{strategy}-pair-split-{constant.pairs[pair]}.json")

    total = (pair + 2) * 2
    if pair > 8:
        total = 20

    if pair == 12:  # Aces (treated as soft 12)
        model_stand = utility.load_json_file(f"{models_path}{decks}/{strategy}-stand-soft-12.json")
        model_hit = utility.load_json_file(f"{models_path}{decks}/{strategy}-hit-soft-12.json")
    else:
        model_stand = utility.load_json_file(f"{models_path}{decks}/{strategy}-stand-hard-{total}.json")
        model_hit = utility.load_json_file(f"{models_path}{decks}/{strategy}-hit-hard-{total}.json")

    for up in range(2, 12):
        predict_split = model_split["predictions"][up - 2]
        predict_stand = model_stand["predictions"][up - 2]
        predict_hit = model_hit["predictions"][up - 2]

        best = predict_split >= max(predict_stand, predict_hit)
        f1.write(f'"{"Y" if best else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Write a single row of stand/hit decisions
#
def build_charts_stand_row(f1, decks, strategy, total, option):
    models_path = f"{constant.resources_url}/models/"
    model_stand = utility.load_json_file(f"{models_path}{decks}/{strategy}-stand-{option}-{total}.json")
    model_hit = utility.load_json_file(f"{models_path}{decks}/{strategy}-hit-{option}-{total}.json")

    for up in range(2, 12):
        predict_stand = model_stand["predictions"][up - 2]
        predict_hit = model_hit["predictions"][up - 2]

        best = predict_stand >= predict_hit
        f1.write(f'"{"Y" if best else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Open a new JSON file for writing the chart
#
def open_chart(decks, strategy):
    charts_path = f"{constant.resources_url}/charts/"
    os.makedirs(charts_path, exist_ok=True)
    file = open(f"{charts_path}{decks}-{strategy}.json", "w")
    file.write("{\n")
    file.write(f'  "playbook": "{decks}-{strategy}",\n')
    file.write('  "counts": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],\n')
    return file


#
# Close the chart file, writing a default insurance entry
#
def close_chart(file):
    file.write('  "insurance": "N"\n')
    file.write("}\n")
    file.close()
