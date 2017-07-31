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

def read_output_streaming_of_one_dataset(dataset_name):
    cls_l21 = read_output_streaming("../streaming_l21/%s_cls.output_streaming"%dataset_name)
    cls_l21.name = 'sfs_l21'
    cls_osfs = read_output_streaming("../streaming_osfs/%s_cls.output_streaming_osfs"%dataset_name)
    cls_osfs.name = 'osfs'
    cls_Alpha_investing = read_output_streaming("../streaming_Alpha_investing/%s_cls.output_streaming_Alpha_investing"%dataset_name)
    cls_Alpha_investing.name = 'Alpha_investing'
    cls = pd.concat((cls_l21, cls_osfs, cls_Alpha_investing), axis=1)
    return cls
    
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

def get_datasets_name():
    datasets_name = []
    with open('../all_attribute.csv', 'r') as f:
        f.readline()
        for line in f:
            datasets_name.append(line.split(',')[0])
    return datasets_name

def main():
    datasets_name = get_datasets_name()
    for dataset_name in datasets_name:
        print "draw %s"%dataset_name
        cls = read_output_streaming_of_one_dataset(dataset_name)
        draw(cls, dataset_name)
        print "finish %s"%dataset_name


if __name__ == '__main__':
    main()
    print "Done!"
    
