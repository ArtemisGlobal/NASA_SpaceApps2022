# NASA_SpaceApps2022


NASA Space Apps Challenge 2022


Team Artemis [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project]( 


https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project) in Washington D.C.

## Overview
Our challenge topic is Turning STEM into STEAM [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details]( https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details). We chose different images collected by James Webb Space Telescope, and transformed them into music. We also set up a web application to let user interact with our program. Specifically, the user can upload a custom audio and choose a image, we transform the image into sound and match with the audio that the user provided to create new style music. This Github repo mainly shows the core algorithm that load an audio file, extracts the key and tempo, loads an image, and then converts it to audio with musical inverse spectrogram technique such that it can be combined with the original audio file. 

You can find the detailed code in this repo, especially in the `audio_match_sonification.ipynb` or `audio_match_sonification.py` files. Within these files you will choose the song name (an mp3 or wav file must be in `/songs`). You can also select the image from the catalog `WebbDemo.csv` by setting its index number. Running `/audio_match_sonification.py` will generate an audio file of the image sonification in `/sonification` and a mix of the sonification and original audio in `/mixes`. 








## Requirements

Python 3.7+ is required.  

We recommend [Anaconda](https://www.continuum.io/downloads/) which comes with a suite of packages useful for scientific data analysis. Step-by-step instructions for installing Anaconda can be found at: [Windows](https://docs.anaconda.com/anaconda/install/windows/), [macOS](https://docs.anaconda.com/anaconda/install/mac-os/), [Linux](https://docs.anaconda.com/anaconda/install/linux/)

## Installation

### Setup your Virtual Environment
To avoid potential dependency issues with other Python packages, we suggest creating a virtual environment for this project; you can create a virtual environment in your terminal with:

```bash
python -m venv Hackathon
```

To enter your virtual environment, run the 'activate' script:

#### Windows

```bash
.\Hackathon\Scripts\activate
```

#### macOS and Linux

```bash
source Hackathon/bin/activate
```


After Python is installed, install the Python packages using:

```shell
python3 -m venv hackathon 
source hackathon/bin/activate
pip install -r requirements.txt
```

## Create the Database
Since you have set up the environemnt, you could set up the database by running this line:

```bash
chmod +x ./bin/insta485db
./bin/insta485db create
```

This will create simple SQLite database to store images that used later.
And if you want to drop the database, you can type:

```bash
./bin/insta485db destroy
```



## API
The server is currently deployed on an AWS EC2 instance, its address is http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/. The API uses sessions to keep track of current users and securely authenticate cookies. In order to interact with the API you must be logged in, without logging in first you will be denied access. Since there are different levels of access, public, mission control, or researcher you must be authenticated to get the appropriate level of access.

Logging In
To log in go to the /login endpoint at http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/login. See Current Active Test Users for the username and password to use to test access

If you are logged in as a public profile, you may only retrieve data, you may not input any kind of data. If you are logged in as not public, you can upload meida and logs to the database as well as retrieve.

### `/login`
- GET - You can perform a get request ot login to the server. It will return a cookie to be used for all other sessions

### `/logs`
- GET - Will return all of the logs.

### `/logs/add`
- POST - Either POST JSON or a Form requests will add a new log to the database.

### `/uploadsAud`
- POST - Will allow the user to upload the custom audio.

### `/delete`
- POST - Will allow the user to delete the uploaded audio.

### `/select`
- GET - Will let the user to choose one image from the image list.

### `/result`
- GET - Will export the audio file to the user's local directory.

### `/users`
- GET - If authenticated user has a role of `mission control` it will return a listing of all names in the database. If the user is anything else it will return only the user's first and last name.

### `/logout`
- GET - Log out of the current user and purge the session.


## DATA AND RESOURCES:


WebbTelescope.org (Image Resources): A developing gallery of images featuring astronomical observations and informative science content around the Webb telescope (JWST) mission. (72 kB)



Webb Space Telescope data: https://webbtelescope.org/resource-gallery/images



The Mikulski Archive for Space Telescopes (MAST) Portal lets astronomers search space telescope data, spectra, images and publications. Missions include Hubble, Kepler, GALEX, IUE, FUSE and more with a focus on the optical, ultraviolet, and near-infrared parts of the spectrum. https://www.mast.stsci.edu



jackmcarthur/musical-key-finder: A python project that uses several standard/otherwise very common libraries to determine the key that a song (an .mp3) is in, i.e. F major or C# minor, with annotations and some examples.



Barbara A. Mikulski Archive for Space Telescopes (MAST) dataset


https://mast.stsci.edu/portal/Mashup/Clients/Mast/Portal.html




## TOOLS:

Jupyter Notebook


Python


MySQL


Figma


Wix


Canva


Musical-key-finder package: https://github.com/jackmcarthur/musical-key-finder


Wav file writer package: Think DSP: Digital Signal Processing in Python 1st Edition by Allen B. Downey


Other python libraries: librosa, PIL, pandas, lumpy, audiolazy, pydub, urllib

