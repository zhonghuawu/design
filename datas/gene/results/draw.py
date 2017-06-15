import pandas as pd
import matplotlib.pyplot as plt

cls = pd.read_csv('all_cls.csv', index_col=0)
nfs = pd.read_csv('all_nfs.csv', index_col=0)

fig, axes = plt.subplots(2, 1)

cls.plot(ax=axes[0], ylim=(0.0, 1.0))
nfs.plot(ax=axes[1], ylim=(0, 100))

plt.show()
