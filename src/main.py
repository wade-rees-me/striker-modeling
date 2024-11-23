#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import requests
import json
import csv
import strikerImage as image
import strikerModel as model
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

striker_home = "/Users/waderees/github.com/wade-rees-me/striker/"
bucket_name = 'rees-me-striker'
cards = ['twos', 'threes', 'fours', 'fives', 'sixes', 'sevens', 'eights', 'nines', 'tens', 'jacks', 'queens', 'kings', 'aces']

#
#    Trains a linear regression model on the provided data dictionary.
#    
#    Parameters:
#    data_dict (dict): Dictionary containing the data. Keys are column names.
#    y_column (str): The name of the target column.
#
#    Returns:
#    model (LinearRegression): The trained linear regression model.
#    metrics (dict): Dictionary containing model performance metrics.
#
def train_linear_regression(data_dict, y_column):
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data_dict)
    
    # Separate features (X) and target (y)
    X = df.drop(columns=[y_column, 'total'])
    y = df[y_column]

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the linear regression model
    model = LinearRegression()
    #print(X_train, y_train)
    model.fit(X_train, y_train)
    
    # Make predictions and calculate metrics
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'mean_squared_error': mse,
        'r2_score': r2
    }
    
    return model, metrics

#
#
#
def train_polynomial_regression(data_dict, y_column, degree=4):
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data_dict)

    # Separate features (X) and target (y)
    X = df.drop(columns=[y_column, 'total'])
    y = df[y_column]

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transform the features for polynomial regression
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Initialize and train the linear regression model on polynomial features
    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    # Make predictions and calculate metrics
    y_pred = model.predict(X_test_poly)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    metrics = {
        'mean_squared_error': mse,
        'r2_score': r2
    }

    return model, poly, metrics  # Return the PolynomialFeatures transformer as well

#
#
#
def build_strategy_table_linear(f1, strategy, hand, model, total, basic, last):
    #build_linear_strategy(f1, "hard-double", linear_model_hard_double, 4, 22, "Y", "N")
    f1.write('\t\t"' + ("%s" % str(total)) + '" : [ "')
    for up in [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]:
        new_data = {
            'up': [up]
        }
        new_data_df = pd.DataFrame(new_data)
        if up > 2:
            f1.write(',\t\t"')
        prediction = model.predict(new_data_df)
        if prediction >= 0.0:
            f1.write(("%s" % "Y") + '"')
        else:
            f1.write(("%s" % "N") + '"')
    f1.write(' ]')
    if not last:
        f1.write(',')
    f1.write("\n")

#
#
#
def build_strategy_table_polynomial(f2, strategy, hand, model, polynomial, total, basic, last):
    #build_linear_strategy(f2, "hard-double", linear_model_hard_double, 4, 22, "Y", "N")
    f2.write('\t\t"' + ("%s" % str(total)) + '" : [ "')
    for up in [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]:
        new_data = {
            'up': [up]
        }
        new_data_df = pd.DataFrame(new_data)
        new_data_polynomial = polynomial.transform(new_data_df)
        if up > 2:
            f2.write(',\t\t"')
        prediction = model.predict(new_data_polynomial)
        if prediction >= 0.0:
            f2.write(("%s" % "Y") + '"')
        else:
            f2.write(("%s" % "N") + '"')
    f2.write(' ]')
    if not last:
        f2.write(',')
    f2.write("\n")

#
#
#
def build_strategy_images(strategy, decks, play, hand, linear_model, linear_metrics, polynomial_model, polynomial, polynomial_metrics, total, basic, split, card):
    if split:
        title = "Player should split with a pair of %s vs dealer up card" % card
    else:
        title = "Player should %s with %s %d vs dealer up card" % (play, hand, total)
    fig = image.build_base(-2.0, 2.0, 0.5, title, total)
    image.add_basic(fig, basic)
    image.add_linear(fig, linear_model, linear_metrics, total)
    image.add_polynomial(fig, polynomial_model, polynomial, polynomial_metrics, total)
    image.add_legend(fig)
    plt.savefig("./diagrams/" + decks + "/" + strategy + "-" + str(total) + ".png", bbox_inches='tight')
    plt.close()

