#!/usr/local/bin/python3

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

import constant

LOSS = 'binary_crossentropy'
EPOCHS = 8
BATCH_SIZE = 32

#
#
#
def train_dnn_save(file_name, model_name):
    df = load_normalized_data_frame(file_name)
    build_dnn_save(df, model_name)

#
#
#
def load_normalized_data_frame(file_name):
    print("file:", file_name)
    data = pd.read_csv(file_name, dtype=float)
    df = pd.DataFrame(data)
    randomized_df = df.sample(frac=1).reset_index(drop=True)

    normalized_df = normalize_column(randomized_df, 'win', min_value=constant.MINIMUM_WIN, max_value=constant.MAXIMUM_WIN)
    normalized_df = normalize_column(normalized_df, 'play', min_value=constant.MINIMUM_PLAY, max_value=constant.MAXIMUM_PLAY)
    normalized_df = normalize_column(normalized_df, 'total', min_value=constant.MINIMUM_TOTAL, max_value=constant.MAXIMUM_TOTAL)
    normalized_df = normalize_column(normalized_df, 'up', min_value=constant.MINIMUM_UP, max_value=constant.MAXIMUM_UP)
    normalized_df = normalize_column(normalized_df, 'soft', min_value=constant.MINIMUM_SOFT, max_value=constant.MAXIMUM_SOFT)

    return normalized_df

#
#
#
def normalize_data_frame(df):
    df = normalize_column(df, 'play', min_value=constant.MINIMUM_PLAY, max_value=constant.MAXIMUM_PLAY)
    df = normalize_column(df, 'total', min_value=constant.MINIMUM_TOTAL, max_value=constant.MAXIMUM_TOTAL)
    df = normalize_column(df, 'up', min_value=constant.MINIMUM_UP, max_value=constant.MAXIMUM_UP)
    df = normalize_column(df, 'soft', min_value=constant.MINIMUM_SOFT, max_value=constant.MAXIMUM_SOFT)
    return df

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
    normalized_values = [
        (value - min_value) / (max_value - min_value) if max_value != min_value else 0
        for value in column_values
    ]

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

#
#
#
def build_dnn_save(df, model_name):
    X = df.drop(columns=["win"])
    y = df["win"]

    #
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    #
    model = Sequential()
    model.add(Input(shape={4,}))  # Shape based on number of features
    model.add(Dense(units=32, activation='relu'))
    model.add(Dense(units=64, activation='relu'))  # Optionally adding a second hidden layer
    model.add(Dense(units=1, activation='sigmoid'))  # Binary classification

    # Compile the model
    optimizer = Adam(learning_rate=0.001)  # Optional learning rate adjustment
    model.compile(optimizer=optimizer, loss=LOSS, metrics=['accuracy'])
    #model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

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

    #
    #accuracy = accuracy_score(y_test, y_hat)
    #print(f"Accuracy: {accuracy * 100}%")

    model.save(model_name)

