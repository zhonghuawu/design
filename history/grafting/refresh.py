import numpy as np
from pandas import Series, DataFrame

def refresh_selected(w, X_index, X_model, RetainCount):
    X_zero = X_model[:, 0]
    w_zero = w[0]
    X_dataframe = DataFrame(X_model[:, 1:].transpose(), index=X_index)
    w_series = Series(w[1:], index=X_index)
    w_series = w_series.sort_values(ascending=False)[:RetainCount]
    X_index_new = list(w_series.index)
    X_model_new = X_dataframe.ix[X_index_new].get_values().transpose()
    X_model_new = np.hstack((X_zero, X_model_new))
    w_new = w_series.get_values()
    w_new = np.hstack((w_zero, w_new))
    return w_new, X_index_new, X_model_new
