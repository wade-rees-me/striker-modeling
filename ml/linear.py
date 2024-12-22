#!/usr/local/bin/python3

import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

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

