import xml.etree.ElementTree as ET
from pathlib import Path
import os
import cv2

xml_path = "/home/shreeram/mustafa_xml/"
images_path = "/home/shreeram/mustafa_data_yolo/images/"
output_dir = "/home/shreeram/Downloads/xml_images_test/"

def read_content(xml_path):

    for file in os.listdir(xml_path):
        print(file)
        tree = ET.parse(os.path.join(xml_path, file))
        root = tree.getroot()

        list_with_all_boxes = []
        basename = Path(os.path.join(xml_path, file)).stem
        print(basename)
        img = cv2.imread(os.path.join(images_path, basename + ".png"))
        width = img.shape[0]
        height = img.shape[1]

        for boxes in root.iter('object'):

            filename = root.find('filename').text

            ymin, xmin, ymax, xmax = None, None, None, None

            ymin = int(boxes.find("bndbox/ymin").text)
            xmin = int(boxes.find("bndbox/xmin").text)
            ymax = int(boxes.find("bndbox/ymax").text)
            xmax = int(boxes.find("bndbox/xmax").text)

            x = xmin
            y = ymin
            w = (xmax - xmin)
            h = (ymax - ymin)

            # x = int(x)
            # y = int(y)
            # w = int(w)
            # h = int(h)

            cv2.rectangle(img, (x, y), (x+w, y+h), (0,0,255), 1)
            cv2.imwrite(os.path.join(output_dir, "{}_annotated.jpg".format(basename)), img)

            list_with_single_boxes = [xmin, ymin, xmax, ymax]
            list_with_all_boxes.append(list_with_single_boxes)

    return filename, list_with_all_boxes

name, boxes = read_content(xml_path)