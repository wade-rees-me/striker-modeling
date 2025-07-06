import pandas as pd
import numpy as np
import json
import random

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

import utility
import constant

LOSS = "binary_crossentropy"
# LOSS = 'mse'
EPOCHS = 2
BATCH_SIZE = 32


#
# play, soft, total, pair, up, win
#
def train_neural_save2(file_name, data_dict, y_column, drop_columns):
    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data_dict)
    df_normalized = normalized_data_frame(df)

    # Separate features (X) and target (y)
    y = df_normalized["win"]
    X = df_normalized.drop(columns=drop_columns)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #
    model = Sequential()
    model.add(
        Input(
            shape={
                1,
            }
        )
    )  # Shape based on number of features
    model.add(Dense(units=32, activation="relu"))
    model.add(Dense(units=64, activation="relu"))  # Optionally adding a second hidden layer
    model.add(Dense(units=128, activation="relu"))  # Third hidden layer (newly added)
    model.add(Dense(units=1, activation="sigmoid"))  # Binary classification

    # Compile the model
    optimizer = Adam(learning_rate=0.001)  # Optional learning rate adjustment
    model.compile(optimizer=optimizer, loss=LOSS, metrics=["accuracy"])
    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=EPOCHS)
    model.summary()

    #
    y_hat = model.predict(X_test)

    #
    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(y_test, y_hat)
    print(f"Mean Squared Error: {mse}")

    # Calculate R-squared (R2) score
    r2 = r2_score(y_test, y_hat)
    print(f"R2 Score: {r2}")

    model.save(file_name)


#
#
#
def normalized_data_frame(data):
    data.fillna(0, inplace=True)

    data["total"] = pd.to_numeric(data["total"], errors="coerce")
    data["pair"] = pd.to_numeric(data["pair"], errors="coerce")
    data["up"] = pd.to_numeric(data["up"], errors="coerce")
    data["win"] = pd.to_numeric(data["win"], errors="coerce")

    df = pd.DataFrame(data)
    normalized_df = df.sample(frac=1).reset_index(drop=True)
    normalized_df = normalize_column(
        normalized_df,
        "total",
        min_value=constant.MINIMUM_TOTAL,
        max_value=constant.MAXIMUM_TOTAL,
    )
    normalized_df = normalize_column(
        normalized_df,
        "pair",
        min_value=constant.MINIMUM_CARD,
        max_value=constant.MAXIMUM_CARD,
    )
    normalized_df = normalize_column(
        normalized_df,
        "up",
        min_value=constant.MINIMUM_CARD,
        max_value=constant.MAXIMUM_CARD,
    )
    normalized_df = normalize_column(
        normalized_df,
        "win",
        min_value=constant.MINIMUM_WIN,
        max_value=constant.MAXIMUM_WIN,
    )

    return normalized_df


#
#
#
def normalize_column(data_dict, column_key, min_value, max_value):
    # Check if the column_key exists in the dictionary
    if column_key not in data_dict:
        raise KeyError(f"'{column_key}' not found in the dictionary.")

    # Extract the column values
    column_values = data_dict[column_key]

    # Normalize the values using the min-max formula
    normalized_values = [(value - min_value) / (max_value - min_value) if max_value != min_value else 0 for value in column_values]

    # Update the dictionary with normalized values
    data_dict[column_key] = normalized_values

    return data_dict


#
#
#
def reverse_normalize_nested_values(normalized_values, min_value, max_value):
    return [[reverse_normalize_value(value, min_value, max_value) for value in sublist] for sublist in normalized_values]


#
#
#
def reverse_normalize_value(normalized_value, min_value, max_value):
    return normalized_value * (max_value - min_value) + min_value
