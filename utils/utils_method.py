import numpy
import os
import cv


# 获取某个文件夹下的所有图片路径
def get_image_paths(directory):
    return [x.path for x in os.scandir(directory) if x.name.endswith(".jpg") or x.name.endswith(".png")]


def load_images(image_paths, convert=None):
    iter_all_images = (cv2.imread(fn) for fn in image_paths)
    if convert:
        iter_all_images = (convert(img) for img in iter_all_images)
    for i, image in enumerate(iter_all_images):
        if i == 0:
            all_images = numpy.empty((len(image_paths),) + image.shape, dtype=image.dtype)
        all_images[i] = image
    return all_images


if __name__ == '__main__':
    result = get_image_paths("/Users/fan/opt/image")
    print(result)
