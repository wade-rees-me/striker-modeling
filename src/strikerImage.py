#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import requests
import strikerImage as image
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

#
#
def build_base(y_min, y_max, y_step, title, total):
    y_array = np.arange(y_min, y_max + y_step, y_step)
    x1 = np.arange(2, 14).reshape(-1, 1)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1]

    plt.close('all')
    fig = plt.figure(figsize=(12.00, 6.00))

    ax = fig.add_axes([0.06, 0.10, 0.92, 0.84])  # [left, bottom, width, height]
    ax.set_ylim(y_min, y_max)
    ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    ax.set_yticks(y_array)
    ax.set_xticklabels(['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace'])
    plt.xlabel("Dealer up card", fontsize = 16)
    plt.ylabel("Expected value in units", fontsize = 16)
    plt.title(title, fontsize = 18)

    for i in range(0, 13):
        plt.axvline(i, color='lightgrey')
    plt.axhline(0, color='black', linewidth=1.0)

    return fig

#
#
def add_basic(fig, basic):
    #print(basic)
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    y = [-1 if value == 'N' else 1 for value in basic]
    plt.plot(x, y, marker='x', label='Basic strategy', color='#FF99FF', linestyle="--",markersize=10) 

#
#
def add_linear(fig, model, metrics, total):
    new_data = {
        'up': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
    new_data_df = pd.DataFrame(new_data)
    y_predict = model.predict(new_data_df)
    mse = f"{metrics['mean_squared_error']:.3f}"
    r2 = f"{metrics['r2_score']:.3f}"
    plt.plot(new_data_df, y_predict, color='green', label='Linear Regression: MSE = ' + mse + ', R2 = ' + r2)

#
#
def add_polynomial(fig, model, polynomial, metrics, total):
    new_data = {
        #'total': [total] * 13,
        'up': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    }
    new_data_df = pd.DataFrame(new_data)
    new_data_polynomial = polynomial.transform(new_data_df)
    mse = f"{metrics['mean_squared_error']:.3f}"
    r2 = f"{metrics['r2_score']:.3f}"
    plt.plot(new_data_df, model.predict(new_data_polynomial), color='red', label='Polynomial Regression: MSE = ' + mse + ', R2 = ' + r2)

#
#
def add_legend(fig):
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc="upper left", fontsize=12)

