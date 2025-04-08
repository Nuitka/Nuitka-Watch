# nuitka-project: --mode=standalone
# nuitka-project: --enable-plugin=no-qt

# Relevant debugging option: --experimental=debug-self-forking

import os, sys

if "NUITKA_LAUNCH_TOKEN" not in os.environ:
    sys.exit("Error, need launch token or else fork bomb suspected.")
else:
    del os.environ["NUITKA_LAUNCH_TOKEN"]

# isort:start

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.svm import SVC

# load the dataset and split it into training and testing sets
dataset = load_breast_cancer()
X = dataset.data
Y = dataset.target
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.30, random_state=101
)
# train the model on train set without using GridSearchCV
model = SVC()
model.fit(X_train, y_train)

# print prediction results
predictions = model.predict(X_test)
print("REPORT1:")
print(classification_report(y_test, predictions))

# defining parameter range
param_grid = {
    "C": [0.1, 1, 10, 100],
    "gamma": [1, 0.1, 0.01, 0.001, 0.0001],
    "gamma": ["scale", "auto"],
    "kernel": ["linear"],
}

grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=1, n_jobs=2)

# fitting the model for grid search
grid.fit(X_train, y_train)

# print best parameter after tuning
print("PARAMS:")
print(grid.best_params_)
grid_predictions = grid.predict(X_test)

# print classification report
print("REPORT2:")
print(classification_report(y_test, grid_predictions))
