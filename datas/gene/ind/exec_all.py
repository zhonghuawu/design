import os

def exec_command(fname):
    os.system("python classifying.py %s.ind > result_tmp/%s_cls.output"%(fname, fname))

fnames = os.listdir(os.getcwd())
k = 1

for fname in fnames:
    name_ext = os.path.splitext(fname)
    if name_ext[-1] == '.mat':
        print k
        print "start classifying %s..."%fname
        exec_command(name_ext[0])
        print "finish classifying %s..."%fname
        k+=1


