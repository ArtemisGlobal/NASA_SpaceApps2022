# NASA_SpaceApps2022
NASA Space Apps Challenge 2022
Team Artemis [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project]( https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/teams/team-artemis-2/project) in Washington D.C.

Our challenge topic is Turning STEM into STEAM [https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details]( https://2022.spaceappschallenge.org/challenges/2022-challenges/steam/details). We chose different images collected by James Webb Space Telescope, and transformed them into music. We also set up a web application to let user interact with our program. Specifically, the user can upload a custom audio and choose a image, we transform the image into sound and match with the audio that the user provided to create new style music. This Github repo mainly shows the core algorithm that we do load audio file, extract keys, load image, convert to audio with musical inverse spectrogram technique, and sonification.







This will provide a backend API for the spaceapps challenge based on Flask.

API
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

### `/meidas`
- GET - Will return all of the media information.

### `/medias/add`
- POST - Will add a new media, JSON and Form posts are also allowed here.

### `/users`
- GET - If authenticated user has a role of `mission control` it will return a listing of all names in the database. If the user is anything else it will return only the user's first and last name.

### `/logout`
- GET - Log out of the current user and purge the session.






Examples Using CURL
Curl is a common command line utility that is used for interacting with URLs.

Logging in
curl http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/login -F 'username=DaveB' -F 'password=1523#' --cookie cookies.txt --cookie-jar newcookies.txt This generates a file called newcookies.txt that will contain the cookie that is needed to interact with the API for the user DaveB.

You can also visit http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/login in the browser and use the logins below to have the browser maintain your cookies.

Getting Data
For this example we will look at getting the medias out of the server. This can be done by logging in and going to http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/meidas in your browser or using CURL:

$ curl http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/meidas --cookie newcookies.txt
[
  {
    "audioref": "",
    "imageref": "Im123",
    "mediaID": 1,
    "videoref": ""
  },
  {
    "audioref": "Aud123",
    "imageref": "",
    "mediaID": 2,
    "videoref": ""
  },
  {
    "audioref": "",
    "imageref": "",
    "mediaID": 3,
    "videoref": "Vid123"
  }
]
Logging Out
Logging out is easy, it will invalidate the session associated with that cookie. To do so, visit http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/logout in your browser or use curl:

$ curl http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/logout --cookie newcookies.txt
This will invalidate the session on the server and the cookie in the file can be deleted.

Adding Data
The easiest way to upload data is through the browser by filling out the forms at http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/logs/add and http://ec2-18-221-105-205.us-east-2.compute.amazonaws.com:5000/medias/add. These can also be achieved with CURL by using CURL -X POST and making a JSON object that contains the appropriate information.

Current Active Test Users
username	password	firstname	lastname	company	role
ChrisN	1234!	Christine	Nolan	Hubbal Finacial	researcher
DaveB	1523#	Dave	Borncamp	Ball Corp.	mission control
RuthF	9875$	Ruth	Fantastic	Student	public
Installation Locally or on Server
MySQL needs to be installed and started. I followed this guide to get mysql installed and running on Ubuntu (Linux).

Once MySQL is installed, we need to install python 3.8.5. Install Python 3.8.10

The commands are:

sudo apt install python3-pip mysql-server python3.8-venv libmysqlclient-dev default-libmysqlclient-dev

sudo mysql_secure_installation
After Python is installed, install the Python packages using:

python3 -m venv hackathon 
source hackathon/bin/activate
pip install -r requirements.txt
Running
After things have been installed, the server can be started. We will need to export the name of the file to run.

EXPORT FLASK_APP=api
flask run --host=0.0.0.0
This will run the Flask API server on the machine, defaulting to port 5000.

