import cv2
import os
import numpy as np

def resize(image):
    new_image = None
    height,width,c = image.shape
    if height > width:
        new_image = cv2.resize(image,(3000,4000))
    else:
        new_image = cv2.resize(image,(4000,3000))
    return new_image

def convert_to_black_and_white(image,T_value):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, black_white_image = cv2.threshold(gray_image, T_value, 255, cv2.THRESH_BINARY)
    return black_white_image

def remove_noise(image):
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((3, 3), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return image

def make_font_thinner(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((3,3),np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image

def rotate(image,angle):
    if angle == 0:
        return image
    (height, width) = image.shape[:2]
    center = (width//2,height//2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_sorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = contours_sorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return crop

def add_borders(image):
    color = [255, 255, 255]
    top, bottom, left, right = [150]*4
    image_with_border = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return image_with_border

def preprocess_image(filename,angle,T_value):
    image = cv2.imread(filename)
    image = resize(image)
    image = convert_to_black_and_white(image,T_value)
    image = remove_noise(image)
    image = make_font_thinner(image)
    image = rotate(image,angle)
    image = remove_borders(image)
    image = add_borders(image)
    name = "temp/preprocessed_card_" + str(T_value) + ".jpg"
    cv2.imwrite(name,image)

def preprocess_images_all_versions(filename,angle):
    if os.path.isdir('temp') == False:
        os.mkdir('temp')
    T_value_list = [120,145,170]
    for T in T_value_list:
        preprocess_image(filename,angle,T)