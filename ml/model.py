#!/usr/local/bin/python3

import linear
import polynomial
import dnn
import utility
import constant

#
#
#
def build_models(strategy, decks):
    print("  Building model files (" + strategy + " " + decks + ")...")

    data_file = utility.load_models(strategy, decks)
    basic_chart = utility.load_json_file("./charts/" + decks + "-basic.json")

    dnn.train_dnn_save("./data/" + decks + "-basic.csv", "./models/" + decks + "/dnn-" + decks + "-tf-model.keras")

    for hard_total in range(4, 22):
        #print("    Hard Total: ", hard_total)
        new_data_double = utility.filter_csv_by_total(data_file["hard_double"], hard_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-double-hard-" + str(hard_total) + ".json", new_data_double, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-double-hard-" + str(hard_total) + ".json", new_data_double, constant.y_column, degree=4)

        new_data_stand = utility.filter_csv_by_total(data_file["hard_stand"], hard_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-stand-hard-" + str(hard_total) + ".json", new_data_stand, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-hard-" + str(hard_total) + ".json", new_data_stand, constant.y_column, degree=4)

        new_data_hit = utility.filter_csv_by_total(data_file["hard_hit"], hard_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-hit-hard-" + str(hard_total) + ".json", new_data_hit, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-hard-" + str(hard_total) + ".json", new_data_hit, constant.y_column, degree=4)

    for soft_total in range(12, 22):
        #print("    Soft Total: ", soft_total)
        new_data_double = utility.filter_csv_by_total(data_file["soft_double"], soft_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-double-soft-" + str(soft_total) + ".json", new_data_double, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-double-soft-" + str(soft_total) + ".json", new_data_double, constant.y_column, degree=4)

        new_data_stand = utility.filter_csv_by_total(data_file["soft_stand"], soft_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-stand-soft-" + str(soft_total) + ".json", new_data_stand, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-soft-" + str(soft_total) + ".json", new_data_stand, constant.y_column, degree=4)

        new_data_hit = utility.filter_csv_by_total(data_file["soft_hit"], soft_total)
        linear.train_linear_regression_save("./models/" + decks + "/linear-hit-soft-" + str(soft_total) + ".json", new_data_hit, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-soft-" + str(soft_total) + ".json", new_data_hit, constant.y_column, degree=4)

    for pair in range(0, 13):
        #print("    Pairs: ", pair)
        new_data_split = utility.filter_csv_by_total(data_file["pair_split"], pair)
        linear.train_linear_regression_save("./models/" + decks + "/linear-pair-split-" + constant.pairs[pair] + ".json", new_data_split, constant.y_column)
        polynomial.train_polynomial_regression_save("./models/" + decks + "/polynomial-pair-split-" + constant.pairs[pair] + ".json", new_data_split, constant.y_column, degree=4)

