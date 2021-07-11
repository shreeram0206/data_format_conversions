import cv2
import matplotlib.pyplot as plt
import os
from pathlib import Path

output_dir = "/home/shreeram/Downloads/yolo_bbox/"
path = "/home/shreeram/Downloads/test_images/"
label_path = "/home/shreeram/Downloads/yolo_conversions/"

for file in os.listdir("/home/shreeram/Downloads/test_images/"):
    # print(file)
    basename = Path(os.path.join(path, file)).stem
    print(basename)
    # img = cv2.imread("/home/shreeram/mustafa_data_yolo/images/00000162.png")
    img = cv2.imread(os.path.join(path, file))
    dh, dw, _ = img.shape

    fl = open(os.path.join(label_path, basename + ".txt"), 'r')
    data = fl.readlines()
    fl.close()

    for dt in data:

        # Split string to float
        _, x, y, w, h = map(float, dt.split(' '))

        # Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
        # via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
        l = int((x - w / 2) * dw)
        r = int((x + w / 2) * dw)
        t = int((y - h / 2) * dh)
        b = int((y + h / 2) * dh)

        if l < 0:
            l = 0
        if r > dw - 1:
            r = dw - 1
        if t < 0:
            t = 0
        if b > dh - 1:
            b = dh - 1

        cv2.rectangle(img, (l, t), (r, b), (0, 0, 0), 1)
        cv2.imwrite(os.path.join(output_dir, "{}_annotated.jpg".format(file)), img)
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()
