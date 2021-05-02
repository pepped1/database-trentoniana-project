\c tren

SELECT title
FROM MAINVIEW
WHERE last_name = 'Klatzkin';

SELECT title
FROM MAINVIEW
WHERE city = 'Trenton';

SELECT mp3
FROM FILEVIEW;

SELECT title, month, day, year
FROM MAINVIEW
WHERE year > 1990;

SELECT acc_type
FROM PERMISSIONS
WHERE can_write = 'true';

SELECT *
FROM USERSVIEW;

UPDATE USERS
SET acc_type = 'admin'
WHERE email_address = 'pepped1@tcnj.edu';

INSERT INTO USERS
VALUES
('mcdonaghd1@tcnj.edu', 'superpassword', 'mcdonaghd1', 'user');

DELETE FROM USERS
WHERE email_address = 'degoodj@tcnj.edu';

SELECT *
FROM USERSVIEW;
