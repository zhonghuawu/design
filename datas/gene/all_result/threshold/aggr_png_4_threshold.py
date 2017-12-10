from matplotlib import image
import numpy as np

if __name__=='__main__':
    # img_names="SMK_CAN_187 GLI_85 Prostate_GE DLBCL".split()
    img_names="SMK_CAN_187 GLIOMA Prostate_GE SRBCT".split()
    img1=image.imread("%s_one.png"%img_names[0])
    img1=np.concatenate((img1, image.imread("%s_one.png"%img_names[1])), axis=1)

    img2=image.imread("%s_one.png"%img_names[2])
    img2=np.concatenate((img2, image.imread("%s_one.png"%img_names[3])), axis=1)

    img=np.concatenate((img1, img2))

    image.imsave("aggr_one.png", img)


