# Set this to <= the number of cores your CPU has. More cores will process
# matches faster but will also significantly slow down your system.
NUM_CORES = 4

# This to determines the amount of sample matches the nearest neighbours
# algorithm will look at. Higher values may bring higher accuracy at the
# expense of longer processing times.
K = 5

# When you set it to 100 it gets 99.38% accuracy and executes the face 
# descriptor extraction 100 times on slightly modified versions of
# the face and returns the average result. This makes the call 100x slower.
# You could also pick a more middle value, such as 10, which is only 10x 
# slower but still gets an LFW accuracy of 99.3%. A value of 1 gets 99.13% 
# accuracy on LFW. http://dlib.net/face_recognition.py.html

DESCRIPTOR_ACCURACY = 100

# Directory constants
TEMP_DIR = 'tmp'
SAVED_LIKES_DIR = 'like_swipe'
SAVED_NOPES_DIR = 'nope_swipe'
SAMPLE_LIKES_DIR = 'like'
SAMPLE_NOPES_DIR = 'nope'
BURNED_DIR = 'burned'

# Set this to true to save swipes for triaging (doesn't actually swipe)
DEBUG_MODE = False