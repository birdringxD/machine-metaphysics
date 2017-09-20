# -*- coding: utf-8 -*-
import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages/')
import cv2


def show(img):
    cv2.imshow('Image', img)
    cv2.waitKey(0)


def get_face_image(img, margin_extend_rate=0.3):
    faces = []
    coordinates = []
    faces_coordinate_ = face_cascade.detectMultiScale(
        img,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(5, 5)
    )
    for (x, y, w, h) in faces_coordinate_:
        x_extend = int(w * margin_extend_rate)
        y_extend = int(h * margin_extend_rate)
        if y-y_extend > 0:
            y_min = y-y_extend
        else:
            y_min = 0

        if y+h+y_extend > img.shape[0]:
            y_max = img.shape[0]
        else:
            y_max = y+h+y_extend

        if x-x_extend > 0:
            x_min = x-x_extend
        else:
            x_min = 0

        if x+w+x_extend > img.shape[1]:
            x_max = img.shape[1]
        else:
            x_max = x+w+x_extend

        roi = img[y_min:y_max, x_min:x_max]
        faces.append(roi)
        coordinates.append((x, y))
        # print('FaceDetected')

    return faces, coordinates


def draw_faces(img):
    faces = []
    image = img
    faces_coordinate_ = face_cascade.detectMultiScale(
        img,
        scaleFactor=1.15,
        minNeighbors=5,
        minSize=(5, 5)
    )
    print "__Found {0} faces!__".format(len(faces_coordinate_))
   #  print faces_coordinate_
    for (x, y, w, h) in faces_coordinate_:
        print x, y, w, h, '-=-=-=-=-=-='
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image

face_cascade = cv2.CascadeClassifier(r'./haarcascade_frontalface_default.xml')

if __name__ == '__main__':
    _img = cv2.imread('girls.jpg')
    img_drawed = draw_faces(_img)
    faces, coordinates = get_face_image(_img)
    #print faces
    #print coordinates
    #print len(faces)
    # cv2.imshow("Faces found", img_drawed)
    show(img_drawed)
    for img in faces: show(img)
