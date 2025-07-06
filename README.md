# Striker Modeling

**Striker Modeling** is a Python-based simulation and visualization tool for building Blackjack strategy charts and diagrams using machine learning models.

It supports linear regression, polynomial regression, and neural network models to analyze optimal decisions for blackjack hands across multiple deck types and strategies.

---

## 📂 Project Structure

```plaintext
ml/
├── arguments.py         # CLI argument parser
├── chart.py             # Generates strategy charts from regression models
├── chart_neural.py      # Generates strategy charts from trained neural networks
├── constant.py          # Constants for strategies, deck types, card values, etc.
├── diagram.py           # Builds visual diagrams comparing model predictions
├── linear.py            # Linear regression training and export
├── polynomial.py        # Polynomial regression training and export
├── utility.py           # Data loading, preprocessing, file I/O helpers
├── main.py              # Main entry point for chart and diagram generation
```

---

## 🚀 Features

- Generate strategy charts (double, stand, split) based on model predictions
- Train and export linear and polynomial regression models to JSON
- Load and apply neural networks for soft/hard hands and pairs
- Build side-by-side visual diagrams comparing all three model types
- Supports single deck, double deck, and six-deck ("shoe") configurations
- Output format: JSON charts and PNG diagrams

---

## 🖥️ Requirements

- Python 3.7+
- TensorFlow 2.x
- scikit-learn
- pandas
- matplotlib
- numpy

Install requirements using:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup

Set the following environment variable to specify the root path for all data, model, chart, and diagram files:

```bash
export STRIKER_RESOURCES=/absolute/path/to/resources
```

The directory should contain:

```plaintext
resources/
├── data/         # CSV input files
├── models/       # Trained models in JSON and .keras format
├── charts/       # Output JSON strategy charts
├── diagrams/     # Output PNG images
```

---

## 🧠 Model Types

| Type        | Method                      | File Format          |
|-------------|-----------------------------|-----------------------|
| Linear      | `linear.py`                 | JSON                 |
| Polynomial  | `polynomial.py`             | JSON                 |
| Neural Net  | TensorFlow (`.keras`)       | Keras model + script |

---

## 🧾 Usage

### Generate Charts and Diagrams

```bash
python ml/main.py --model --chart --diagram
```

### Command-Line Options

| Option        | Description                              |
|---------------|------------------------------------------|
| `-M`, `--model`   | Train and save models                   |
| `-C`, `--chart`   | Build strategy charts (JSON)            |
| `-D`, `--diagram` | Build comparison diagrams (PNG)         |
| `--help`      | Show usage message                       |
| `--version`   | Display version info                     |

---

## 📊 Outputs

- **Charts**: JSON files for each deck/strategy combination.
  - Located in: `resources/charts/`
  - Example: `single-deck-linear.json`

- **Diagrams**: PNG visualizations for soft/hard totals and pair splits.
  - Located in: `resources/diagrams/`
  - Example: `double-soft-12.png`

---

## 📁 Data Inputs

CSV files are expected in this format:

| up | total | soft | win |
|----|-------|------|-----|
| 2  | 13    | 0    | 1.0 |

Where:
- `up`: Dealer's up card (2–11)
- `total`: Player's total
- `soft`: Whether it's a soft hand (`1`) or hard (`0`)
- `win`: Simulated EV (expected value)

---

## ✅ Example: Train Linear Model

```python
from ml.linear import train_linear_regression_save
from ml.utility import load_models

data = load_models("linear", "single-deck")["hard_double"]
train_linear_regression_save("models/single-deck/linear-double-hard-13.json", data, "win", ["soft"])
```

---

## 🔧 Developer Notes

- All model exports are readable and portable (JSON or Keras format)
- Neural predictions use normalized input/output values
- Visualization tools are built with Matplotlib for cross-platform compatibility

---

## 📝 License

MIT License (or specify your own)

---

## 🙋 Support

For bugs or feature requests, please open an issue or submit a pull request.

---
