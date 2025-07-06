import json
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score


#
# Train a polynomial regression model and save coefficients, metrics, and predictions to a JSON file.
#
def train_polynomial_regression_save(file_name, data_dict, y_column, drop_columns, degree=4):
    # Convert the input dictionary to a DataFrame
    df = pd.DataFrame(data_dict)

    # Separate features and target
    y = df[y_column]
    X = df.drop(columns=drop_columns)

    # Split into training and testing sets (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Transform features to polynomial of specified degree
    poly = PolynomialFeatures(degree=degree)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Fit linear regression on transformed features
    model = LinearRegression()
    model.fit(X_train_poly, y_train)

    # Predict and evaluate
    y_pred = model.predict(X_test_poly)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    metrics = {"mean_squared_error": mse, "r2_score": r2}

    # Save model coefficients and metrics
    model_data = {"coefficients": model.coef_.tolist(), "intercept": model.intercept_, "metrics": metrics}

    # Predict for upcard values 2–11 and store
    predictions = []
    for up in range(2, 12):
        input_df = pd.DataFrame({"up": [up]})
        input_poly = poly.transform(input_df)
        prediction = model.predict(input_poly)
        predictions.append(prediction[0])

    model_data["predictions"] = predictions

    # Write model data to JSON file
    with open(file_name, "w") as f:
        json.dump(model_data, f, indent=4)
