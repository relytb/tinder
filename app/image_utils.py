import sys
import dlib
import os
import cv2
import pickle
from django.conf import settings

predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

def pre_process_image(image_path, id, n):
    # Open image
    cv2_image = cv2.imread(image_path)

    # Detect faces
    detected_faces = detector(cv2_image, 1)
    print("{} - Detected {} face(s)".format(image_path, len(detected_faces)))

    if len(detected_faces) == 1:
        # Align face http://dlib.net/face_alignment.py.html
        full_object_detections = dlib.full_object_detections()
        for detected_face in detected_faces:
            full_object_detections.append(sp(cv2_image, detected_face))
        shape = full_object_detections[0]
        face_chip = dlib.get_face_chip(cv2_image, shape)

        print("{} - Generating descriptor".format(image_path))
        face_descriptor = facerec.compute_face_descriptor(cv2_image, shape, 100)

        # write to file
        print("{} - Writing pic".format(image_path))
        new_image_path = "{}_{}_processed.jpg".format(id, n)
        cv2.imwrite(os.path.join(os.path.dirname(image_path), new_image_path), face_chip)

        # save descriptor
        print("{} - Writing descriptor".format(image_path))
        descriptor_filename = "{}_{}_descriptor".format(id, n)
        f = open(os.path.join(os.path.dirname(image_path), descriptor_filename), "w+b")
        pickle.dump(face_descriptor, f)
        f.close()
    else:
        print("{} - Not exactly one face".format(image_path))
    
    f = open(os.path.join(os.path.dirname(image_path), "{}_{}_done".format(id, n)), "w")
    f.close()
    print("Done!")

def extract_id(image_path):
    return image_path.split("_")[0]

def extract_n(image_path):
    return image_path.split("_")[1].split(".")[0]

def run(img_dir):
    entries = os.listdir(img_dir)
    ids = set([extract_id(entry) for entry in entries])
    for id in ids: 
        profile_pics = [entry for entry in entries if ".jpg" in entry and id in entry]
        for pic in profile_pics:
            n = pic.split("_")[1].split(".")[0]
            if not "{}_{}_done".format(id, n) in entries:
                pre_process_image(os.path.join(os.path.abspath(img_dir), pic), id, n)


if __name__ == '__main__':
    
    # Test
    print("Pre-processing nopes")
    run("../nope")
    print("Pre-processing likes")
    run("../like")
    
