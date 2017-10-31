
import numpy as np
from matplotlib import image


def merge_image_horizontal(img1, img2):
    height = min(img1.shape[0], img2.shape[0])
    img1 = img1[:height, :]
    img2 = img2[:height, :]
    img = np.concatenate((img1, img2), axis=1)
    return img


def merge_image_vertical(img1, img2):
    width = min(img1.shape[1], img2.shape[1])
    img1 = img1[:, :width]
    img2 = img2[:, :width]
    img = np.concatenate((img1, img2), axis=0)
    return img


def read_image(nm1, nm2, nm3):
    img1 = image.imread("%s.png" % nm1)
    img2 = image.imread("%s.png" % nm2)
    img3 = image.imread("%s.png" % nm3)
    img = merge_image_horizontal(img1, img2)
    img = merge_image_horizontal(img, img3)
    return img


def aggr(image_names, wfname):
    imgs = []
    for nms in image_names.split(","):
        nm1, nm2, nm3 = nms.split()
        imgs.append(read_image(nm1, nm2, nm3))
    img = merge_image_vertical(imgs[0], imgs[1])
    image.imsave("%s.png" % wfname, img)


def main():
    # img_names = "pixraw10P TOX_171,SMK_CAN_187 Prostate_GE,arcene PCMAC"
    # aggr(img_names, "aggr_vertical")
    img_names = "pixraw10P TOX_171 SMK_CAN_187,Prostate_GE arcene PCMAC"
    aggr(img_names, "aggr_horizontal")

    # img_names = "ALLAML GLI_85,GLIOMA orlraws10P,RELATHE warpPIE10P"
    # aggr(img_names, "aggr_vertical_other")


if __name__ == '__main__':
    main()
