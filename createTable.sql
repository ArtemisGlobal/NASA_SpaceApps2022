PRAGMA foreign_keys = ON; -- turn on foreign key support

CREATE TABLE images(
    imageID INTEGER PRIMARY KEY AUTOINCREMENT,  -- * like 1, 2, 3, ...
    ImageName VARCHAR(40) NOT NULL,
    FileDir VARCHAR(256) NOT NULL,
    CollectDate DATE,
    Instrument VARCHAR(20)
);

CREATE TABLE users(
  username VARCHAR(20) NOT NULL, -- if we use CHARACTER, the length will be constant
  email VARCHAR(40) NOT NULL,
  "password" VARCHAR(256) NOT NULL,
  imageID INTERGER NOT NULL,
  audioID INTEGER NOT NULL,
  PRIMARY KEY(username),
  FOREIGN KEY(imageID) REFERENCES images(imageID) ON DELETE CASCADE,
  FOREIGN KEY(audioID) REFERENCES audio(audioID) ON DELETE CASCADE
);



CREATE TABLE audio(
    audioID INTEGER PRIMARY KEY AUTOINCREMENT,
    audioName VARCHAR(40) NOT NULL
);

