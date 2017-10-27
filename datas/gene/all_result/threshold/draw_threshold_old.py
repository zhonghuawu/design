import pandas as pd
import matplotlib.pyplot as plt

def read_output_threshold(fname):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    with open(fname, 'r') as f:
        threshold = 0.0
        for line in f:
            line_list = line.strip().split(' ')
            if line_list[0] == 'after':
                threshold = float(line_list[-4][:-1])
            if line_list[0] == 'cross':
                res_cls[threshold] = float(line_list[-1])
            if line_list[0] == 'size' and line_list[2] == 'data':
                res_nfs[threshold] = int(line_list[-1][:-1])
    res_cls.name = 'prediction accuracy'
    res_nfs.name = 'number of selected features'
    return res_cls.drop(0.0), res_nfs.drop(0.0)
    

def draw(cls, nfs, fname):
    fig, axes = plt.subplots(2, 1)
    cls.plot(ax=axes[0], style='o-', ylim=(0.5, 1.0))
    nfs.plot(ax=axes[1], style='*-', ylim=(0, 100))
    axes[0].set_ylabel('Prediction accuracy')
    axes[1].set_ylabel('The number of selected features')
    axes[1].set_xlabel('lambda')
    fig.suptitle('Effect of lambda on dataset %s'%fname)

    # plt.show()
    fig.set_size_inches(9, 6)
    fig.savefig('%s.png'%fname, bbox_inches='tight')
    plt.close()

def draw_accuracy(cls, fname):
    fig, ax = plt.subplots(1, 1)
    cls.plot(ax=ax, style='*-', ylim=(0.6, 1.0))
    ax.set_ylabel('Prediction accuracy')
    ax.set_xlabel("lambda")
    ax.set_title("Prediction accuracy as lambda changes on dataset %s"%fname)
    plt.show()
    plt.close()

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    cls, nfs = read_output_threshold(fname)
    fname = fname.split('.')[0][:-4]
    draw(cls, nfs, fname)
    # draw_accuracy(cls, fname)
    #output_fname = "opt_threshold_on_%s"%fname
    #res = pd.concat((cls, nfs), axis=1)
    #res.index.name = 'lambda'
    #res.to_csv("%s.csv"%output_fname)
    #print res


    #cls.to_csv("%s_cls.csv"%output_fname)
    #nfs.to_csv("%s_nfs.csv"%output_fname)
