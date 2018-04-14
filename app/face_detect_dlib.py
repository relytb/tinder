import sys
import dlib
import os
import cv2

predictor_path = "shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)

def pre_process_image(image_path, new_image_path):
    # Open image
    cv2_image = cv2.imread(image_path)
    cv2_image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    # Detect faces
    detected_faces = detector(cv2_image_rgb, 1)

    if len(detected_faces) > 0:
        # Align face http://dlib.net/face_alignment.py.html
        full_object_detections = dlib.full_object_detections()
        for detected_face in detected_faces:
            full_object_detections.append(sp(cv2_image_rgb, detected_face))
        face_chip = dlib.get_face_chip(cv2_image_rgb, full_object_detections[0])

        # grayscale
        gray = cv2.cvtColor(face_chip, cv2.COLOR_BGR2GRAY)

        # write to file
        processed_image_path = os.path.join(extracted_dir, new_image_path)
        print("Writing for {}".format(image_path))
        cv2.imwrite(processed_image_path, gray)
    else:
        print("Failed to extract face for {}".format(image_path))


if __name__ == '__main__':
    
    extracted_dir = "../extracted"
    if not os.path.exists(extracted_dir):
        os.makedirs(extracted_dir)
    f = 0
    for root_path in ["../like", "../nope"]:
        for path in os.listdir(root_path):
            image_names = list(filter(lambda s: "jpg" in s, os.listdir(
                os.path.join(root_path, path))))
            for image_name in image_names:
                image_path = os.path.join(root_path, path, image_name)
                pre_process_image(image_path, os.path.join(extracted_dir, "{}.jpg".format(f)))
                f += 1
