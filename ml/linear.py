import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


#
# Train a linear regression model and save coefficients, metrics, and predictions to a JSON file.
#
def train_linear_regression_save(file_name, data_dict, y_column, drop_columns):
    # Convert input dictionary to DataFrame
    df = pd.DataFrame(data_dict)

    # Separate target variable and features
    y = df[y_column]
    X = df.drop(columns=drop_columns)

    # Split the dataset: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    metrics = {"mean_squared_error": mse, "r2_score": r2}

    # Prepare model data to save
    model_data = {"coefficients": model.coef_.tolist(), "intercept": model.intercept_, "metrics": metrics}

    # Generate predictions for dealer upcards 2 through 11
    predictions = []
    for up in range(2, 12):
        input_df = pd.DataFrame({"up": [up]})
        prediction = model.predict(input_df)
        predictions.append(prediction[0])

    # Add predictions to model data and save to file
    model_data["predictions"] = predictions

    with open(file_name, "w") as f:
        json.dump(model_data, f, indent=4)
