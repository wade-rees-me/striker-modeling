#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import model

TITLE_SOFT_DOUBLE = "Player should double with soft %s vs dealer up card"
TITLE_HARD_DOUBLE = "Player should double with hard %s vs dealer up card"
TITLE_PAIR_SPLIT = "Player should split a pair of %s vs dealer up card"
TITLE_SOFT_STAND = "Player should stand with soft %s vs dealer up card"
TITLE_HARD_STAND = "Player should stand with hard %s vs dealer up card"

cards = ['twos', 'threes', 'fours', 'fives', 'sixes', 'sevens', 'eights', 'nines', 'tens', 'jacks', 'queens', 'kings', 'aces']

#
#
#
def build_diagrams(decks, label):
    print("  Building diagrams (" + decks + ")...")

    basic_chart = model.load_json_file("./charts/" + decks + "-basic.json")

    build_double(12, 22, decks, label + TITLE_SOFT_DOUBLE, "double-soft", "double-soft-", basic_chart["soft-double"])
    build_double(4, 22, decks, label + TITLE_HARD_DOUBLE, "double-hard", "double-hard-", basic_chart["hard-double"])
    build_split(0, 13, decks, label + TITLE_PAIR_SPLIT, "split-pair", basic_chart["pair-split"])
    build_double(12, 22, decks, label + TITLE_SOFT_STAND, "stand-soft", "stand-soft-", basic_chart["soft-stand"])
    build_double(4, 22, decks, label + TITLE_HARD_STAND, "stand-hard", "stand-hard-", basic_chart["hard-stand"])

#
#
#
def build_double(beg, end, decks, title, hand, option, basic):
    path = "./models/" + decks + "/"
    for total in range(beg, end):
        model_linear = model.load_json_file(path + "linear-" + option + str(total) + ".json")
        model_polynomial = model.load_json_file(path + "polynomial-" + option + str(total) + ".json")
        build_strategy_images(decks, title, hand, str(total), model_linear, model_polynomial, basic[str(total)])

#
#
#
def build_split(beg, end, decks, title, hand, basic):
    path = "./models/" + decks + "/"
    for pair in range(beg, end):
        model_linear = model.load_json_file(path + "linear-pair-split-" + model.pairs[pair] + ".json")
        model_polynomial = model.load_json_file(path + "polynomial-pair-split-" + model.pairs[pair] + ".json")
        build_strategy_images(decks, title, hand, cards[pair], model_linear, model_polynomial, basic[model.pairs[pair]])

#
#
#
def build_strategy_images(decks, title, hand, total, model_linear, model_polynomial, basic):
    full_title = title % (total)
    fig = build_base(-3.0, 3.0, 0.5, full_title)
    add_basic(fig, basic)
    add_model(fig, model_linear, 'green', 'Linear')
    add_model(fig, model_polynomial, 'red', 'Polynomial')
    add_legend(fig)
    plt.savefig("./diagrams/" + decks + "/" + hand + "-" + str(total) + ".png", bbox_inches='tight')
    plt.close()

#
#
def build_base(y_min, y_max, y_step, title):
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
def add_model(fig, model, color, label):
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

#
#
def add_basic(fig, basic):
    print(basic)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [-1 if value == 'N' else 1 for value in basic]
    plt.plot(x, y, marker='x', label='Basic strategy', color='#FF99FF', linestyle="--", markersize=10) 

