import psycopg2
import csv

from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
    """
    CREATE TABLE PARTICIPANTS (
	PID INT PRIMARY KEY,
	first_name varchar(12),
	middle_name varchar(12),
	last_name varchar(20)
    );
    """,
    """
    CREATE TABLE PLACES (
    	LID INT PRIMARY KEY,
    	city varchar(12),
        state char(2)
    )
    """,
    """
    CREATE TABLE FILES (
        FID INT PRIMARY KEY,
        ogg text,
        afpk text,
        mp3 text
    )
    """,
    """
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
    """,
    """
    CREATE TABLE PERMISSIONS (
        acc_type varchar(8) PRIMARY KEY,
        can_read varchar(6) NOT NULL,
        can_write varchar(6) NOT NULL,
        can_update varchar(6) NOT NULL,
        can_delete varchar(6) NOT NULL,
        all_access varchar(6) NOT NULL
    )
    """,
    """
    CREATE TABLE USERS (
        email_address varchar(32) PRIMARY KEY,
        password varchar(16),
        display_name varchar(16) UNIQUE,
        acc_type varchar(8) REFERENCES PERMISSIONS
    )
    """,
    """
    CREATE VIEW MAINVIEW AS
    SELECT ARCHIVES.title, ARCHIVES.month, ARCHIVES.day, ARCHIVES.year, PARTICIPANTS.first_name, PARTICIPANTS.middle_name, PARTICIPANTS.last_name, PLACES.city, PLACES.state
    FROM ARCHIVES
    JOIN PARTICIPANTS ON ARCHIVES.PID = PARTICIPANTS.PID
    JOIN PLACES ON ARCHIVES.LID = PLACES.LID
    """,
    """
    CREATE VIEW FILEVIEW AS
    SELECT ARCHIVES.title, ARCHIVES.month, ARCHIVES.day, ARCHIVES.year, FILES.ogg, FILES.afpk, FILES.mp3
    FROM ARCHIVES JOIN FILES ON ARCHIVES.FID = FILES.FID
    """,
    """
    CREATE VIEW USERSVIEW AS
    SELECT USERS.email_address, USERS.display_name, USERS.acc_type, PERMISSIONS.can_read, PERMISSIONS.can_write, PERMISSIONS.can_update, PERMISSIONS.can_delete, PERMISSIONS.all_access
    FROM USERS JOIN PERMISSIONS ON USERS.acc_type = PERMISSIONS.acc_type
        
    """)
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
        # with open('permissions.csv', 'r') as f:
        #     next(f) # header row skipped
        #     cur.copy_from(f, 'PERMISSIONS', sep=',')
        # with open('csv/archives.csv', 'r') as f:
        #     next(f) # header row skipped
        #     cur.copy_expert(f, 'ARCHIVES', sep=',')
        with open('csv/participants.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY PARTICIPANTS FROM STDIN WITH (FORMAT CSV)""", f)  
        with open('csv/places.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY PLACES FROM STDIN WITH (FORMAT CSV)""", f)
        with open('csv/files.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY FILES FROM STDIN WITH (FORMAT CSV)""", f)
        with open('csv/archives.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY ARCHIVES FROM STDIN WITH (FORMAT CSV)""", f)
        with open('csv/permissions.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY PERMISSIONS FROM STDIN WITH (FORMAT CSV)""", f)
        with open('csv/users.csv', 'r') as f:
            next(f)
            cur.copy_expert("""COPY USERS FROM STDIN WITH (FORMAT CSV)""", f)
            
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