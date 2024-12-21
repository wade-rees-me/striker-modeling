#!/usr/local/bin/python3

import pandas as pd
import json
import csv
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

pairs = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
y_column = 'win'

#
#
#
def train_linear_regression_save(file_name, data_dict, y_column):
    #print("Linear: ", data_dict[0])
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

    # Save the model and metrics to a JSON file
    model_data = {
        'coefficients': model.coef_.tolist(),
        'intercept': model.intercept_,
        'metrics': metrics
    }

    predictions = []
    for up in range(0, 13):
        new_data = {
            'up': [up]
        }
        new_data_df = pd.DataFrame(new_data)
        prediction_linear = model.predict(new_data_df)
        predictions.append(prediction_linear[0])

    additional_data = {
        'predictions': predictions
    }
    model_data.update(additional_data)

    with open(file_name, "w") as f:
        json.dump(model_data, f, indent=4)

    #return model, metrics

#
#
#
def train_polynomial_regression_save(file_name, data_dict, y_column, degree=4):
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

    #return model, poly, metrics  # Return the PolynomialFeatures transformer as well
    # Save the model and metrics to a JSON file
    model_data = {
        'coefficients': model.coef_.tolist(),
        'intercept': model.intercept_,
        'metrics': metrics
    }

    predictions = []
    for up in range(0, 13):
        new_data = {
            'up': [up]
        }
        new_data_df = pd.DataFrame(new_data)
        new_data_polynomial = poly.transform(new_data_df)
        prediction_linear = model.predict(new_data_polynomial)
        predictions.append(prediction_linear[0])

    additional_data = {
        'predictions': predictions
    }
    model_data.update(additional_data)

    with open(file_name, "w") as f:
        json.dump(model_data, f, indent=4)

#
#
#
def build_models(strategy, decks):
    print("  Building model files (" + strategy + " " + decks + ")...")

    data_file = load_models(strategy, decks)
    basic_chart = load_json_file("./charts/" + decks + "-basic.json")

    for hard_total in range(4, 22):
        #print("    Hard Total: ", hard_total)
        new_data_double = filter_csv_by_total(data_file["hard_double"], hard_total)
        train_linear_regression_save("./models/" + decks + "/linear-double-hard-" + str(hard_total) + ".json", new_data_double, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-double-hard-" + str(hard_total) + ".json", new_data_double, y_column, degree=4)

        new_data_stand = filter_csv_by_total(data_file["hard_stand"], hard_total)
        train_linear_regression_save("./models/" + decks + "/linear-stand-hard-" + str(hard_total) + ".json", new_data_stand, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-hard-" + str(hard_total) + ".json", new_data_stand, y_column, degree=4)

        new_data_hit = filter_csv_by_total(data_file["hard_hit"], hard_total)
        train_linear_regression_save("./models/" + decks + "/linear-hit-hard-" + str(hard_total) + ".json", new_data_hit, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-hard-" + str(hard_total) + ".json", new_data_hit, y_column, degree=4)

    for soft_total in range(12, 22):
        #print("    Soft Total: ", soft_total)
        new_data_double = filter_csv_by_total(data_file["soft_double"], soft_total)
        train_linear_regression_save("./models/" + decks + "/linear-double-soft-" + str(soft_total) + ".json", new_data_double, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-double-soft-" + str(soft_total) + ".json", new_data_double, y_column, degree=4)

        new_data_stand = filter_csv_by_total(data_file["soft_stand"], soft_total)
        train_linear_regression_save("./models/" + decks + "/linear-stand-soft-" + str(soft_total) + ".json", new_data_stand, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-stand-soft-" + str(soft_total) + ".json", new_data_stand, y_column, degree=4)

        new_data_hit = filter_csv_by_total(data_file["soft_hit"], soft_total)
        train_linear_regression_save("./models/" + decks + "/linear-hit-soft-" + str(soft_total) + ".json", new_data_hit, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-hit-soft-" + str(soft_total) + ".json", new_data_hit, y_column, degree=4)

    for pair in range(0, 13):
        #print("    Pairs: ", pair)
        new_data_split = filter_csv_by_total(data_file["pair_split"], pair)
        train_linear_regression_save("./models/" + decks + "/linear-pair-split-" + pairs[pair] + ".json", new_data_split, y_column)
        train_polynomial_regression_save("./models/" + decks + "/polynomial-pair-split-" + pairs[pair] + ".json", new_data_split, y_column, degree=4)

#
# Filter the list of dictionaries where "total" equals the specified value
#
def filter_csv_by_total(csv_list, total_value):
    #print("Filtered list for ", total_value)
    filtered_list = [row for row in csv_list if row.get("total") == str(total_value)]

    # Initialize counts dictionary
    counts = {str(up): {'4': 0, '3': 0, '2': 0, '0': 0, '-2': 0, '-3': 0, '-4': 0} for up in range(13)}

    # Count occurrences
    for entry in filtered_list:
        up = entry['up']
        win = entry['win']
        if up in counts and win in counts[up]:
            counts[up][win] += 1

    # Print the counts
    #for up, win_counts in counts.items():
    #    print(f"Up={up}: {win_counts}")

    return filtered_list

#
#
def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

#
#
# Reads a CSV file into a list of dictionaries.
#
def read_csv_to_dict(filename):
    print(filename)
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

#
# Separates rows into two lists based on the value of the specified column.
#
def separate_by_third_column_dict(data, column_name):
    hard_list = []
    soft_list = []

    for row in data:
        row_copy = {key: value for key, value in row.items() if key != column_name}  # Remove the specified column
        if row[column_name] == '0':
            hard_list.append(row_copy)
        elif row[column_name] == '1':
            soft_list.append(row_copy)

    return hard_list, soft_list

#
# Loads model files for all 5 hand types
#
def load_models(strategy, decks):
    hard_double, soft_double = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-double.csv"), 'soft')
    hard_stand, soft_stand = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-stand.csv"), 'soft')
    hard_hit, soft_hit = separate_by_third_column_dict(read_csv_to_dict("./data/" + decks + "-" + strategy + "-hit.csv"), 'soft')
    pair_split = read_csv_to_dict("./data/" + decks + "-" + strategy + "-split.csv")
    data_files = {
        'hard_double': hard_double,
        'soft_double': soft_double,
        'pair_split': pair_split,
        'soft_stand': soft_stand,
        'hard_stand': hard_stand,
        'soft_hit': soft_hit,
        'hard_hit': hard_hit
    }
    return data_files

