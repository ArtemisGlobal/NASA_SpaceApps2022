# NASA_SpaceApps2022


NASA Space Apps Challenge 2022


Team Artemis [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project]( 


https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project) in Washington D.C.


Our challenge topic is Turning STEM into STEAM [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details]( https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details). We chose different images collected by James Webb Space Telescope, and transformed them into music. We also set up a web application to let user interact with our program. Specifically, the user can upload a custom audio and choose a image, we transform the image into sound and match with the audio that the user provided to create new style music. This Github repo mainly shows the core algorithm that we do load audio file, extract keys, load image, convert to audio with musical inverse spectrogram technique, and sonification.







### API
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




## Installation Locally or on Server

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

## Running

After things have been installed, the server can be started.
We will need to export the name of the file to run.

```shell
EXPORT FLASK_APP=api
flask run --host=0.0.0.0
```

This will run the Flask API server on the machine, defaulting to port 5000.
