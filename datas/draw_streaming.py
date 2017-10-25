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
    # cls.name = 'prediction accuracy'
    return cls.drop('1000')


def read_output_streaming_of_one_dataset(dstype, dataset_name):
    alg = "sfs_l21"
    cls_l21 = read_output_streaming(
        "%s/all_result/streaming_l21/%s_cls.output_streaming" % (dstype, dataset_name))
    cls_l21.name = alg
    cls = cls_l21

    algs = "grafting osfs Alpha_investing saola".split()
    for alg in algs:
        fname = "%s/all_result/streaming_%s/%s_cls.output_streaming" % (
            dstype, alg, dataset_name)
        cls_tmp = read_output_streaming(fname)
        cls_tmp.name = alg
        cls = pd.concat((cls, cls_tmp), axis=1)
    return cls


def draw(cls, fname):
    fig, ax = plt.subplots(1, 1)
    style = 'o- ^-- s-. p: D:'.split(' ')
    cls.plot(ax=ax, style=style, ylim=(0.0, 1.0), rot=30)
    ax.set_ylabel('Prediction accuracy')
    ax.set_xlabel('The percentage of features streaming in (%)')
    ax.set_title(fname)

    fig.set_size_inches(12, 8)
    fig.savefig('images_streaming/%s.png' % fname, bbox_inches='tight')
    plt.close()


def get_datasets_name():
    datasets_name = {}
    with open('selected_datasets.txt', 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue
            dstype, dsname = line.split(":")
            dstype = dstype.strip()
            datasets_name[dstype.strip()] = dsname
    return datasets_name


def main():
    datasets_name = get_datasets_name()
    for dstype, dsnames in datasets_name.iteritems():
        for dsname in dsnames.split():
            print "draw %s/%s" % (dstype, dsname)
            cls = read_output_streaming_of_one_dataset(dstype, dsname)
            cls.to_csv("images_streaming/%s.csv" % dsname)
            draw(cls, dsname)
            print "finish %s/%s" % (dstype, dsname)


if __name__ == '__main__':
    main()
    print "Done!"
