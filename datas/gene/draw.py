import sys

import pandas as pd
import matplotlib.pyplot as plt


def draw(cls, nfs, fn_png, write_to_folder):
    fig, axes = plt.subplots(2, 1)
    # style='o- ^-- s-. +-- x-.'.split(' ')
    style = 'o- ^-- s-. p: D:'.split(' ')
    cls.plot(ax=axes[0], style=style, ylim=(0.0, 1.0), rot=30)
    nfs.plot(ax=axes[1], style=style, ylim=(0, 100), rot=30)

    axes[0].set_ylabel('Prediction accuracy')
    axes[0].set_xticks(range(12))
    axes[0].set_xticklabels(cls.index)
    axes[1].set_ylabel('The number of selected features')
    axes[1].set_xticks(range(12))
    axes[1].set_xticklabels(nfs.index)

    plt.xlabel("datasets")
    # plt.show()
    fig.set_size_inches(16, 12)
    fig.savefig("%s/%s.png" % (write_to_folder, fn_png), bbox_inches='tight')
    plt.close()


def draw_sfs_l21_vs_other(cls, nfs, write_to_folder):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xticks(range(len(cls.index)))
    ax1.set_xticklabels(cls.index)
    ax2 = ax1.twinx()
    ax1.set_ylabel('Prediction accuracy')
    ax2.set_ylabel('The number of selected features')
    style1 = 'bo- gs--'.split()
    style2 = 'b^- g*--'.split()
    cls.plot(ax=ax1, style=style1, ylim=(0.0, 1.0), rot=30)
    nfs.plot(ax=ax2, style=style2, ylim=(0, 100))  # , kind='bar')
    plt.xlabel("datasets")
    fig.set_size_inches(12, 8)
    ax1.legend(loc="upper left")
    ax2.legend(loc="center right")
    alg1, alg2 = cls.columns
    classifiers = {
        "result":"SVM",
        "ab":"AdaBoost",
        "dt":"Decision Tree", 
        "gb":"Gradient Boosting",
        "lr":"Logistics Regression", 
        "nb":"Naive Bayes",
        "nn":"Neural Network",
        "rf":"Random Forest",
        "sgd":"Stochastic Gradient Descent"
    }
    clf = write_to_folder.split('_')[-1]
    ax1.set_title("%s vs %s(%s)"%(alg1, alg2, classifiers[clf]))
    fig.savefig("%s/all_%s_vs_%s.png" %
                (write_to_folder, alg1, alg2), bbox_inches='tight')
    plt.close()


def draw_vs_others(cls, nfs, write_to_folder):
    my_alg = 'sfs_l21'
    vs_algs = 'grafting osfs Alpha_investing saola'.split()
    for vs_alg in vs_algs:
        cls_tmp = cls[[my_alg, vs_alg]]
        nfs_tmp = nfs[[my_alg, vs_alg]]
        draw_sfs_l21_vs_other(cls_tmp, nfs_tmp, write_to_folder)


def get_datasets_order():
    datasets_order = []
    with open("datasets_order.txt", 'r') as f:
        for line in f:
            datasets_order.append(line.strip())
    return datasets_order


def get_cls_nfs(from_folder):
    cls = pd.read_csv('%s/all_cls.csv' % from_folder, index_col=0)
    try:
        cls = cls.drop('origin_data', axis=1)
    except:
        pass
    nfs = pd.read_csv('%s/all_nfs.csv' % from_folder, index_col=0)

    try:
        cls = cls.drop('osfs5', axis=1)
        nfs = nfs.drop('osfs5', axis=1)
    except:
        pass

    datasets_order = get_datasets_order()
    return cls.reindex(datasets_order), nfs.reindex(datasets_order)


def draw_compactness(nfs):
    fig, ax = plt.subplots(1, 1)
    style = 'o- ^-- s-. p-- D:'.split(' ')
    nfs.plot(ax=ax, style=style, ylim=(0, 50), rot=30)
    ax.set_ylabel('The number of selected features')
    ax.set_xticks(range(12))
    ax.set_xticklabels(nfs.index)
    ax.set_title("Compactness")

    fig.set_size_inches(12, 6)
    fig.savefig('all_result/all_nfs.png', bbox_inches='tight')
    plt.close()


def main(from_folder):
    clses, nfses = get_cls_nfs(from_folder)
    draw_vs_others(clses, nfses, from_folder)
    draw(clses, nfses, "all", from_folder)
    # print nfses
    # draw_compactness(nfses)


if __name__ == '__main__':
    main(sys.argv[1])
