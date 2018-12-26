import os
import pickle
import sys
from multiprocessing import Pool

import cv2
import dlib
from constants import SAMPLE_LIKES_DIR, SAMPLE_NOPES_DIR

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

def pre_process_image(args):
    image_path, pic_id, n, cur, total = args[0], args[1], args[2], args[3], args[4]
    tag = '[{} of {}] '.format(cur, total)
    # Open image
    cv2_image = cv2.imread(image_path)

    # Detect faces
    detected_faces = detector(cv2_image, 1)
    print(tag + '{} - Detected {} face(s)'.format(image_path, len(detected_faces)))

    if len(detected_faces) == 1:
        # Align face http://dlib.net/face_alignment.py.html
        full_object_detections = dlib.full_object_detections()
        for detected_face in detected_faces:
            full_object_detections.append(sp(cv2_image, detected_face))
        shape = full_object_detections[0]
        face_chip = dlib.get_face_chip(cv2_image, shape)

        print(tag + '{} - Generating descriptor'.format(image_path))
        face_descriptor = facerec.compute_face_descriptor(cv2_image, shape, 100)

        # write to file
        print(tag + '{} - Writing pic'.format(image_path))
        new_image_path = os.path.join(os.path.dirname(image_path), '{}_{}_processed.jpg'.format(pic_id, n))
        cv2.imwrite(new_image_path, face_chip)

        # save descriptor
        print(tag + '{} - Writing descriptor'.format(image_path))
        descriptor_path = os.path.join(os.path.dirname(image_path), '{}_{}_descriptor'.format(pic_id, n))
        f = open(descriptor_path, 'w+b')
        pickle.dump(face_descriptor, f)
        f.close()
    else:
        print(tag + '{} - Not exactly one face'.format(image_path))
    
    f = open(os.path.join(os.path.dirname(image_path), '{}_{}_done'.format(pic_id, n)), 'w')
    f.close()
    print(tag + 'Done!')

def extract_id(image_path):
    return image_path.split('_')[0]

def extract_n(image_path):
    return image_path.split('_')[1].split('.')[0]

def run(img_dir, pool):
    if os.path.exists(img_dir):
        entries = set(os.listdir(img_dir))
        to_process = []
        cur = 1
        for entry in entries:
            if '.jpg' in entry:
                pic_id = extract_id(entry)
                n = extract_n(entry)
                if '{}_{}_done'.format(pic_id, n) not in entries:
                    to_process.append([os.path.join(os.path.abspath(img_dir), entry), pic_id, n, cur, 0])
                    cur += 1

        total = len(to_process)
        for arg in to_process:
            arg[-1] = total
        pool.map(pre_process_image, to_process)


if __name__ == '__main__':
    pool = Pool(processes=4)
    print('Pre-processing likes')
    run(SAMPLE_LIKES_DIR, pool)
    print('Pre-processing nopes')
    run(SAMPLE_NOPES_DIR, pool)
    pool.close()
    pool.join()
