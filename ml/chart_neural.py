import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

# Project imports
import neural
import model
import chart
import utility
import constant


#
# Build full set of neural-based strategy charts for the given strategy and deck type.
#
def build_charts_neural(strategy, decks):
    print(f"  Building chart files ({strategy} {decks})...")

    f1 = chart.open_chart(decks, strategy)

    # Double strategy for soft and hard totals
    build_charts_double_neural(f1, 12, 22, decks, "soft")
    build_charts_double_neural(f1, 4, 22, decks, "hard")

    # Pair splitting section
    f1.write('  "pair-split":{\n')
    for pair in range(2, 12):
        f1.write(f'    "{constant.pairs[pair]}": [ ')
        build_charts_pair_split_row_neural(f1, decks, pair)
        f1.write(" ]")
        if pair != 11:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")

    # Stand strategy for soft and hard totals
    build_charts_stand_neural(f1, 12, 22, decks, "soft")
    build_charts_stand_neural(f1, 4, 22, decks, "hard")

    chart.close_chart(f1)


#
# Write "double" decisions for each total and upcard using neural network predictions
#
def build_charts_double_neural(f1, beg, end, decks, option):
    f1.write(f'  "{option}-double":{{\n')
    for total in range(beg, end):
        f1.write(f'    "{total}": [ ')
        build_charts_double_row_neural(f1, decks, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
# Write "stand" decisions for each total and upcard using neural predictions
#
def build_charts_stand_neural(f1, beg, end, decks, option):
    f1.write(f'  "{option}-stand":{{\n')
    for total in range(beg, end):
        f1.write(f'    "{total}": [ ')
        build_charts_stand_row_neural(f1, decks, total, option)
        f1.write(" ]")
        if total != 21:
            f1.write(",")
        f1.write("\n")
    f1.write("  },\n")


#
# Predict double, split, stand, hit outcomes and write "Y" if double is best option
#
def build_charts_double_row_neural(f1, decks, total, option):
    models_path = f"{constant.resources_url}/models/"
    model_double = load_model(f"{models_path}{decks}/neural-double-{option}-{total}-tf.keras")
    model_stand = load_model(f"{models_path}{decks}/neural-stand-{option}-{total}-tf.keras")
    model_hit = load_model(f"{models_path}{decks}/neural-hit-{option}-{total}-tf.keras")

    # Special case: soft 12 gets a pair-split model for Aces
    if option == "soft" and total == 12:
        model_split = load_model(f"{models_path}{decks}/neural-pair-split-{constant.pairs[11]}-tf.keras")
    else:
        model_split = None

    for up in range(2, 12):
        predict_double = get_prediction(model_double, up)
        predict_stand = get_prediction(model_stand, up)
        predict_hit = get_prediction(model_hit, up)
        predict_split = get_prediction(model_split, up) if model_split else float("-inf")

        print(f"Double: {total} vs {constant.cards[up]}")
        print(f"  double: {predict_double} > split: {predict_split} > stand: {predict_stand} > hit: {predict_hit}")

        is_best = predict_double >= max(predict_split, predict_stand, predict_hit)
        f1.write(f'"{"Y" if is_best else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Predict whether pair splitting is better than hit/stand
#
def build_charts_pair_split_row_neural(f1, decks, pair):
    models_path = f"{constant.resources_url}/models/"
    model_split = load_model(f"{models_path}{decks}/neural-pair-split-{constant.pairs[pair]}-tf.keras")
    total = pair * 2

    for up in range(2, 12):
        if pair == 11:  # Special case for Aces
            model_stand = load_model(f"{models_path}{decks}/neural-stand-soft-12-tf.keras")
            model_hit = load_model(f"{models_path}{decks}/neural-hit-soft-12-tf.keras")
        else:
            model_stand = load_model(f"{models_path}{decks}/neural-stand-hard-{total}-tf.keras")
            model_hit = load_model(f"{models_path}{decks}/neural-hit-hard-{total}-tf.keras")

        predict_stand = get_prediction(model_stand, up)
        predict_hit = get_prediction(model_hit, up)
        predict_split = get_prediction(model_split, up)

        print(f"Split: {constant.cards[pair]} vs {constant.cards[up]}")
        print(f"  split: {predict_split} > stand: {predict_stand} > hit: {predict_hit}")

        is_best = predict_split >= max(predict_stand, predict_hit)
        f1.write(f'"{"Y" if is_best else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Predict whether standing is better than hitting
#
def build_charts_stand_row_neural(f1, decks, total, option):
    models_path = f"{constant.resources_url}/models/"
    model_stand = load_model(f"{models_path}{decks}/neural-stand-{option}-{total}-tf.keras")
    model_hit = load_model(f"{models_path}{decks}/neural-hit-{option}-{total}-tf.keras")

    for up in range(2, 12):
        predict_stand = get_prediction(model_stand, up)
        predict_hit = get_prediction(model_hit, up)

        print(f"stand: {option} :{total} vs {up} == {predict_stand} > {predict_hit}  " f"{'stand' if predict_stand >= predict_hit else 'hit'}")

        f1.write(f'"{"Y" if predict_stand >= predict_hit else "N"}"')
        if up != 11:
            f1.write(", ")


#
# Get a normalized prediction from the neural network and reverse-scale it
#
def get_prediction(model, up):
    # Prepare input data as a normalized DataFrame
    new_data = {"up": np.array([float(up)])}
    data_df = pd.DataFrame(new_data)
    data_df = neural.normalize_column(data_df, "up", constant.MINIMUM_CARD, constant.MAXIMUM_CARD)
    data_df = data_df.values.reshape(1, -1)

    # Predict and reverse normalization
    y = model.predict(data_df)
    return neural.reverse_normalize_nested_values(y, constant.MINIMUM_WIN, constant.MAXIMUM_WIN)[0][0]
