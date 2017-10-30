
import numpy as np
from matplotlib import image


def merge_image(img1, img2, _axis=1):
    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])
    img1 = img1[:height, :width]
    img2 = img2[:height, :width]
    print img1.shape, img2.shape
    img = np.concatenate((img1, img2), axis=_axis)
    return img


def read_image(nm1, nm2):
    img1 = image.imread("%s.png" % nm1)
    img2 = image.imread("%s.png" % nm2)
    return merge_image(img1, img2)


def aggr(image_names, wfname):
    imgs = []
    for nms in image_names.split(","):
        nm1, nm2 = nms.split()
        type1, name1 = nm1.split('.')
        type2, name2 = nm2.split('.')
        nm1 = "../%s/all_result/epsilon/%s_one" % (type1, name1)
        nm2 = "../%s/all_result/epsilon/%s_one" % (type2, name2)
        imgs.append(read_image(nm1, nm2))
    img = merge_image(imgs[0], imgs[1], 0)
    image.imsave("%s.png" % wfname, img)


def main():
    img_names = "gene.SMK_CAN_187 gene.GLIOMA,gene.Prostate_GE other.arcene"
    aggr(img_names, "aggr_vertical")

    # img_names = "ALLAML GLI_85,GLIOMA orlraws10P,RELATHE warpPIE10P"
    # aggr(img_names, "aggr_vertical_other")


if __name__ == '__main__':
    main()
