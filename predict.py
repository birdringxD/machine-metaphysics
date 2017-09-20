# from __future__ import print_function
import sys
# sys.path.append('/usr/local/lib/python2.7/site-packages/')
from keras.models import *
import keras.backend
import numpy as np
import sys
import os
import cv2
import csv
from scipy.stats import norm
import face_detection as fd

features = [[],[],[],[],[],[],[],[],[],[]]

def Chebyshev(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return max(np.abs(npvec1-npvec2))


def get_percentage(score):
    for i in range(len(list)):
        if score < float(list[i]):
            return (i + 1.0) / (len(list))


def get_AQ(score):
    score = float(score)
    percentage = get_percentage(score)
    print percentage ,"---%%%%%%%%%"
    #z_score = norm.ppf(percentage)
  #  print score, z_score, '___'
    return '%.1f' % (4.95 + percentage * 4.95)  # + '%.2f'% z_score
    # return int(100 + (z_score * 24))

def load_image(file):
    image = cv2.imread(file)
    image = cv2.resize(image, (256, 256))
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image


def predict_cv_img(img):
    img = cv2.resize(img, (256, 256))
    img = img / 255
    img = np.expand_dims(img, axis=0)
    return predict(img)


def predict(img):
    # print model.summary()
   # get_feature = keras.backend.function([keras.backend.learning_phase(),
    #model.layers[0].input], model.layers[13].output)

    return _model.predict(img) * 5.0


def training_test():
    filelist = os.listdir('./data')
    for i in filelist:
        print(i, '  ', predict(load_image('./data/' + i)))


def main():
    features = [[]]
    for i in sys.argv:
        if i.find('.jpg') != -1:
            img = load_image(i)
            predict(img)

_model = load_model('faceRank.h5')

list = []
with open('label.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        list.append(row['Attractiveness label'])
list.sort()
print(len(_model.layers))
layer_count=len(_model.layers)

model = Model(input=_model.input, output=_model.layers[12].output)

def save_predict_img(img_file, save_path):
    img = cv2.imread(img_file)
    l = img.shape[0]
    r = img.shape[1]
    print l, r
    if l >= 600 : t = (l * 1.0) / 600
    elif l <= 300 : t = (l * 1.0) / 300
    else : t = 1
    if l > r : img = cv2.resize(img, (int(r / t), int(l / t)))
    elif l == r : img = cv2.resize(img, (400, 400))
    else :img = cv2.resize(img, (int(r / t), int(l / t)))

    img_drawed = fd.draw_faces(img)
    font = cv2.FONT_HERSHEY_SIMPLEX
    faces, coordinates = fd.get_face_image(img)
    max_sim = 0; ii = 0; jj = 0
    for i in range(len(faces)):
        print coordinates[i]
        img = faces[i]
        img = cv2.resize(img, (256, 256))
        img = img / 255
        img = np.expand_dims(img, axis=0)
        features[i] = model.predict(img)
        features[i] = features[i].flatten().tolist()
        print features[i]
        print len(features[i])
        print "_____________________"
        for j in range(i):
            if i > j:
                # score = 1 - cosine(features[i], features[j])
                score = 1 - Chebyshev(features[i], features[j])
                print score, i, j
                if score >= max_sim:
                    max_sim = score; ii = i; jj = j
        # img_drawed = fd.draw_faces(img)
        score = predict_cv_img(faces[i])
       # cv2.putText(img_drawed, str(get_AQ(score[0][0])),
       #             coordinates[i], font, 0.8, (255, 150, 10), 2)
        cv2.putText(img_drawed, str(i + 1),
                    coordinates[i], font, 0.8, (255, 150, 10), 2)


    cv2.imwrite(save_path, img_drawed)
    if len(faces) == 1 : max_sim = 1.00
    elif len(faces) == 0 : max_sim = 0.00; ii = -1; jj = -1
    return max_sim, min(ii + 1, jj + 1), max(ii + 1, jj + 1)
    #fd.show(img_drawed)


if __name__ == '__main__':
    # print(get_AQ(3))
    main()
