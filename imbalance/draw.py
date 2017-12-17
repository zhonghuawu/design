# draw ruc and auc curve

import os
from sklearn import metrics
from matplotlib import pyplot as plt


def plotRUC(yt, ys, title=None):
    """
    paint ROC-AUC curve
    :param yt: y true
    :param ys: y prediction
    """
    f_pos, t_pos, thresh = metrics.roc_curve(yt, ys)
    auc_area = metrics.auc(f_pos, t_pos)
    print "auc_area:{}".format(auc_area)

    plt.plot(f_pos, t_pos, "darkorange", lw=2, label="AUC = %.2f" % auc_area)
    plt.legend(loc="lower right")
    plt.plot([0, 1], [1, 0], color='navy', linestyle='--')
    plt.title("ROC-AUC curve for %s" % title)
    plt.ylabel("True Pos Rate")
    plt.xlabel("False Pos Rate")
    plt.show()
    # plt.savefig(os.path.join(CWD, "middlewares/roc"+title+".png"))


def main():
    yt = [1,1,1,0,0]
    ys = [0,1,1,1,0]
    title = 'test'
    plotRUC(yt, ys, title)


if __name__ == '__main__':
    main()