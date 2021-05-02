CREATE DATABASE tren;

\c tren

CREATE TABLE PARTICIPANTS (
	PID INT PRIMARY KEY,
	first_name varchar(12),
	middle_name varchar(12),
	last_name varchar(20)
);

INSERT INTO PARTICIPANTS
VALUES 
(1, 'Minerva', '', 'Rosenthal'), 
(2, 'Joe', '', 'Klatzkin'), 
(3, 'Ida', 'Mae', 'Klatzkin'), 
(4, 'Herman', '', 'Finkle');

CREATE TABLE PLACES (
	LID INT PRIMARY KEY,
	city varchar(12),
	state char(2)
);

INSERT INTO PLACES
VALUES 
(1, 'Trenton', 'NJ'), 
(2, 'Ewing', 'NJ'), 
(3, 'Easton','PA');

CREATE TABLE FILES (
	FID INT PRIMARY KEY,
	ogg text,
	afpk text,
	mp3 text
);

INSERT INTO FILES
VALUES 
(1, 'https://archive.org/download/JHS05SideA/JHS%2005-%20side%20A.ogg', 'https://archive.org/download/JHS05SideA/JHS%2005-%20side%20A.afpk', 'https://archive.org/download/JHS05SideA/JHS%2005-%20side%20A.mp3'),
(2, 'https://archive.org/download/JHS08SideA/JHS%2008-%20side%20A.ogg', 'https://archive.org/download/JHS08SideA/JHS%2008-%20side%20A.afpk', 'https://archive.org/download/JHS08SideA/JHS%2008-%20side%20A.mp3'), 
(3, 'https://archive.org/download/JHS10SideA/JHS%2010-%20side%20A.ogg', 'https://archive.org/download/JHS10SideA/JHS%2010-%20side%20A.afpk', 'https://archive.org/download/JHS10SideA/JHS%2010-%20side%20A.mp3');

CREATE TABLE ARCHIVES (
	title varchar(64) NOT NULL,
	month SMALLINT,
	day SMALLINT,
	year SMALLINT,
	transcript text,
	description text,
	keywords text,
	PID INT REFERENCES PARTICIPANTS,
	LID INT REFERENCES PLACES,
	FID INT REFERENCES FILES
);

INSERT INTO ARCHIVES
VALUES 
('Interview of Minerva Rosenthal', 10, 29, 1996, 'https://docs.google.com/document/d/1DBvjBLZMOSTMxjT2YVX7Nfe1Rrb0Ikf1_Ly4AzbLOiE/edit?usp=sharing', 'Minerva Bonen/Rosenthal interviewed. Mother Sarah Siet. Was a Trenton High School grad, involved in various community activities. Recalls a Rabbi Mosavich and many other Jewish figures from her youth. Worked as a saleswoman at the Benders store, in the sportswear department. Discussion of other Rosenthal family members, too.', 'Jewish, Oral History, Family History', 1, 1, 1), 
('Interview of Joe & Ida Klatzkin', 6, 8, 1988, 'https://docs.google.com/document/d/1rVwGMxUQ7rS_m0J8uH-aJNxqGsqUeNYuNbMyi2W6rzg/edit?usp=sharing', 'Ida Mae Klatzkin interviewed by her grandson (on the mothers side), who has a humorous demeanor. Born in Philadelphia as Ida Mae Smith. Her husband was her violin teachers son. Family came from Lithuania, her father came to the U.S. when he was 19, to Philadelphia. Her parents met later as her mother came to the U.S. later. Father Lewis Smith, mother Devera Esther Aronson. This is a family tape that delves into family history, also talking to Joe Klatzkin.', 'Jewish, Oral History, Family History', 3, 1, 2), 
('Interview of Herman "Humpsy" Finkle', 10, 16, 2003, 'https://docs.google.com/document/d/1eZYOcmHOgDkUVcXhVeTVjGaU9Nz4WYu5FvaioPKaP1o/edit?usp=sharing', 'Interviewed at his house. Most of the interview consists of miscellaneous reminiscences of "Jewtown" (the Jewish neighborhood in South Trenton) between the mid-1930s and 1940s. Recalls the YMHA (Young Mens Hebrew Association) on Stockton Street, and many businesses (including Herman Spiegel Furniture and a drugstore) near the intersection of Market and Lamberton Streets. At the beginning of WW2, worked at the GM Factory in Ewing Township. Later entered the service and visited Palestine before it became the State of Israel. Mentions one Benny (?) Olinsky as the keeper of Jewish history in Trenton.', 'Jewish, Oral History, YMHA', 4, 1, 3);

CREATE TABLE PERMISSIONS (
	acc_type varchar(8) PRIMARY KEY, 
	can_read varchar(6) NOT NULL, 
	can_write varchar(6) NOT NULL, 
	can_update varchar(6) NOT NULL, 
	can_delete varchar(6) NOT NULL, 
	all_access varchar(6) NOT NULL 
);

INSERT INTO PERMISSIONS 
VALUES 
('user', 'true', 'false', 'false', 'false', 'false'), 
('editor', 'true', 'true', 'true', 'false', 'false'), 
('admin', 'true', 'true', 'true', 'true', 'true');

CREATE TABLE USERS (
	email_address varchar(32) PRIMARY KEY,
	password varchar(16), 
	display_name varchar(16) UNIQUE, 
	acc_type varchar(8) REFERENCES PERMISSIONS
);

INSERT INTO USERS
VALUES 
('pepped1@tcnj.edu', 'password1', 'pepped1', 'user'), 
('poppera1@tcnj.edu', 'password2', 'poppera1', 'editor'), 
('hoffmans1@tcnj.edu', 'password3', 'hoffmans1', 'admin'), 
('degoodj@tcnj.edu', 'password4', 'degoodj', 'admin');

CREATE VIEW MAINVIEW AS
SELECT ARCHIVES.title, ARCHIVES.month, ARCHIVES.day, ARCHIVES.year, PARTICIPANTS.first_name, PARTICIPANTS.middle_name, PARTICIPANTS.last_name, PLACES.city, PLACES.state
FROM ARCHIVES 
JOIN PARTICIPANTS ON ARCHIVES.PID = PARTICIPANTS.PID
JOIN PLACES ON ARCHIVES.LID = PLACES.LID;

CREATE VIEW FILEVIEW AS
SELECT ARCHIVES.title, ARCHIVES.month, ARCHIVES.day, ARCHIVES.year, FILES.ogg, FILES.afpk, FILES.mp3
FROM ARCHIVES JOIN FILES ON ARCHIVES.FID = FILES.FID;

CREATE VIEW USERSVIEW AS
SELECT USERS.email_address, USERS.display_name, USERS.acc_type, PERMISSIONS.can_read, PERMISSIONS.can_write, PERMISSIONS.can_update, PERMISSIONS.can_delete, PERMISSIONS.all_access
FROM USERS JOIN PERMISSIONS ON USERS.acc_type = PERMISSIONS.acc_type;