#
#
#
def process_strategy(f1, f2, strategy, decks, x, hand, label, beg, end, data, basic, split):
    y_column = 'win'

    print("    Build model (" + strategy + " " + decks + " " + hand + ")...")
    f1.write('\t"' + x + '": {\n')
    f2.write('\t"' + x + '": {\n')

    for total in range(beg, end):
        new_data = model.filter_csv_by_total(data, total)
        if split:
            card = cards[total]
            print("      pair: ", cards[total])
        else:
            card = ''
            print("      total: ", total)
        linear_model, linear_metrics = train_linear_regression(new_data, y_column)
        polynomial_model, polynomial, polynomial_metrics = train_polynomial_regression(new_data, y_column)
        if split:
            build_strategy_images(x, decks, label, hand, linear_model, linear_metrics, polynomial_model, polynomial, polynomial_metrics, total + 2, basic[str(total + 2)], split, card)
            build_strategy_table_linear(f1, strategy, hand, linear_model, total + 2, basic, total == end - 1)
            build_strategy_table_polynomial(f2, strategy, hand, polynomial_model, polynomial, total + 2, basic, total == end - 1)
        else:
            build_strategy_images(x, decks, label, hand, linear_model, linear_metrics, polynomial_model, polynomial, polynomial_metrics, total, basic[str(total)], split, card)
            build_strategy_table_linear(f1, strategy, hand, linear_model, total, basic, total == end - 1)
            build_strategy_table_polynomial(f2, strategy, hand, polynomial_model, polynomial, total, basic, total == end - 1)

    f1.write('\t},\n')
    f2.write('\t},\n')

#
#
#
def process_strategies(strategy, decks):
    print("  Load model file (" + strategy + " " + decks + ")...")

    basic = model.load_json_file("./charts/" + decks + "-basic.json")
    hard_double, soft_double, hard_stand, soft_stand, pair_split = model.load_models(strategy, decks)

    f1 = open("charts/" + decks + "-linear.json", "w")
    f2 = open("charts/" + decks + "-polynomial.json", "w")

    f1.write('{\n')
    f2.write('{\n')
    f1.write('\t"playbook": "' + decks + '-linear",\n')
    f2.write('\t"playbook": "' + decks + '-polynomial",\n')
    f1.write('\t"counts": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],\n')
    f2.write('\t"counts": [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],\n')
    f1.write('\t"bets": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],\n')
    f2.write('\t"bets": [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],\n')

    process_strategy(f1, f2, strategy, decks, "soft-double", "soft", "double down", 12, 22, soft_double, basic["soft-double"], False)
    process_strategy(f1, f2, strategy, decks, "hard-double", "hard", "double down", 4, 22, hard_double, basic["hard-double"], False)
    process_strategy(f1, f2, strategy, decks, "pair-split", "pair of", "split", 0, 13, pair_split, basic["pair-split"], True)
    process_strategy(f1, f2, strategy, decks, "soft-stand", "soft", "stand", 12, 22, soft_stand, basic["soft-stand"], False)
    process_strategy(f1, f2, strategy, decks, "hard-stand", "hard", "stand", 4, 22, hard_stand, basic["hard-stand"], False)

    f1.write('\t"insurance": "N"\n')
    f2.write('\t"insurance": "N"\n')
    f1.write('}\n')
    f2.write('}\n')

    f1.close()
    f2.close()

#
#
#
if __name__ == "__main__":
    print("Starting...")
    process_strategies('basic', 'single-deck')
    process_strategies('basic', 'double-deck')
    process_strategies('basic', 'six-shoe')
    print("Ending...\n")

