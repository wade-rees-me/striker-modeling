import os

# Base path for resources, set via environment variable STRIKER_RESOURCES
resources_url = os.getenv("STRIKER_RESOURCES")

# Strategy types
BASIC = "basic"
LINEAR = "linear"
POLYNOMIAL = "polynomial"
NEURAL = "neural"

# Deck configurations
SINGLE_DECK = "single-deck"
DOUBLE_DECK = "double-deck"
SIX_SHOE = "six-shoe"

# Play actions (used as indexes or identifiers)
PLAY_DOUBLE = 0
PLAY_SPLIT = 1
PLAY_STAND = 2
PLAY_HIT = 3

# Total hand value ranges
MINIMUM_TOTAL = 0
MAXIMUM_TOTAL = 21

# Soft hand range (usually Ace + something)
MINIMUM_SOFT = 0
MAXIMUM_SOFT = 2

# Card value range (2–11 where 11 = Ace)
MINIMUM_CARD = 0
MAXIMUM_CARD = 11

# Normalized win/loss value range for predictions
MINIMUM_WIN = -8
MAXIMUM_WIN = 8

# Standard color hex values for plotting or UI
COLOR_BLUE = "#1f77b4"
COLOR_RED = "#e84a5f"
COLOR_GREEN = "#2ca02c"
COLOR_ORANGE = "#ff7f0e"

# Card labels for charts/predictions: index 2–11 used
cards = [
    "",
    "",  # index 0, 1 unused
    "twos",  # 2
    "threes",  # 3
    "fours",  # 4
    "fives",  # 5
    "sixes",  # 6
    "sevens",  # 7
    "eights",  # 8
    "nines",  # 9
    "tens",  # 10
    "aces",  # 11
]

# Pair labels (e.g., "2", "3", ..., "X" for 10s, "A" for Aces)
pairs = ["", "", "2", "3", "4", "5", "6", "7", "8", "9", "X", "A"]  # index 0, 1 unused  # 10s  # Aces

# Target column in prediction/training datasets
y_column = "win"
