import psycopg2
import csv

from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
    """
    CREATE TABLE PLACES (
	LID SERIAL PRIMARY KEY,
	city varchar(12),
	state char(2)
);
    """,
    """
    CREATE TABLE ARCHIVES (
	AID SERIAL PRIMARY KEY,
	title varchar(64) NOT NULL,
	interview_date DATE,
	transcript text,
	description text,
	sound_file text,
	LID INT REFERENCES PLACES (LID)
    );
    """,
    """
    CREATE TABLE PARTICIPANTS (
	AID INT NOT NULL REFERENCES ARCHIVES (AID) ON UPDATE CASCADE ON DELETE CASCADE,
	first_name varchar(12),
	middle_name varchar(12),
	last_name varchar(20)
    );
    """,
    """
    CREATE TABLE KEYWORDS (
        KID SERIAL PRIMARY KEY,
        word varchar(16) NOT NULL
    );
    """,
    """
    CREATE TABLE ARCHIVE_KEYWORD (
	AID INT REFERENCES ARCHIVES (AID) ON UPDATE CASCADE ON DELETE CASCADE,
	KID INT REFERENCES KEYWORDS (KID) ON UPDATE CASCADE ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE PERMISSIONS (
	acc_type varchar(8) PRIMARY KEY, 
	can_read BOOLEAN NOT NULL, 
	can_write BOOLEAN NOT NULL, 
	can_update BOOLEAN NOT NULL, 
	can_delete BOOLEAN NOT NULL, 
	all_access BOOLEAN NOT NULL 
    );
    """,
    """
    CREATE TABLE USERS (
	email_address varchar(32) NOT NULL PRIMARY KEY,
	password varchar(16) NOT NULL, 
	display_name varchar(16) NOT NULL UNIQUE, 
	acc_type varchar(8) NOT NULL REFERENCES PERMISSIONS (acc_type)
    );
    """
    )
    
    gen_view_commands = (
    """
    CREATE VIEW KEYVIEW AS
    SELECT ARCHIVES.AID, KEYWORDS.word
    FROM ARCHIVE_KEYWORD
    JOIN ARCHIVES ON ARCHIVE_KEYWORD.AID = ARCHIVES.AID
    JOIN KEYWORDS ON ARCHIVE_KEYWORD.KID = KEYWORDS.KID;
    """,
    """
    CREATE VIEW SEARCHVIEW AS
    SELECT ARCHIVES.AID, ARCHIVES.title, ARCHIVES.interview_date, PARTICIPANTS.first_name, PARTICIPANTS.middle_name, PARTICIPANTS.last_name, PLACES.city, PLACES.state, KEYVIEW.word
    FROM ARCHIVES 
    JOIN PARTICIPANTS ON ARCHIVES.AID = PARTICIPANTS.AID
    JOIN KEYVIEW ON ARCHIVES.AID = KEYVIEW.AID
    JOIN PLACES ON ARCHIVES.LID = PLACES.LID;
    """,
    """
    CREATE VIEW MAINVIEW AS
    SELECT SEARCHVIEW.*, ARCHIVES.transcript, ARCHIVES.description, ARCHIVES.sound_file
    FROM SEARCHVIEW
    JOIN ARCHIVES ON SEARCHVIEW.AID = ARCHIVES.AID;
    """,
    """
    CREATE VIEW USERSVIEW AS
    SELECT USERS.email_address, USERS.display_name, USERS.acc_type, PERMISSIONS.can_read, PERMISSIONS.can_write, PERMISSIONS.can_update, PERMISSIONS.can_delete, PERMISSIONS.all_access
    FROM USERS JOIN PERMISSIONS ON USERS.acc_type = PERMISSIONS.acc_type;
    """
    )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        
        # the loading in of the data comes from the csv files in the csv folder in the program. there is one csv file per entity.
        
        # load in places from csv
        with open('csv/places.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY PLACES FROM STDIN WITH (FORMAT CSV)""", f)
        
        # load in archive data from csv
        with open('csv/archives.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY ARCHIVES FROM STDIN WITH (FORMAT CSV)""", f)
        
        # load in participants from csv
        with open('csv/participants.csv', 'r') as f:
            next(f) # skip first line, first line is headers
            cur.copy_expert("""COPY PARTICIPANTS FROM STDIN WITH (FORMAT CSV)""", f)  
        
        # load in keywords from csv
        with open('csv/keywords.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY KEYWORDS FROM STDIN WITH (FORMAT CSV)""", f)
        
        # load in association for archives and keywords
        with open('csv/archive_keywords.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY ARCHIVE_KEYWORD FROM STDIN WITH (FORMAT CSV)""", f)
        
        with open('csv/permissions.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY PERMISSIONS FROM STDIN WITH (FORMAT CSV)""", f)
        
        # load in user data
        with open('csv/users.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY USERS FROM STDIN WITH (FORMAT CSV)""", f)
        
        # create views after data is populated
        for command in gen_view_commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
