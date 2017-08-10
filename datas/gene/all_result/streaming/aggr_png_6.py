from matplotlib import image
import numpy as np

if __name__=='__main__':
    img_names="TOX_171 SMK_CAN_187 ALLAML".split()
    img1=image.imread("%s.png"%img_names[0])
    img1=np.concatenate((img1, image.imread("%s.png"%img_names[1])), axis=1)
    img1=np.concatenate((img1, image.imread("%s.png"%img_names[2])), axis=1)
    
    img_names="GLI_85 Prostate_GE Lung_Cancer".split()
    img2=image.imread("%s.png"%img_names[0])
    img2=np.concatenate((img2, image.imread("%s.png"%img_names[1])), axis=1)
    img2=np.concatenate((img2, image.imread("%s.png"%img_names[2])), axis=1)

    img=np.concatenate((img1, img2))
    image.imsave("aggr.png", img)
    

