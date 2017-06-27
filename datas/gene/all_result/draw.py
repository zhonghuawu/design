import pandas as pd
import matplotlib.pyplot as plt

def draw(cls, nfs):
    #dataset = cls['dataset']
    print pd.Series(cls.index, index=range(1,9))
    #cls = cls.drop('dataset', axis=1)
    cls = cls.drop('osfs5', axis=1)
    if 'origin_data' in cls.columns:
        cls = cls.drop('origin_data', axis=1)
    #nfs = nfs.drop('dataset', axis=1)
    nfs = nfs.drop('osfs5', axis=1)

    fig, axes = plt.subplots(2, 1)

    style='o- ^- x- *- .-'.split(' ')
    cls.plot(ax=axes[0], style=style, ylim=(0.4, 1.0))
    nfs.plot(ax=axes[1], style=style, ylim=(0, 60))

    axes[0].set_ylabel('Prediction accuracy')
    axes[1].set_ylabel('The number of selected features')

    plt.xlabel("datasets")
    plt.show()

if __name__=='__main__':
    drop_dataset = "lymphoma SMK_CAN_187 GLI_85 lung".split(" ")
    nfs = pd.read_csv('all_nfs.csv', index_col=0)
    nfs = nfs.drop(drop_dataset)
    cls = pd.read_csv('all_cls.csv', index_col=0)
    cls = cls.drop(drop_dataset)
    draw(cls, nfs)
