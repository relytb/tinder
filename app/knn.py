import pickle
import os
import math
from random import shuffle
from collections import OrderedDict
from image_utils import run

LIKES = {}
NOPES = {}


def setupDicts():
    likes = load("../like")
    likes_keys = list(likes.keys())
    shuffle(likes_keys)
    for k in likes_keys:
        LIKES[k] = likes[k]


    nopes = load("../nope")
    nopes_keys = list(nopes.keys())
    shuffle(nopes_keys)
    for k in nopes_keys:
        NOPES[k] = nopes[k]
        
    print('{} likes'.format(len(LIKES)))
    print('{} nopes'.format(len(NOPES)))



def knn(k, descriptor):
    return _knn(k, descriptor, LIKES, NOPES)

def _knn(k, descriptor, likes, nopes):
    distances = {}
    for descriptor_path in nopes.keys():
        distance = euclidean_distance(nopes[descriptor_path], descriptor)
        #print("Distance {} for nope {}".format(distance, descriptor_path))
        distances[descriptor_path] = distance
    
    for descriptor_path in likes.keys():
        distance = euclidean_distance(likes[descriptor_path], descriptor)
        #print("Distance {} for like {}".format(distance, descriptor_path))
        distances[descriptor_path] = distance
    
    distances = OrderedDict(sorted(distances.items(), key=lambda t: t[1]))

    like_count = 0
    i = 0
    for descriptor_path in list(distances.keys())[:k]:
        swipe = "nope"
        if descriptor_path in likes.keys():
            swipe = "like"
            like_count += 1
        print("{}th descriptor: {} is a {} with distance {}".format(i, descriptor_path, swipe, distances[descriptor_path]))
        print("Check it out here: {}".format(os.path.abspath(os.path.join("../{}".format(swipe), "_".join(descriptor_path.split("_")[:-1]) + ".jpg"))))
        i += 1
    print("{} likes out of {}".format(like_count, k))
    return round(like_count/k)   

def euclidean_distance(descriptor1, descriptor2):
    terms = []
    for i in range(len(descriptor1)):
        terms.append((descriptor1[i] - descriptor2[i]) ** 2)
    return math.sqrt(sum(terms))
  
def load(img_dir):
    vectors = {}
    entries = os.listdir(img_dir)
    descriptor_paths = [entry for entry in entries if "descriptor" in entry]
    for descriptor_path in descriptor_paths:
        vectors[descriptor_path] = pickle.load(open(os.path.join(img_dir, descriptor_path), "rb"))
    return vectors

setupDicts()

if __name__ == '__main__':
    likes = load("../like")
    nopes = load("../nope")
    print(len(likes))
    print(len(nopes))
    likes_keys = list(likes.keys())
    shuffle(likes_keys)
    divider = int((len(likes_keys)/10)*8)
    likes_training_keys = likes_keys[:divider]
    likes_test_keys = likes_keys[divider:]

    nopes_keys = list(nopes.keys())
    shuffle(nopes_keys)
    divider = int((len(nopes_keys)/10)*8)
    nopes_training_keys = nopes_keys[:len(likes_training_keys)]
    nopes_test_keys = nopes_keys[len(likes_training_keys):len(likes_training_keys) + len(likes_test_keys)]

    print("{} in likes train set, {} in likes test set, {} in nopes train set, {} in nopes test set".format(
        len(likes_training_keys), len(likes_test_keys), len(nopes_training_keys), len(nopes_test_keys)))

    test = likes_test_keys + nopes_test_keys

    nopes_training_dict = {}
    for k in nopes_training_keys:
        nopes_training_dict[k] = nopes[k]
    
    likes_training_dict = {}
    for k in likes_training_keys:
        likes_training_dict[k] = likes[k]
    for k in range(1, 27, 2):
        like_but_swiped_left = 0
        nope_but_swiped_right = 0
        for i in range(len(test)):
            value = likes[test[i]] if test[i] in likes.keys() else nopes[test[i]]
            result = _knn(k, value, likes_training_dict, nopes_training_dict)

            is_nope = test[i] in nopes.keys()
            if (result == 0 and not is_nope):
                like_but_swiped_left += 1
            if (result == 1 and is_nope):
                nope_but_swiped_right += 1
            print("                                                                           ", end="\r")
            print("{} way done for k={}".format(i/len(test), k), end="\r")
        print("Accuracy: {}%, {}% swiped left on likes, {}% swiped right on nopes for k={}".format(round(((len(test) - like_but_swiped_left - nope_but_swiped_right)/len(test))*100), 
        (like_but_swiped_left/len(likes_test_keys))*100, (nope_but_swiped_right/len(nopes_test_keys))*100,  k))