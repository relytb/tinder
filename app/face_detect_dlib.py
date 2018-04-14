import sys
import dlib
from skimage import io
import os
import cv2

if __name__ == '__main__':
    
    predictor_path = "shape_predictor_68_face_landmarks.dat"
    face_detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(predictor_path)

    extracted_dir = "../extracted"
    if not os.path.exists(extracted_dir):
        os.makedirs(extracted_dir)
    f = 0
    for root_path in ["../like", "../nope"]:
        for path in os.listdir(root_path):
            imgs = list(filter(lambda s: "jpg" in s, os.listdir(
                os.path.join(root_path, path))))
            for img in imgs:
                imagePath = os.path.join(root_path, path, img)
                # Read the image
                image = io.imread(imagePath)
                detected_faces = face_detector(image, 1)
                cv2image = cv2.imread(imagePath)
                img = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
                faces = dlib.full_object_detections()
                for face_rect in detected_faces:
                    faces.append(sp(img, face_rect))
                    image = dlib.get_face_chip(img, faces[0])
                    cv_bgr_img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                    x = face_rect.left()
                    y = face_rect.top()
                    w = face_rect.right() - x
                    h = face_rect.bottom() - y
                    sub_img=gray[y-10:y+h+10,x-10:x+w+10]
                    imgpath = os.path.join(extracted_dir, str(f) + ".jpg")
                    f += 1
                    print("Writing {}".format(imgpath))
                    cv2.imwrite(imgpath, cv_bgr_img)
                    if cv2.imread(imgpath) is None:
                        os.remove(imgpath)
