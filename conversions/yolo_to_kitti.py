import os
import cv2
import time

# class_name = 'apron'

def check_class(class_id):
    if class_id == 0:
        class_name = 'device'
    else:
        # class_name = None
        print("Class ID exceeds the number of classes")
    return class_name

# Restore the coordinates in the txt to the coordinates of the original photo
def restore_coordinate(yolo_bbox, image_w, image_h):
    coordinates_array = []
    for bbox in yolo_bbox:
        box_w = float(bbox[3]) * image_w
        box_h = float(bbox[4]) * image_h
        x_mid = float(bbox[1]) * image_w + 1
        y_mid = float(bbox[2]) * image_h + 1
        xmin = int(x_mid - box_w / 2)
        xmax = int(x_mid + box_w / 2)
        ymin = int(y_mid - box_h / 2) + 5 # Added an offset of 5;
        ymax = int(y_mid + box_h / 2) + 5
        class_id = int(bbox[0])
        class_name = check_class(class_id)
        bbox_array = [xmin, ymin, xmax, ymax, class_name]
        # bbox_array = [xmin, ymin, xmax, ymax]
        coordinates_array.append(bbox_array)
    return coordinates_array
    # return [xmin, ymin, xmax, ymax]


# Generate txt tag file in kitti format
def write_to_kitti_txt(save_path, box, name):
    with open(os.path.join(save_path, name + '.txt'), 'w') as f:
        for b in box:
        # kitti tag file contains 15 parameters
            # print("The class name present in this image is ", class_name)
            new_info = str(b[4]) + ' ' + '0' + ' ' + '0' + ' ' + '0' + ' '\
                        + str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + ' ' + str(b[3]) \
                        + ' ' + '0' + ' ' + '0' + ' ' + '0' + ' ' + '0' + ' ' + '0' \
                        + ' ' + '0' + ' ' + '0' + '\n'
            f.writelines(new_info)
        # f.writelines(new_info)
    f.close()


# Get the labels file and images file of the photo, and generate a new label file
def restore_results(images_folder, labels_folder, output_dir):
    labels = os.listdir(labels_folder)
    for label in labels:
        name = label.split('.')[0]
        print(name)
        with open(os.path.join(labels_folder, label), 'r') as f:
            array = []
            # info = f.readline().strip('\n')
            for info in f:
                print("information is ", info.strip())
                label = info.split(' ')
                array.append(label)
                print("Label as read from the yolo txt file is ", label)
            img = cv2.imread(os.path.join(images_folder, name + '.jpg'))
            # print(name)
            img = cv2.resize(img, (960, 544))
            cv2.imwrite(os.path.join(output_dir, "{}.jpg".format(name)), img)
            w = img.shape[1]
            h = img.shape[0]
            # class_name = label[0]
            ori_box = restore_coordinate(array, w, h)
            write_to_kitti_txt('/home/shreeram/Downloads/frisking_kitti/labels', ori_box, name)
            # Draw the converted coordinate value onto the original picture and display it for viewing
            # cv2.rectangle(img, (ori_box[0], ori_box[1]), (ori_box[2], ori_box[3]), (0, 255, 255), 2)
            # cv2.imshow('Transfer_label', img)
            # if cv2.waitKey(100) & 0XFF == ord('q'):
            #     break
        f.close()
    # cv2.destoryAllWindows()


if __name__ == '__main__':
    s = time.time()
    print('----Data conversion start---')

    restore_results('/home/shreeram/Downloads/frisking_data_yolo/images',
                    '/home/shreeram/Downloads/frisking_data_yolo/labels',
                    '/home/shreeram/Downloads/frisking_kitti/images')

    print('---Time-consuming: {:.3f}ms'.format(time.time() - s))
    print('---Data conversion succeeded---')