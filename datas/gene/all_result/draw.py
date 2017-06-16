import pandas as pd
import matplotlib.pyplot as plt

cls = pd.read_csv('all_cls.csv')
dataset = cls['dataset']
print dataset
cls = cls.drop('dataset', axis=1)
if 'origin_data' in cls.columns:
    cls = cls.drop('origin_data', axis=1)
nfs = pd.read_csv('all_nfs.csv')
nfs = nfs.drop('dataset', axis=1)


fig, axes = plt.subplots(2, 1)

cls.plot(ax=axes[0], ylim=(0.4, 1.0))
nfs.plot(ax=axes[1], ylim=(0, 50))

plt.show()
