#!/usr/local/bin/python3

import pandas as pd
import numpy as np

import os
import neural
import model
import utility
import constant

from tensorflow.keras.models import Sequential, load_model

#
#
#
def build_charts(strategy, decks):
    print("  Building chart files (" + strategy + " " + decks + ")...")

    f1 = open_chart(decks, strategy)
    build_charts_double(f1, 12, 22, strategy, decks, "soft")
    build_charts_double(f1, 4, 22, strategy, decks, "hard")

    f1.write('  "pair-split":{\n')
    for pair in range(2, 12):
        f1.write('    "' + ("%s" % constant.pairs[pair]) + '": [ ')
        build_charts_pair_split_row(f1, strategy, decks, pair)
        f1.write(' ]')
        if pair != 11:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

    build_charts_stand(f1, 12, 22, strategy, decks, "soft")
    build_charts_stand(f1, 4, 22, strategy, decks, "hard")
    close_chart(f1)

#
#
#
def build_charts_double(f1, beg, end, strategy, decks, option):
    f1.write('  "' + option + '-double":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_double_row(f1, decks, strategy, total, option)
        f1.write(' ]')
        if total != 21:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

#
#
#
def build_charts_stand(f1, beg, end, strategy, decks, option):
    f1.write('  "' + option + '-stand":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_stand_row(f1, decks, strategy, total, option)
        f1.write(' ]')
        if total != 21:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

#
#
#
def build_charts_double_row(f1, decks, strategy, total, option):
    model_double = utility.load_json_file("./models/" + decks + "/" + strategy + "-double-" + option + "-" + str(total) + ".json")
    model_stand = utility.load_json_file("./models/" + decks + "/" + strategy + "-stand-" + option + "-" + str(total) + ".json")
    model_hit = utility.load_json_file("./models/" + decks + "/" + strategy + "-hit-" + option + "-" + str(total) + ".json")
    if total == 12:
        model_split = utility.load_json_file("./models/" + decks + "/" + strategy + "-pair-split-" + "A" + ".json")
    else:
        model_split = None

    for up in range(2, 12):
        predict_double = model_double['predictions'][up - 2]
        predict_split = -99.0
        predict_stand = model_stand['predictions'][up - 2]
        predict_hit = model_hit['predictions'][up - 2]
        if model_split != None:
            predict_split = model_split['predictions'][up - 2]
        f1.write('"%s"' % ('Y' if (predict_double >= predict_split and predict_double >= predict_stand and predict_double >= predict_hit) else 'N'))
        if up != 11:
            f1.write(', ')

#
#
#
def build_charts_pair_split_row(f1, strategy, decks, pair):
    total = (pair + 2) * 2
    if pair > 8:
        total = 20
    model_split = utility.load_json_file("./models/" + decks + "/" + strategy + "-pair-split-" + constant.pairs[pair] + ".json")
    if pair == 12: # aces
        model_stand = utility.load_json_file("./models/" + decks + "/" + strategy + "-stand-soft-" + str(12) + ".json")
        model_hit = utility.load_json_file("./models/" + decks + "/" + strategy + "-hit-soft-" + str(12) + ".json")
    else:
        model_stand = utility.load_json_file("./models/" + decks + "/" + strategy + "-stand-hard-" + str(total) + ".json")
        model_hit = utility.load_json_file("./models/" + decks + "/" + strategy + "-hit-hard-" + str(total) + ".json")

    for up in range(2, 12):
        predict_split = model_split['predictions'][up - 2]
        predict_stand = model_stand['predictions'][up - 2]
        predict_hit = model_hit['predictions'][up - 2]
        f1.write('"%s"' % ('Y' if (predict_split >= predict_stand and predict_split >= predict_hit) else 'N'))
        if up != 11:
            f1.write(', ')

#
#
#
def build_charts_stand_row(f1, decks, strategy, total, option):
    model_stand = utility.load_json_file("./models/" + decks + "/" + strategy + "-stand-" + option + "-" + str(total) + ".json")
    model_hit = utility.load_json_file("./models/" + decks + "/" + strategy + "-hit-" + option + "-" + str(total) + ".json")

    for up in range(2, 12):
        predict_stand = model_stand['predictions'][up - 2]
        predict_hit = model_hit['predictions'][up - 2]
        f1.write('"%s"' % ('Y' if (predict_stand >= predict_hit) else 'N'))
        if up != 11:
            f1.write(', ')

#
#
#
def open_chart(decks, strategy):
    file = open("charts/" + decks + "-" + strategy + ".json", "w")
    file.write('{\n')
    file.write('  "playbook": "' + decks + '-' + strategy + '",\n')
    file.write('  "counts": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],\n')
    return file

#
#
#
def close_chart(file):
    file.write('  "insurance": "N"\n')
    file.write('}\n')
    file.close()

