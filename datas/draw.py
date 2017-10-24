import pandas as pd
import matplotlib.pyplot as plt


def get_dataset_name():
    algs = "sfs_l21 grafting Alpha_investing osfs saola".split()
    clses, nfses = None, None
    with open("selected_datasets.txt", 'r') as f:
        for line in f:
            if line.startswith("#"):
                continue
            dstype, dsname = line.split(":")
            dstype = dstype.strip()
            dsname = dsname.split()
            clspath = "%s/all_result/all_cls.csv" % dstype
            nfspath = "%s/all_result/all_nfs.csv" % dstype
            clstmp = pd.read_csv(clspath, index_col=0)[algs].ix[dsname]
            nfstmp = pd.read_csv(nfspath, index_col=0)[algs].ix[dsname]
            clses = pd.concat((clses, clstmp))
            nfses = pd.concat((nfses, nfstmp))
    return clses, nfses


def draw(cls, nfs, fn_png):
    fig, axes = plt.subplots(2, 1)
    # style='o- ^-- s-. +-- x-.'.split(' ')
    style = 'o- ^-- s-. p: D:'.split(' ')
    cls.plot(ax=axes[0], style=style, ylim=(0.0, 1.0), rot=45)
    nfs.plot(ax=axes[1], style=style, ylim=(0, 300), rot=45)

    axes[0].set_ylabel('Prediction accuracy')
    axes[1].set_ylabel('The number of selected features')

    plt.xlabel("datasets")
    # plt.show()
    fig.set_size_inches(16, 12)
    fig.savefig("%s.png" % fn_png, bbox_inches='tight')
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
    nfs.plot(ax=ax2, style=style2, ylim=(0, 300))
    plt.xlabel("datasets")
    fig.set_size_inches(12, 8)
    ax1.legend(loc="center left")
    ax2.legend(loc="center left")
    alg1, alg2 = cls.columns
    fig.savefig("all_%s_vs_%s.png" % (alg1, alg2), bbox_inches='tight')
    plt.close()


def draw_vs_others(cls, nfs):
    my_alg = 'sfs_l21'
    vs_algs = 'grafting osfs Alpha_investing saola'.split()
    for vs_alg in vs_algs:
        cls_tmp = cls[[my_alg, vs_alg]]
        nfs_tmp = nfs[[my_alg, vs_alg]]
        draw_sfs_l21_vs_other(cls_tmp, nfs_tmp)


if __name__ == '__main__':
    clses, nfses = get_dataset_name()
    # clses.to_csv("all_cls.csv")
    # nfses.to_csv("all_nfs.csv")
    print clses
    print nfses
    # draw_vs_others(clses, nfses)
    draw(clses, nfses, "all")
