# Tinder Auto-Swipe

Tinder auto-swipe using k nearest neighbours on facial descriptors generated using dlib.

## Getting Started

### Prerequisites

You'll need a Python 3 environment with the following installed:

```
cv2
dlib
lxml
requests
robobrowser
```

### Collecting Data

Once you've cloned the github repo you'll need some data. I recommend first getting some likes by scraping insta posts of people you find attractive. You should look for posts with only one face in them. Insta post URLs are in this format:

```
https://www.instagram.com/p/{post_id}/
```

Put the `post_id` of posts you like in a file at the repository root called `insta_likes` and run:
```
python insta_scrape.py
```
This will create a folder called `like` full of profiles of people you find attractive. Run
```
python image_utils.py
```
to generate facial descriptors for these profiles (this might take a while).

 Next copy `fb_config_example.py` to `fb_config.py` and fill in the `fb_username` and `fb_password` variables with your Facebook credentials. Make sure not to commit this! Set

```
DEBUG_MODE = True
```
in `constants.py` and run
```
python auto_swipe.py
```
This will save likes and nopes in directories `like_swipe` and `nope_swipe` respectively but won't actually call the Tinder endpoint to swipe. This allows you to move the swipes (every file prefixed with the same hash) to the correct data directory (either `like` or `nope`). 

## Running Auto Swipe

Once you feel like you've collected enough data (you can tell when the things in `like_swipe` and `nope_swipe` start making sense), set
```
DEBUG_MODE = False
```
and run
```
python auto_swipe.py
```

### Spoofing your location

If you'd like to swipe in a different location, simply run
```
python auto_swipe.py {latitude} {longitude}
```
where `latitude` and `longitude` are the latitude and longitude of the location you'd like to swipe in. _Note that South and West are represented by negative numbers._

This works best if you close the app on your phone as it just repeatedly spams the ping endpoint the Tinder app calls to relay your phone's location. Actually changing your location would of course require a Pro account.

## Improving Performance

### On Good Data
The performance of algorithms like k-NN is only as good as your data: 
* Save profiles you feel strongly about (either really like or really dislike)
* Don't save profiles that have pictures of other people, emo/bit-mojis, memes with faces in them, etc.
* Try to keep your `like` and `nope` directories roughly the same size (`auto_swipe.py` will tell you how many descriptors it loads on start up)

### Correcting matches

Once you start getting matches you can improve your performance by recording them as either likes or swipes. First run
```
python print_matches.py
```
to get a list of your matches (this'll only report the ones you haven't messaged or sorted yet). If you want more info on a specific match you can run
```
python print_match.py {identifier}
```
where `identifier` is the name or id of the match. Run
```
python add_profile.py {is_like} {profile_id}
```
where `is_like` is a 0 for nope, a 1 for like, or a 2 if you want to keep the match but don't want to commit it to your data and `profile_id` is the match's profile id taken from the `print_matches.py` print out. When you've gone through all the matches in the print out run
```
python image_utils.py
```
to generate descriptors for the profiles.

This will add the matches to your data and you'll see either more or less of them.

### Raising or Lowering CPU Usage

By default you'll see

```
NUM_CORES = 4
```
in `constants.py`. Use this to change the number of processes used to generate face descriptors, making `auto_swipe.py` run faster or slower.

A value of 1 will only ever use one CPU core, while higher values will use more/all available cores for a CPU usage closer to 100%. Note that setting the value higher than the number of cores your machine has gets you diminishing returns.

### Experimenting with K

In my testing I found that a value of K = 5 was suitable, but you may want to try different values by changing 
```
K = 5
```
in `constants.py`. You can get an idea of what the value should be by running
```
python knn.py
```
This'll run KNN on your data for odd values of K from 1-27 and report the accuracy. Setting K to the most accurate value may improve your performance or may just be overfitting your data. 

## Built With

* [Tinder](https://github.com/fbessez/Tinder) - I grabbed the Facebook auth token code from here
* [Dlib](http://dlib.net/) - Facial recognition
* [Tinder API](https://gist.github.com/rtt/10403467#file-tinder-api-documentation-md) - This is where I originally got the Tinder endpoints from

## Contributing

Send me a pull request or fork it!

## Authors

* **relytb** - *Initial work* - [relytb](https://github.com/relytb)

## Acknowledgments

* Anyone whose code was used
* The Dlib folk
* Tinder for not locking their shit down
