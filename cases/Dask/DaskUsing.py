# nuitka-project: --mode=standalone
# nuitka-project: --noinclude-dask-mode=allow
# nuitka-project: --noinclude-numba-mode=allow

import random

import dask
import dask.array as da
import dask_ml.cluster
import dask_ml.datasets
import numpy as np
import pandas as pd
import xarray as xr
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

random.seed(0)

da.random.seed(0)
np.random.seed(0)

x = da.random.random((10000, 10000), chunks=(1000, 1000))
print(x)


y = x + x.T
z = y[::2, 5000:].mean(axis=1)
print(z)


data = np.random.rand(4, 3)

locs = ["IA", "IL", "IN"]

times = pd.date_range("2000-01-01", periods=4)

foo = xr.DataArray(data, coords=[times, locs], dims=["time", "space"])
print(foo)


df = dask.datasets.timeseries(seed=0)
print(df.head())


print(df.dtypes)


pd.options.display.precision = 2
pd.options.display.max_rows = 10


print(df.head(3))


df2 = df[df.y > 0]
df3 = df2.groupby("name").x.std()
print(df3)


computed_df = df3.compute()
if isinstance(computed_df, pd.Series) or isinstance(computed_df, pd.DataFrame):
    computed_df = computed_df.sort_index()
print(computed_df)


df4 = df.groupby("name").aggregate({"x": "sum", "y": "max"})
res = df4.compute()
if isinstance(res, pd.Series) or isinstance(res, pd.DataFrame):
    res = res.sort_index()
print(res)


df4 = df4.repartition(npartitions=1)
joined = df.merge(
    df4, left_on="name", right_index=True, suffixes=("_original", "_aggregated")
)

print(joined.head())


print(df[["x", "y"]].resample("1h").mean().head())


X, y = make_classification(n_samples=1000, random_state=0)
print(X[:5])


param_grid = {
    "C": [0.001, 0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0],
    "kernel": ["rbf", "poly", "sigmoid"],
    "shrinking": [True, False],
}

grid_search = GridSearchCV(
    SVC(gamma="auto", random_state=0, probability=True),
    param_grid=param_grid,
    return_train_score=False,
    cv=3,
    n_jobs=-1,
)


print(grid_search.fit(X, y))

cv_results = pd.DataFrame(grid_search.cv_results_)
drop_cols = [
    c
    for c in ["mean_fit_time", "std_fit_time", "mean_score_time", "std_score_time"]
    if c in cv_results.columns
]
print(cv_results.drop(columns=drop_cols).head())

print(grid_search.predict(X)[:5])


X, y = dask_ml.datasets.make_blobs(
    n_samples=100, chunks=1000, random_state=0, centers=3
)
X = X.persist()

km = dask_ml.cluster.KMeans(
    n_clusters=3, init_max_iter=2, oversampling_factor=10, random_state=0
)
print(km.fit(X))
