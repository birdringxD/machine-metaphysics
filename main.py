import cv2
import sys
import predict
import face_detection as fd
import numpy as np
import math
from scipy.spatial.distance import cosine

sys.argv[0] = 'girls.jpg'

features = [[],[],[],[],[],[],[],[],[],[]]

def Chebyshev(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return max(np.abs(npvec1-npvec2))

if __name__ == '__main__':
    max_sim = 0
    for i in sys.argv:
        if i.find('.jpg') != -1:
            img = cv2.imread(i)
            l = img.shape[0]
            r = img.shape[1]
            print l, r
            if l >= 1000: t = (l * 1.0) / 1000
            elif l <= 500 : t = (l * 1.0) / 500
            else : t = 1

            if l > r : img = cv2.resize(img, (int(r / t), int(l / t)))
            elif l == r : img = cv2.resize(img, (800, 800))
            else : img = cv2.resize(img, (int(r / t), int(l / t)))

            img_drawed = fd.draw_faces(img)
            font = cv2.FONT_HERSHEY_SIMPLEX
            faces, coordinates = fd.get_face_image(img)
            for i in range(len(faces)):
                print coordinates[i]
                img = faces[i]
                img = cv2.resize(img, (256, 256))
                img = img / 255
                img = np.expand_dims(img, axis=0)
                features[i] = predict.model.predict(img)
                features[i] = features[i].flatten().tolist()
                #print features[i]
                print len(features[i])
                print "_____________________"

                for j in range(i) :
                    if i > j :
                        # score = 1 - cosine(features[i], features[j])
                        score = 1 - Chebyshev(features[i], features[j])
                        print score, i, j
                        if score >= max_sim :
                            max_sim = score
                            ii = i
                            jj = j
                # img_drawed = fd.draw_faces(img)
                score = predict.predict_cv_img(faces[i])
                cv2.putText(img_drawed, str(predict.get_AQ(score[0][0])),
                            coordinates[i], font, 0.8, (255, 150, 10), 2)

            print max_sim, ii + 1, jj + 1
            fd.show(img_drawed)


