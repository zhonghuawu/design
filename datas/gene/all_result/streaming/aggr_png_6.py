from matplotlib import image
import numpy as np

if __name__=='__main__':
    img_names="TOX_171 SMK_CAN_187".split()
    img1=np.concatenate((image.imread("%s.png"%img_names[0]),image.imread("%s.png"%img_names[1])), axis=1)
    # img1=image.imread("%s.png"%img_names[0])
    # img1=np.concatenate((img1, image.imread("%s.png"%img_names[1])), axis=1)
    # img1=np.concatenate((img1, image.imread("%s.png"%img_names[2])), axis=1)

    img_names="ALLAML GLI_85".split()
    img2=np.concatenate((image.imread("%s.png"%img_names[0]),image.imread("%s.png"%img_names[1])), axis=1)
    
    img_names="GLI_85 Prostate_GE".split()
    img3=np.concatenate((image.imread("%s.png"%img_names[0]),image.imread("%s.png"%img_names[1])), axis=1)

    img=np.concatenate((img1, img2, img3))
    image.imsave("aggr_vertical.png", img)
    

