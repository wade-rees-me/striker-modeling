#!/usr/local/bin/python3

import pandas as pd
import numpy as np

import os
import neural
import model
import chart
import utility
import constant

from tensorflow.keras.models import Sequential, load_model


#
#
#
def build_charts_neural(strategy, decks):
    print("  Building chart files (" + strategy + " " + decks + ")...")

    f1 = chart.open_chart(decks, strategy)
    build_charts_double_neural(f1, 12, 22, decks, "soft")
    build_charts_double_neural(f1, 4, 22, decks, "hard")

    f1.write('  "pair-split":{\n')
    for pair in range(2, 12):
        f1.write('    "' + ("%s" % constant.pairs[pair]) + '": [ ')
        build_charts_pair_split_row_neural(f1, decks, pair)
        f1.write(" ]")
        if pair != 11:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")

    build_charts_stand_neural(f1, 12, 22, decks, "soft")
    build_charts_stand_neural(f1, 4, 22, decks, "hard")
    chart.close_chart(f1)


#
#
#
def build_charts_double_neural(f1, beg, end, decks, option):
    f1.write('  "' + option + '-double":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_double_row_neural(f1, decks, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
#
#
def build_charts_stand_neural(f1, beg, end, decks, option):
    f1.write('  "' + option + '-stand":{\n')
    for total in range(beg, end):
        f1.write('    "' + ("%s" % str(total)) + '": [ ')
        build_charts_stand_row_neural(f1, decks, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
#
#
def build_charts_double_row_neural(f1, decks, total, option):
    models_path = constant.resources_url + "/models/"
    model_double = load_model(models_path + decks + "/neural-double-" + option + "-" + str(total) + "-tf.keras")
    model_stand = load_model(models_path + decks + "/neural-stand-" + option + "-" + str(total) + "-tf.keras")
    model_hit = load_model(models_path + decks + "/neural-hit-" + option + "-" + str(total) + "-tf.keras")
    if option == "soft" and total == 12:
        model_split = load_model(models_path + decks + "/neural-pair-split-" + constant.pairs[11] + "-tf.keras")
    else:
        model_split = None

    for up in range(2, 12):
        predict_double = get_prediction(model_double, up)
        predict_split = float(-99.0)
        predict_stand = get_prediction(model_stand, up)
        predict_hit = get_prediction(model_hit, up)
        if model_split != None:
            predict_split = get_prediction(model_split, up)
        print("Double: " + str(total) + " vs " + constant.cards[up])
        print(
            "  double: "
            + str(predict_double)
            + " > "
            + "split: "
            + str(predict_split)
            + " > "
            + "stand: "
            + str(predict_stand)
            + " > "
            + "hit: "
            + str(predict_hit)
        )
        f1.write('"%s"' % ("Y" if (predict_double >= predict_split and predict_double >= predict_stand and predict_double >= predict_hit) else "N"))
        if up != 11:
            f1.write(", ")


#
#
#
def build_charts_pair_split_row_neural(f1, decks, pair):
    models_path = constant.resources_url + "/models/"
    model_split = load_model(models_path + decks + "/neural-pair-split-" + constant.pairs[pair] + "-tf.keras")

    total = pair * 2
    for up in range(2, 12):
        if pair == 11:  # aces
            model_stand = load_model(models_path + decks + "/neural-stand-soft-" + str(12) + "-tf.keras")
            model_hit = load_model(models_path + decks + "/neural-hit-soft-" + str(12) + "-tf.keras")
            predict_stand = get_prediction(model_stand, up)
            predict_hit = get_prediction(model_hit, up)
        else:
            model_stand = load_model(models_path + decks + "/neural-stand-hard-" + str(total) + "-tf.keras")
            model_hit = load_model(models_path + decks + "/neural-hit-hard-" + str(total) + "-tf.keras")
            predict_stand = get_prediction(model_stand, up)
            predict_hit = get_prediction(model_hit, up)
        predict_split = get_prediction(model_split, up)
        print("Split: " + constant.cards[pair] + " vs " + constant.cards[up])
        print("  split: " + str(predict_split) + " > " + "stand: " + str(predict_stand) + " > " + "hit: " + str(predict_hit))
        f1.write('"%s"' % ("Y" if (predict_split >= predict_stand and predict_split >= predict_hit) else "N"))
        if up != 11:
            f1.write(", ")


#
#
#
def build_charts_stand_row_neural(f1, decks, total, option):
    models_path = constant.resources_url + "/models/"
    model_stand = load_model(models_path + decks + "/neural-stand-" + option + "-" + str(total) + "-tf.keras")
    model_hit = load_model(models_path + decks + "/neural-hit-" + option + "-" + str(total) + "-tf.keras")
    for up in range(2, 12):
        predict_stand = get_prediction(model_stand, up)
        predict_hit = get_prediction(model_hit, up)
        print(
            "stand: "
            + str(option)
            + " :"
            + str(total)
            + " vs "
            + str(up)
            + " == "
            + str(predict_stand)
            + " > "
            + str(predict_hit)
            + "  "
            + ("stand" if (predict_stand >= predict_hit) else "hit")
        )
        f1.write('"%s"' % ("Y" if (predict_stand >= predict_hit) else "N"))
        if up != 11:
            f1.write(", ")


#
#
#
def get_prediction(model, up):
    new_data = {"up": np.array([float(up)])}
    data_df = pd.DataFrame(new_data)
    data_df = neural.normalize_column(data_df, "up", min_value=constant.MINIMUM_CARD, max_value=constant.MAXIMUM_CARD)
    data_df = data_df.values.reshape(1, -1)
    y = model.predict(data_df)
    return neural.reverse_normalize_nested_values(y, constant.MINIMUM_WIN, constant.MAXIMUM_WIN)[0][0]
