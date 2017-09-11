import os
    
# alg = 'streaming_grafting'
alg = 'streaming_l21'

def exec_command(fname):
    dataset_fname=r'ind_%s/%s.ind_%s'%(alg, fname, alg)
    output_fname=r'all_result/%s/%s_cls.output_%s'%(alg, fname, alg)
    os.system("python classifying.py %s > %s"%(dataset_fname, output_fname))

def get_datasets_name():
    fname=r'all_result/all_attribute.csv'
    datasets_fname=[]
    with open(fname, 'r') as f:
        f.readline()
        for line in f:
            datasets_fname.append(line.split(',')[0])
    return datasets_fname

def main():
    datasets_fname =  get_datasets_name()
    for dataset_fname in datasets_fname:
        print "process %s"%dataset_fname
        exec_command(dataset_fname)
        print "finish %s"%dataset_fname

if __name__=='__main__':
    main()
    print "Done!"
    
