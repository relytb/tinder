# Set this to <= the number of cores your CPU has. More cores will process
# matches faster but will also significantly slow down your system.
NUM_CORES = 4

# This to determines the amount of sample matches the nearest neighbours
# algorithm will look at. Higher values may bring higher accuracy at the
# expense of longer processing times.
K = 5

# Directory constants
TEMP_DIR = 'tmp'
SAVED_LIKES_DIR = 'like_swipe'
SAVED_NOPES_DIR = 'nope_swipe'
SAMPLE_LIKES_DIR = '../like'
SAMPLE_NOPES_DIR = '../nope'
BURNED_DIR = '../burned'

# Set this to true to save swipes for triaging (doesn't actually swipe)
DEBUG_MODE = False