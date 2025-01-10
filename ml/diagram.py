#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import neural
import model
import utility
import constant

from tensorflow.keras.models import load_model

TITLE_SOFT_DOUBLE = "Player should double with soft %s vs dealer up card"
TITLE_HARD_DOUBLE = "Player should double with hard %s vs dealer up card"
TITLE_PAIR_SPLIT = "Player should split a pair of %s vs dealer up card"
TITLE_SOFT_STAND = "Player should stand with soft %s vs dealer up card"
TITLE_HARD_STAND = "Player should stand with hard %s vs dealer up card"

#
#
#
def build_diagrams(decks, label):
    print("  Building diagrams (" + decks + ")...")

    basic_chart = utility.load_json_file("./charts/" + decks + "-basic.json")

    build_double(12, 22, decks, label + TITLE_SOFT_DOUBLE, "double-soft", "double-soft-", basic_chart["soft-double"], model, 1, 'soft')
    build_double(4, 22, decks, label + TITLE_HARD_DOUBLE, "double-hard", "double-hard-", basic_chart["hard-double"], model, 1, 'hard')
    build_split(2, 12, decks, label + TITLE_PAIR_SPLIT, "split-pair", basic_chart["pair-split"], model, 2, 'hard')
    build_double(12, 22, decks, label + TITLE_SOFT_STAND, "stand-soft", "stand-soft-", basic_chart["soft-stand"], model, 3, 'soft')
    build_double(4, 22, decks, label + TITLE_HARD_STAND, "stand-hard", "stand-hard-", basic_chart["hard-stand"], model, 3, 'hard')

#
#
#
def build_double(beg, end, decks, title, hand, option, basic, model, playX, optionX):
    path = "./models/" + decks + "/"
    for total in range(beg, end):
        print("Double: " + str(total))
        model_linear = utility.load_json_file(path + "linear-" + option + str(total) + ".json")
        model_polynomial = utility.load_json_file(path + "polynomial-" + option + str(total) + ".json")
        model_neural = load_model(path + "/neural-double-" + optionX + "-" + str(total) + "-tf.keras")
        build_strategy_images(decks, title, hand, str(total), model_linear, model_polynomial, basic[str(total)], model_neural, playX, optionX, total, 0)

#
#
#
def build_split(beg, end, decks, title, hand, basic, model, play, option):
    path = "./models/" + decks + "/"
    print(basic)
    for pair in range(beg, end):
        print("Split: " + str(pair))
        model_linear = utility.load_json_file(path + "linear-pair-split-" + constant.pairs[pair] + ".json")
        model_polynomial = utility.load_json_file(path + "polynomial-pair-split-" + constant.pairs[pair] + ".json")
        model_neural = load_model(path + "/neural-pair-split-" + constant.pairs[pair] + "-tf.keras")
        build_strategy_images(decks, title, hand, constant.cards[pair], model_linear, model_polynomial, basic[constant.pairs[pair]], model_neural, play, option, 0, pair)

#
#
#
def build_strategy_images(decks, title, hand, total, model_linear, model_polynomial, basic, model_neural, play, option, totalX, pairX):
    full_title = title % (total)
    fig = build_base(-3.0, 3.0, 0.5, full_title)
    add_basic(fig, basic, constant.COLOR_ORANGE)
    add_model(fig, model_linear, constant.COLOR_RED, 'Linear')
    add_model(fig, model_polynomial, constant.COLOR_GREEN, 'Polynomial')
    add_model_neural(fig, model_neural, constant.COLOR_BLUE, 'Neural Network', total, play, option, totalX, pairX)
    add_legend(fig)
    plt.savefig("./diagrams/" + decks + "/" + hand + "-" + str(total) + ".png", bbox_inches='tight')
    plt.close()

#
#
def build_base(y_min, y_max, y_step, title):
    y_array = np.arange(y_min, y_max + y_step, y_step)

    plt.close('all')
    fig = plt.figure(figsize=(12.00, 6.00))

    ax = fig.add_axes([0.06, 0.10, 0.92, 0.84])  # [left, bottom, width, height]
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    ax.set_yticks(y_array)
    ax.set_xticklabels(['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'ace'])
    plt.xlabel("Dealer up card", fontsize = 16)
    plt.ylabel("Expected value in units", fontsize = 16)
    plt.title(title, fontsize = 18)

    for i in range(0, 13):
        plt.axvline(i, color='lightgrey')
    plt.axhline(0, color='black', linewidth=1.0)

    return fig

#
#
def add_model(fig, model, color, label):
    new_data = {
        'up': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    }
    print(new_data)
    new_data_df = pd.DataFrame(new_data)
    y_predict = model['predictions']
    metrics = model['metrics']
    mse = f"{metrics['mean_squared_error']:.3f}"
    r2 = f"{metrics['r2_score']:.3f}"
    #plt.plot(new_data_df, y_predict, color='green', label='Linear Regression: MSE = ' + mse + ', R2 = ' + r2)
    plt.plot(new_data_df, y_predict, color=color, label=label + ' Regression: MSE = ' + mse + ', R2 = ' + r2)

#
#
def add_model_neural(fig, model, color, label, total, play, option, totalX, pairX):
    new_data = {
        'up': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    }
    new_data_df = pd.DataFrame(new_data)
    y_predict = []

    for up in range(2, 12):
        #y_df = neural.get_prediction(up, model)
        y_df = get_prediction(up, model)
        y_normalized = neural.reverse_normalize_nested_values(y_df, constant.MINIMUM_WIN, constant.MAXIMUM_WIN)
        print("neural: " + str(y_df) + " / " + str(y_normalized))
        y_predict.append(y_normalized[0])

    #metrics = model['metrics']
    #mse = f"{metrics['mean_squared_error']:.3f}"
    #r2 = f"{metrics['r2_score']:.3f}"

    plt.plot(new_data_df, y_predict, color=color, label=label + ' Regression: MSE = ' + ', R2 = ')

#
#
def add_legend(fig):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=9)

#
#
def add_basic(fig, basic, color):
    print(basic)
    x = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    y = [-1 if value == 'N' else 1 for value in basic]
    plt.plot(x, y, marker='x', label='Basic strategy', color=color, linestyle="--", markersize=10) 

#
#
#
def get_prediction(up, model):
    new_data = {
        'up': np.array([float(up)])
    }
    data_df = pd.DataFrame(new_data)
    data_df = neural.normalize_column(data_df, 'up', min_value=constant.MINIMUM_CARD, max_value=constant.MAXIMUM_CARD)
    data_df = data_df.values.reshape(1, -1)
    return model.predict(data_df)

