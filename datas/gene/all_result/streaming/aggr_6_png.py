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


def read_3_image(nm1, nm2, nm3):
    img1 = image.imread("%s.png" % nm1)
    img2 = image.imread("%s.png" % nm2)
    img3 = image.imread("%s.png" % nm3)
    img = merge_image_horizontal(img1, img2)
    img = merge_image_horizontal(img, img3)
    return img

def read_2_image(nm1, nm2):
    img1 = image.imread("%s.png" % nm1)
    img2 = image.imread("%s.png" % nm2)
    img = merge_image_horizontal(img1, img2)
    return img


def main():
    nms = "TOX_171 SMK_CAN_187 ALLAML GLI_85 Lung_Cancer Prostate_GE".split()

    img1 = read_2_image(nms[0], nms[1])
    img2 = read_2_image(nms[2], nms[3])
    img3 = read_2_image(nms[4], nms[5])

    img = merge_image_vertical(img1, img2)
    img = merge_image_vertical(img, img3)

    image.imsave("aggr_vertical.png", img)

if __name__ == '__main__':
    main()
