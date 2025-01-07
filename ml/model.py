#!/usr/local/bin/python3

import linear
import polynomial
import neural
import utility
import constant

#
#
#
def build_models(strategy, decks):
    print("  Building model files (" + strategy + " " + decks + ")...")

    #neural.train_neural_save("./data/" + decks + "-basic.csv", "./models/" + decks + "/neural-" + decks + "-tf-model.keras")

    data_file = utility.load_models(strategy, decks)
    basic_chart = utility.load_json_file("./charts/" + decks + "-basic.json")

    # play,soft,total,pair,up,win / soft,total,pair,up,win
    for hard_total in range(4, 22):
        print("    Hard Total: ", hard_total)

        new_data_double = [row for row in data_file["hard_double"] if row.get('total') == str(hard_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-double-hard-" + str(hard_total) + ".json", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-double-hard-" + str(hard_total) + ".json", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-double-hard-" + str(hard_total) + "-tf.keras", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'])

        new_data_stand = [row for row in data_file["hard_stand"] if row.get('total') == str(hard_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-stand-hard-" + str(hard_total) + ".json", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-hard-" + str(hard_total) + ".json", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-stand-hard-" + str(hard_total) + "-tf.keras", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'])

        new_data_hit = [row for row in data_file["hard_hit"] if row.get('total') == str(hard_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-hit-hard-" + str(hard_total) + ".json", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-hard-" + str(hard_total) + ".json", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-hit-hard-" + str(hard_total) + "-tf.keras", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'])

    #
    for soft_total in range(12, 22):
        print("    Soft Total: ", soft_total)

        new_data_double = [row for row in data_file["soft_double"] if row.get('total') == str(soft_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-double-soft-" + str(soft_total) + ".json", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-double-soft-" + str(soft_total) + ".json", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-double-soft-" + str(soft_total) + "-tf.keras", new_data_double, constant.y_column, ['play', 'win', 'total', 'pair'])

        new_data_stand = [row for row in data_file["soft_stand"] if row.get('total') == str(soft_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-stand-soft-" + str(soft_total) + ".json", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-soft-" + str(soft_total) + ".json", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-stand-soft-" + str(soft_total) + "-tf.keras", new_data_stand, constant.y_column, ['play', 'win', 'total', 'pair'])

        new_data_hit = [row for row in data_file["soft_hit"] if row.get('total') == str(soft_total)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-hit-soft-" + str(soft_total) + ".json", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-soft-" + str(soft_total) + ".json", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-hit-soft-" + str(soft_total) + "-tf.keras", new_data_hit, constant.y_column, ['play', 'win', 'total', 'pair'])

    #
    for pair in range(2, 12):
        print("    Pairs: ", pair)
        new_data_split = [row for row in data_file["pair_split"] if row.get('pair') == str(pair)]
        linear.train_linear_regression_save("./models/" + decks + "/linear-pair-split-" + constant.pairs[pair] + ".json", new_data_split, constant.y_column, ['play', 'win', 'total', 'soft', 'pair'])
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-pair-split-" + constant.pairs[pair] + ".json", new_data_split, constant.y_column, ['play', 'win', 'total', 'soft', 'pair'], degree=4)
        neural.train_neural_save2("./models/" + decks + "/neural-pair-split-" + constant.pairs[pair] + "-tf.keras", new_data_split, constant.y_column, ['play', 'win', 'total', 'soft', 'pair'])

