import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tensorflow.keras.models import load_model

# Project modules
import neural
import model
import utility
import constant

# Titles for different types of strategy visuals
TITLE_SOFT_DOUBLE = "Player should double with soft %s vs dealer up card"
TITLE_HARD_DOUBLE = "Player should double with hard %s vs dealer up card"
TITLE_PAIR_SPLIT = "Player should split a pair of %s vs dealer up card"
TITLE_SOFT_STAND = "Player should stand with soft %s vs dealer up card"
TITLE_HARD_STAND = "Player should stand with hard %s vs dealer up card"


#
# Build all diagrams for the given deck type
#
def build_diagrams(decks, label):
    print(f"  Building diagrams ({decks})...")

    charts_path = os.path.join(constant.resources_url, "charts/")
    basic_chart = utility.load_json_file(f"{charts_path}{decks}-ev.json")

    build_double(12, 21, decks, label + TITLE_SOFT_DOUBLE, "double-soft", "double-soft-", basic_chart["soft-double"], 1, "soft", "Soft Double")
    build_double(4, 21, decks, label + TITLE_HARD_DOUBLE, "double-hard", "double-hard-", basic_chart["hard-double"], 1, "hard", "Hard Double")
    build_split(2, 12, decks, label + TITLE_PAIR_SPLIT, "split-pair", "split-pair-", basic_chart["pair-split"], 2, "hard")
    build_double(12, 21, decks, label + TITLE_SOFT_STAND, "stand-soft", "stand-soft-", basic_chart["soft-stand"], 3, "soft", "Soft Stand")
    build_double(4, 21, decks, label + TITLE_HARD_STAND, "stand-hard", "stand-hard-", basic_chart["hard-stand"], 3, "hard", "Hard Stand")


#
# Build diagrams for strategies that depend on total (double/stand)
#
def build_double(beg, end, decks, title, hand, option, basic, playX, optionX, label):
    models_path = os.path.join(constant.resources_url, "models", decks)
    for total in range(beg, end):
        print(f"{label}: {total}")
        model_linear = utility.load_json_file(f"{models_path}/linear-{option}{total}.json")
        model_polynomial = utility.load_json_file(f"{models_path}/polynomial-{option}{total}.json")
        model_neural = load_model(f"{models_path}/neural-{option}{total}-tf.keras")

        build_strategy_images(decks, title, hand, str(total), model_linear, model_polynomial, basic[str(total)], model_neural, playX, optionX, total, 0)


#
# Build diagrams for pair splitting strategy
#
def build_split(beg, end, decks, title, hand, option, basic, playX, optionX):
    models_path = os.path.join(constant.resources_url, "models", decks)
    for pair in range(beg, end):
        print(f"Pair Split: {pair}")
        model_linear = utility.load_json_file(f"{models_path}/linear-pair-split-{constant.pairs[pair]}.json")
        model_polynomial = utility.load_json_file(f"{models_path}/polynomial-pair-split-{constant.pairs[pair]}.json")
        model_neural = load_model(f"{models_path}/neural-pair-split-{constant.pairs[pair]}-tf.keras")

        build_strategy_images(
            decks, title, hand, constant.cards[pair], model_linear, model_polynomial, basic[constant.pairs[pair]], model_neural, playX, optionX, 0, pair
        )


#
# Render and save diagram for one strategy curve
#
def build_strategy_images(decks, title, hand, total, model_linear, model_polynomial, basic, model_neural, play, option, totalX, pairX):
    diagrams_path = os.path.join(constant.resources_url, "diagrams", decks)
    os.makedirs(diagrams_path, exist_ok=True)

    full_title = title % total
    fig = build_base(-3.5, 3.5, 0.5, full_title)

    add_basic(fig, basic, constant.COLOR_ORANGE)
    add_model(fig, model_linear, constant.COLOR_RED, "Linear")
    add_model(fig, model_polynomial, constant.COLOR_GREEN, "Polynomial")
    add_model_neural(fig, model_neural, constant.COLOR_BLUE, "Neural Network", total, play, option, totalX, pairX)

    add_legend(fig)
    output_path = os.path.join(diagrams_path, f"{hand}-{total}.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()


#
# Initialize the diagram canvas
#
def build_base(y_min, y_max, y_step, title):
    y_array = np.arange(y_min, y_max + y_step, y_step)

    plt.close("all")
    fig = plt.figure(figsize=(12.00, 6.00))
    ax = fig.add_axes([0.06, 0.10, 0.92, 0.84])

    ax.set_ylim(y_min, y_max)
    ax.set_xticks(list(range(2, 12)))
    ax.set_yticks(y_array)
    ax.set_xticklabels(["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "ace"])

    plt.xlabel("Dealer up card", fontsize=16)
    plt.ylabel("Expected value in units", fontsize=16)
    plt.title(title, fontsize=18)

    for i in range(2, 12):
        plt.axvline(i, color="lightgrey")
    plt.axhline(0, color="black", linewidth=1.0)

    return fig


#
# Plot model (linear or polynomial) prediction curve
#
def add_model(fig, model, color, label):
    x_values = list(range(2, 12))
    y_values = model["predictions"]
    metrics = model["metrics"]
    mse = f"{metrics['mean_squared_error']:.3f}"
    r2 = f"{metrics['r2_score']:.3f}"
    plt.plot(x_values, y_values, color=color, label=f"{label} Regression: MSE = {mse}, R2 = {r2}")


#
# Plot neural network prediction curve
#
def add_model_neural(fig, model, color, label, total, play, option, totalX, pairX):
    x_values = list(range(2, 12))
    y_values = []

    for up in x_values:
        y_df = get_prediction(up, model)
        y_normalized = neural.reverse_normalize_nested_values(y_df, constant.MINIMUM_WIN, constant.MAXIMUM_WIN)
        print(f"neural: {y_df} / {y_normalized}")
        y_values.append(y_normalized[0])

    plt.plot(x_values, y_values, color=color, label=f"{label} Regression")


#
# Add legend with deduplicated labels
#
def add_legend(fig):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Remove duplicate labels
    plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=9)


#
# Plot the basic approximation line
#
def add_basic(fig, basic, color):
    x = list(range(2, 12))
    y = [float(value) * 2.0 for value in basic]
    plt.plot(x, y, label="Approximation of Expected Values", color=color, linestyle="--")


#
# Normalize dealer card and make prediction using the model
#
def get_prediction(up, model):
    new_data = {"up": np.array([float(up)])}
    data_df = pd.DataFrame(new_data)
    data_df = neural.normalize_column(data_df, "up", constant.MINIMUM_CARD, constant.MAXIMUM_CARD)
    return model.predict(data_df.values.reshape(1, -1))
