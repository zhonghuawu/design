import draw_epsilon as de
import sys
import os

def get_datasets_name():
    datasets_name = []
    with open('../all_attribute.csv', 'r') as f:
        f.readline()
        for line in f:
            if line.startswith("#"):
                continue
            datasets_name.append(line.split(',')[0])
    return datasets_name

def main():
    datasets_name = get_datasets_name()
    postfix="_cls.output_epsilon"
    for dataset_name in datasets_name:
        print "draw %s"%dataset_name
        fname="%s%s"%(dataset_name, postfix)
        cls, nfs = de.read_output_epsilon(fname)
        de.draw(cls, nfs, dataset_name)
        print "finish %s"%dataset_name

if __name__ == '__main__':
    main()
    print "Done!"
