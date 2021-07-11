import os
from PIL import Image, ImageDraw
import glob
import numpy as np
import tqdm
import cv2

def main(kitti_base_dir, output_dir):
    for imagefile in glob.glob(os.path.join(kitti_base_dir+'images/', '*')):
        # with open(imagefile, 'rb') as im_handle:
        print("im handle is ", imagefile)
        # pil_image = Image.open(im_handle)
        # image_array = np.array(pil_image)
        image = cv2.imread(imagefile)
        filename, extension = os.path.splitext(imagefile)
        # print("Filename is ", filename)
        file_name = os.path.basename(filename)
        print("file_name is ", file_name)
        # img = Image.open(os.path.join(kitti_base_dir+'images/', file_name + '.jpg'))
        text_file = open(os.path.join(kitti_base_dir + 'labels/', file_name + '.txt'), 'r')
        # text_file = filename.replace(kitti_base_dir+'images/', kitti_base_dir+'labels/')+'.txt'
        print("Text_file is as follows", text_file)
        bbox = []
        category = []
        for line in text_file:
            features = line.split()
            bbox.append([float(features[4]), float(features[5]), float(features[6]), float(features[7])])
            category.append(features[0])
        print("Bounding Box", bbox)
        print("Bounding Box shape is", len(bbox)) 
        print("Category:", category)
        print("Category shape is ", len(category))
        i = 0
        for bb in bbox:
            # draw_img = ImageDraw.Draw(pil_image)
            shape = ((int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])))
            # if category[i] == 'helmet':
                # outline_clr = "black"
            # elif category[i] == 'apron':
                # outline_clr = "yellow"
            color = (0, 0, 0)
            print(image)
            # draw_img.rectangle(shape, fill=None, outline=outline_clr, width=3)
            image = cv2.rectangle(image, shape[0], shape[1], color, 1)
            print("Image drawn")
            # pil_image.save(os.path.join(output_dir, "{}_annotated.jpg".format(file_name)))
            cv2.imwrite(os.path.join(output_dir, "{}_annotated.jpg".format(file_name)), image)
            print("Image saved successfully")
            i += 1
            
        # img.show()
    
if __name__ == '__main__':
    main(kitti_base_dir='/home/shreeram/Downloads/infer/test_infer/', output_dir='/home/shreeram/Downloads/infer_test/')

