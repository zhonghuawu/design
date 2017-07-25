import pandas as pd
import matplotlib.pyplot as plt

def read_output_streaming_cls_nfs(fname):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    with open(fname, 'r') as f:
        epsilon = 0.0
        for line in f:
            line_list = line.strip().split()
            if line_list[0] == 'after':
                epsilon = float(line_list[-1][:-1])
            if line_list[0] == 'cross':
                res_cls[epsilon] = float(line_list[-1])
            if line_list[0] == 'size' and line_list[2] == 'data':
                res_nfs[epsilon] = int(line_list[-1][:-1])
    res_cls.name = 'prediction accuracy'
    res_nfs.name = 'number of selected features'
    return res_cls.drop(0.0), res_nfs.drop(0.0)

def read_output_streaming(fname):
    cls = pd.Series(())
    with open(fname, 'r') as f:
        percentage = "1000"
        for line in f:
            line_list = line.strip().split()
            if line_list[0] == 'after':
                percentage = line_list[3][:-1]
            if line_list[0] == 'cross':
                cls[percentage] = float(line_list[-1])
    cls.name = 'prediction accuracy'
    return cls.drop('1000')

    
def draw(cls, fname):
    fig, ax = plt.subplots(1, 1)
    cls.plot(ax=ax, style='o-', ylim=(0.6, 1.0))
    #nfs.plot(ax=axes[1], style='*-', ylim=(0, 90))
    ax.set_ylabel('Prediction accuracy')
    ax.set_xlabel('The percentage of features streaming in (%)')
    ax.set_title(fname)

    fig.set_size_inches(12, 8)
    fig.savefig('%s.png'%fname, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    cls = read_output_streaming(fname)
    print cls
    fname = fname.split('.')[0][:-4]
    draw(cls, fname)
