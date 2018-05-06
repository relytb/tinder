import pickle
import os
import math
from collections import OrderedDict

def knn(k, descriptor, likes, nopes):
    distances = {}
    for descriptor_path in nopes.keys():
        distance = euclidean_distance(nopes[descriptor_path], descriptor)
        print("Distance {} for nope {}".format(distance, descriptor_path))
        distances[descriptor_path] = distance
    
    for descriptor_path in likes.keys():
        distance = euclidean_distance(likes[descriptor_path], descriptor)
        print("Distance {} for like {}".format(distance, descriptor_path))
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

likes = load("../like")
nopes = load("../nope")

if __name__ == '__main__':
    print(len(likes))
    print(len(nopes))
    print(knn(5, list(likes.values())[10], likes, nopes))