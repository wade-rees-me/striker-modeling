#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import model

TITLE_SOFT_DOUBLE = "Player should double with soft %d vs dealer up card"
TITLE_HARD_DOUBLE = "Player should double with hard %d vs dealer up card"
TITLE_PAIR_SPLIT = "Player should split a pair of %s vs dealer up card"
TITLE_SOFT_STAND = "Player should stand with soft %d vs dealer up card"
TITLE_HARD_STAND = "Player should stand with hard %d vs dealer up card"

#
#
#
def build_diagrams(decks):
    print("  Building diagrams (" + decks + ")...")

    build_double(12, 22, decks, TITLE_SOFT_DOUBLE, "soft-double", "double-soft-")
    build_double( 4, 22, decks, TITLE_HARD_DOUBLE, "hard-double", "double-hard-")
    build_split( 0, 13, decks, TITLE_PAIR_SPLIT, "pair-split")
    build_double(12, 22, decks, TITLE_SOFT_STAND, "soft-stand", "stand-soft-")
    build_double( 4, 22, decks, TITLE_HARD_STAND, "hard-stand", "stand-hard-")

#
#
#
def build_double(beg, end, decks, title, hand, option):
    path = "./models/" + decks + "/"
    for total in range(beg, end):
        model_linear = model.load_json_file(path + "linear-" + option + str(total) + ".json")
        model_polynomial = model.load_json_file(path + "polynomial-" + option + str(total) + ".json")
        build_strategy_images(decks, title, hand, total, model_linear, model_polynomial)

#
#
#
def build_split(beg, end, decks, title, hand):
    path = "./models/" + decks + "/"
    for pair in range(beg, end):
        model_linear = model.load_json_file(path + "linear-pair-split-" + model.pairs[pair] + ".json")
        model_polynomial = model.load_json_file(path + "polynomial-pair-split-" + model.pairs[pair] + ".json")
        build_strategy_images(decks, title, hand, pair, model_linear, model_polynomial)

#
#
#
def build_strategy_images(decks, title, hand, total, model_linear, model_polynomial):
    full_title = title % (total)
    fig = build_base(-2.0, 2.0, 0.5, full_title, total)
    add_model(fig, model_linear, total, 'green', 'Linear')
    add_model(fig, model_polynomial, total, 'red', 'Polynomial')
    add_legend(fig)
    plt.savefig("./diagrams/" + decks + "/" + hand + "-" + str(total) + ".png", bbox_inches='tight')
    plt.close()

#
#
def build_base(y_min, y_max, y_step, title, total):
    y_array = np.arange(y_min, y_max + y_step, y_step)
    x1 = np.arange(2, 14).reshape(-1, 1)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]

    plt.close('all')
    fig = plt.figure(figsize=(12.00, 6.00))

    ax = fig.add_axes([0.06, 0.10, 0.92, 0.84])  # [left, bottom, width, height]
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    ax.set_yticks(y_array)
    ax.set_xticklabels(['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace'])
    plt.xlabel("Dealer up card", fontsize = 16)
    plt.ylabel("Expected value in units", fontsize = 16)
    plt.title(title, fontsize = 18)

    for i in range(0, 13):
        plt.axvline(i, color='lightgrey')
    plt.axhline(0, color='black', linewidth=1.0)

    return fig

#
#
def add_model(fig, model, total, color, label):
    new_data = {
        'up': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
    new_data_df = pd.DataFrame(new_data)
    y_predict = model['predictions']
    metrics = model['metrics']
    mse = f"{metrics['mean_squared_error']:.3f}"
    r2 = f"{metrics['r2_score']:.3f}"
    #plt.plot(new_data_df, y_predict, color='green', label='Linear Regression: MSE = ' + mse + ', R2 = ' + r2)
    plt.plot(new_data_df, y_predict, color=color, label=label + ' Regression: MSE = ' + mse + ', R2 = ' + r2)

#
#
def add_legend(fig):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=12)

