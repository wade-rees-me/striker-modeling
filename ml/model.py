import linear
import polynomial
import neural
import utility
import constant


#
#
#
def build_models(strategy, decks):
    models_path = constant.resources_url + "/models/"

    print("  Building model files (" + strategy + " " + decks + ")...")

    data_file = utility.load_models(strategy, decks)
    # basic_chart = utility.load_json_file("./charts/" + decks + "-basic.json")

    # play,soft,total,pair,up,win / soft,total,pair,up,win
    for hard_total in range(4, 22):
        print("    Hard Total: ", hard_total)

        new_data_double = [row for row in data_file["hard_double"] if row.get("total") == str(hard_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-double-hard-" + str(hard_total) + ".json",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-double-hard-" + str(hard_total) + ".json",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-double-hard-" + str(hard_total) + "-tf.keras",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

        new_data_stand = [row for row in data_file["hard_stand"] if row.get("total") == str(hard_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-stand-hard-" + str(hard_total) + ".json",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-stand-hard-" + str(hard_total) + ".json",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-stand-hard-" + str(hard_total) + "-tf.keras",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

        new_data_hit = [row for row in data_file["hard_hit"] if row.get("total") == str(hard_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-hit-hard-" + str(hard_total) + ".json",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-hit-hard-" + str(hard_total) + ".json",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-hit-hard-" + str(hard_total) + "-tf.keras",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

    #
    for soft_total in range(12, 22):
        print("    Soft Total: ", soft_total)

        new_data_double = [row for row in data_file["soft_double"] if row.get("total") == str(soft_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-double-soft-" + str(soft_total) + ".json",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-double-soft-" + str(soft_total) + ".json",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-double-soft-" + str(soft_total) + "-tf.keras",
            new_data_double,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

        new_data_stand = [row for row in data_file["soft_stand"] if row.get("total") == str(soft_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-stand-soft-" + str(soft_total) + ".json",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-stand-soft-" + str(soft_total) + ".json",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-stand-soft-" + str(soft_total) + "-tf.keras",
            new_data_stand,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

        new_data_hit = [row for row in data_file["soft_hit"] if row.get("total") == str(soft_total)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-hit-soft-" + str(soft_total) + ".json",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-hit-soft-" + str(soft_total) + ".json",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-hit-soft-" + str(soft_total) + "-tf.keras",
            new_data_hit,
            constant.y_column,
            ["play", "win", "total", "pair"],
        )

    #
    for pair in range(2, 12):
        print("    Pairs: ", pair)
        new_data_split = [row for row in data_file["pair_split"] if row.get("pair") == str(pair)]
        linear.train_linear_regression_save(
            models_path + decks + "/linear-pair-split-" + constant.pairs[pair] + ".json",
            new_data_split,
            constant.y_column,
            ["play", "win", "total", "soft", "pair"],
        )
        polynomial.train_polynomial_regression_save(
            models_path + decks + "/polynomial-pair-split-" + constant.pairs[pair] + ".json",
            new_data_split,
            constant.y_column,
            ["play", "win", "total", "soft", "pair"],
            degree=4,
        )
        neural.train_neural_save2(
            models_path + decks + "/neural-pair-split-" + constant.pairs[pair] + "-tf.keras",
            new_data_split,
            constant.y_column,
            ["play", "win", "total", "soft", "pair"],
        )
