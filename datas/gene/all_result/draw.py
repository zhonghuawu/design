import pandas as pd
import matplotlib.pyplot as plt

def draw(cls, nfs):
    #dataset = cls['dataset']
    #print pd.Series(cls.index, index=range(1,9))

    fig, axes = plt.subplots(2, 1)

    style='o- ^-- s-. p:'.split(' ')
    cls.plot(ax=axes[0], style=style, ylim=(0.4, 1.0))
    nfs.plot(ax=axes[1], style=style, ylim=(0, 60))

    axes[0].set_ylabel('Prediction accuracy')
    axes[1].set_ylabel('The number of selected features')

    plt.xlabel("datasets")
    #plt.show()
    fig.set_size_inches(12, 8)
    fig.savefig("all_final_clear.png", bbox_inches='tight')
    plt.close()

def get_cls_nfs_1():
    cls = pd.read_csv('all_cls.csv')
    if 'origin_data' in cls.columns:
        cls = cls.drop('origin_data', axis=1)
    nfs = pd.read_csv('all_nfs.csv')
    # remove osfs alpha=0.05 result
    cls = cls.drop('osfs5', axis=1)
    nfs = nfs.drop('osfs5', axis=1)

    cls = cls.drop('dataset', axis=1).rename(index=lambda i: i+1)
    nfs = nfs.drop('dataset', axis=1).rename(index=lambda i: i+1)
    return cls, nfs

def get_cls_nfs_2():
    cls = pd.read_csv('all_cls.csv', index_col=0)
    if 'origin_data' in cls.columns:
        cls = cls.drop('origin_data', axis=1)
    nfs = pd.read_csv('all_nfs.csv', index_col=0)
    # remove osfs alpha=0.05 result
    cls = cls.drop('osfs5', axis=1)
    nfs = nfs.drop('osfs5', axis=1)

    # remove some datasets
    drop_dataset = "lymphoma SMK_CAN_187 GLI_85 lung".split(" ")
    cls = cls.drop(drop_dataset)
    nfs = nfs.drop(drop_dataset)

    return cls, nfs

if __name__=='__main__':
    cls, nfs = get_cls_nfs_1()
    draw(cls, nfs)
