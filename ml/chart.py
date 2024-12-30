#!/usr/local/bin/python3

import pandas as pd
import numpy as np

import os
import dnn
import model
import utility
import constant

from tensorflow.keras.models import load_model

#
#
#
def build_charts(strategy, decks):
    print("  Building chart files (" + strategy + " " + decks + ")...")

    f1 = open_chart(decks, strategy)
    build_charts_double(f1, 12, 22, strategy, decks, "soft")
    build_charts_double(f1, 4, 22, strategy, decks, "hard")

    f1.write('  "pair-split":{\n')
    for pair in range(0, 13):
        f1.write('    "' + ("%s" % constant.pairs[pair]) + '": [ ')
        build_charts_pair_split_row(f1, strategy, decks, pair)
        f1.write(' ]')
        if pair != 12:
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

    for up in range(0, 13):
        predict_double = model_double['predictions'][up]
        predict_split = -99.0
        predict_stand = model_stand['predictions'][up]
        predict_hit = model_hit['predictions'][up]
        if model_split != None:
            predict_split = model_split['predictions'][up]
        f1.write('"%s"' % ('Y' if (predict_double >= predict_split and predict_double >= predict_stand and predict_double >= predict_hit) else 'N'))
        if up != 12:
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

    for up in range(0, 13):
        predict_split = model_split['predictions'][up]
        predict_stand = model_stand['predictions'][up]
        predict_hit = model_hit['predictions'][up]
        f1.write('"%s"' % ('Y' if (predict_split >= predict_stand and predict_split >= predict_hit) else 'N'))
        if up != 12:
            f1.write(', ')

#
#
#
def build_charts_stand_row(f1, decks, strategy, total, option):
    model_stand = utility.load_json_file("./models/" + decks + "/" + strategy + "-stand-" + option + "-" + str(total) + ".json")
    model_hit = utility.load_json_file("./models/" + decks + "/" + strategy + "-hit-" + option + "-" + str(total) + ".json")

    for up in range(0, 13):
        predict_stand = model_stand['predictions'][up]
        predict_hit = model_hit['predictions'][up]
        f1.write('"%s"' % ('Y' if (predict_stand >= predict_hit) else 'N'))
        if up != 12:
            f1.write(', ')

#
#
#
def build_charts_neural(strategy, decks):
    print("  Building chart files (" + strategy + " " + decks + ")...")

    model = load_model("./models/" + decks + "/dnn-" + decks + "-tf-model.keras")

    f1 = open_chart(decks, strategy)
    build_charts_double_neural(f1, 12, 22, strategy, decks, 'soft', model)
    build_charts_double_neural(f1, 4, 22, strategy, decks, 'hard', model)

    f1.write('  "pair-split":{\n')
    for pair in range(0, 13):
        f1.write('    "' + ("%s" % constant.pairs[pair]) + '": [ ')
        build_charts_pair_split_row_neural(f1, strategy, decks, pair, model)
        f1.write(' ]')
        if pair != 12:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

    build_charts_stand_neural(f1, 12, 22, strategy, decks, 'soft', model)
    build_charts_stand_neural(f1, 4, 22, strategy, decks, 'hard', model)
    close_chart(f1)

#
#
#
def build_charts_double_neural(f1, beg, end, strategy, decks, option, model):
    f1.write('  "' + option + '-double":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_double_row_neural(f1, decks, strategy, total, option, model)
        f1.write(' ]')
        if total != 21:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

#
#
#
def build_charts_stand_neural(f1, beg, end, strategy, decks, option, model):
    f1.write('  "' + option + '-stand":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_stand_row_neural(f1, total, option, model)
        f1.write(' ]')
        if total != 21:
            f1.write(',')
        f1.write("\n")
    f1.write('  },\n')

#
#
#
def build_charts_double_row_neural(f1, decks, strategy, total, option, model):
    for up in range(0, 13):
        predict_double = get_prediction(1, total, option, up, model)
        predict_split = -99.0
        predict_stand = get_prediction(3, total, option, up, model)
        predict_hit = get_prediction(4, total, option, up, model)
        if total == 12:
            predict_split = get_prediction(2, total, 'soft', up, model)
        f1.write('"%s"' % ('Y' if (predict_double >= predict_split and predict_double >= predict_stand and predict_double >= predict_hit) else 'N'))
        if up != 12:
            f1.write(', ')

#
#
#
def build_charts_pair_split_row_neural(f1, strategy, decks, pair, model):
    total = (pair + 2) * 2
    if pair > 8:
        total = 20
    for up in range(0, 13):
        if pair == 12: # aces
            predict_stand = get_prediction(3, 12, 'soft', up, model)
            predict_hit = get_prediction(4, 12, 'soft', up, model)
        else:
            predict_stand = get_prediction(3, total, 'hard', up, model)
            predict_hit = get_prediction(4, total, 'hard', up, model)
        predict_split = get_prediction(2, pair, 'hard', up, model)
        f1.write('"%s"' % ('Y' if (predict_split >= predict_stand and predict_split >= predict_hit) else 'N'))
        if up != 12:
            f1.write(', ')

#
#
#
def build_charts_stand_row_neural(f1, total, option, model):
    for up in range(0, 13):
        predict_stand = get_prediction(3, total, option, up, model)
        predict_hit = get_prediction(4, total, option, up, model)
        f1.write('"%s"' % ('Y' if (predict_stand >= predict_hit) else 'N'))
        if up != 12:
            f1.write(', ')

#
#
#
def get_prediction(play, total, option, up, model):
    new_data = {
        'play': np.array([float(play)]),
        'total': np.array([float(total)]),
        'soft': np.array([float(1.0 if option == 'soft' else 0.0)]),
        'up': np.array([float(up)])
    }
    data_df = pd.DataFrame(new_data)
    data_df = dnn.normalize_data_frame(data_df)
    data_df = data_df.values.reshape(1, -1)
    return model.predict(data_df)

#
#
#
def open_chart(decks, strategy):
    file = open("charts/" + decks + "-" + strategy + ".json", "w")
    file.write('{\n')
    file.write('  "playbook": "' + decks + '-' + strategy + '",\n')
    file.write('  "counts": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],\n')
    file.write('  "bets": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],\n')
    return file

#
#
#
def close_chart(file):
    file.write('  "insurance": "N"\n')
    file.write('}\n')
    file.close()

