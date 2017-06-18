import pandas as pd
import matplotlib.pyplot as plt

def read_output_epsilon(fname):
    res_cls = pd.Series(())
    res_nfs = pd.Series(())
    with open(fname, 'r') as f:
        epsilon = 0.0
        for line in f:
            line_list = line.strip().split(' ')
            if line_list[0] == 'after':
                epsilon = float(line_list[-1][:-1])
            if line_list[0] == 'cross':
                res_cls[epsilon] = float(line_list[-1])
            if line_list[0] == 'size' and line_list[2] == 'data':
                res_nfs[epsilon] = int(line_list[-1][:-1])
    return res_cls.drop(0.0), res_nfs.drop(0.0)
    

def draw(cls, nfs, output_fname):
    fig, axes = plt.subplots(2, 1)
    cls.plot(ax=axes[0], style='o-', ylim=(0.7, 1.0), title='Prediction accuracy')
    nfs.plot(ax=axes[1], style='*-', ylim=(0, 50), title='The number of selected features')
    plt.xlabel('epsilon')
    #plt.show()
    plt.savefig("%s.png"%output_fname)
    plt.close()


if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    cls, nfs = read_output_epsilon(fname)
    output_fname = "opt_epsilon_on_%s"%fname.split('.')[0][:-4]
    cls.to_csv("%s_cls.csv"%output_fname)
    nfs.to_csv("%s_nfs.csv"%output_fname)
    draw(cls, nfs, output_fname)
