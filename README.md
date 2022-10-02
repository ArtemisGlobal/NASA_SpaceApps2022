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

/login
GET - You can perform a get request ot login to the server. It will return a cookie to be used for all other sessions

