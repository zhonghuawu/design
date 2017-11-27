import pandas as pd
import matplotlib.pyplot as plt

def draw(cls, nfs):
    fig, axes = plt.subplots(2, 1)

    # style='o- ^-- s-. +-- x-.'.split(' ')
    style='o- ^-- s-. p: D:'.split(' ')
    cls.plot(ax=axes[0], style=style, ylim=(0.0, 1.0))
    nfs.plot(ax=axes[1], style=style, ylim=(0, 100))

    axes[0].set_ylabel('Prediction accuracy')
    axes[1].set_ylabel('The number of selected features')

    plt.xlabel("datasets")
    #plt.show()
    fig.set_size_inches(16, 12)
    fig.savefig("all_final.png", bbox_inches='tight')
    plt.close()

def draw_sfs_l21_vs_other(cls, nfs):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.set_ylabel('Prediction accuracy')
    ax2.set_ylabel('The number of selected features')
    style1 = 'ro- gs--'.split(' ')
    style2 = 'r^- g*--'.split(' ')
    cls.plot(ax=ax1, style=style1, ylim=(0.0, 1.0))
    nfs.plot(ax=ax2, style=style2, ylim=(0, 100))
    plt.xlabel("datasets")
    fig.set_size_inches(12, 8)
    ax1.legend(loc="upper left")
    ax2.legend(loc="center right")
    alg1, alg2=cls.columns
    fig.savefig("all_%s_vs_%s.png"%(alg1, alg2), bbox_inches='tight')
    plt.close()

def draw_vs_others(cls, nfs):
	my_alg = 'sfs_l21'
	vs_algs = 'grafting osfs Alpha_investing saola'.split()
	for vs_alg in vs_algs:
		cls_tmp = cls[[my_alg, vs_alg]]
		nfs_tmp = nfs[[my_alg, vs_alg]]
		draw_sfs_l21_vs_other(cls_tmp, nfs_tmp)

def get_cls_nfs_1():
    cls = pd.read_csv('all_cls.csv')
    if 'origin_data' in cls.columns:
        cls = cls.drop('origin_data', axis=1)
    nfs = pd.read_csv('all_nfs.csv')

    # remove osfs alpha=0.05 result
    try:
        cls = cls.drop('osfs5', axis=1)
        nfs = nfs.drop('osfs5', axis=1)

    except :
        pass

    try :
        cls = cls.drop('dataset', axis=1).rename(index=lambda i: i+1)
        nfs = nfs.drop('dataset', axis=1).rename(index=lambda i: i+1)
    except :
        pass

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
    # draw(cls, nfs)
    draw_vs_others(cls, nfs)
