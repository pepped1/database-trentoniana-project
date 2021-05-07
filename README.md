# Trentoniana Transcription & Database Implementation

TTDI was made possible by:
* Nina Brossa
* [Sarah Hoffman](https://github.com/seafoambeige)
* [Dean Peppe](https://github.com/pepped1)
* [Alyssa Popper](https://github.com/alyssapopper)

TTDI's goal was to make the Trentoniana Library's oral history archives more accessable with a better user interface, database, and transcription implementation

## Installation Guide
1. Install the following dependencies:
  * [PostgreSQL](https://www.postgresql.org/)
  * [Python 3](https://www.python.org/)
  * [Python library pip](https://pypi.org/project/pip/)
    * `sudo apt install python3-pip`
  * [Python library psycopg2](https://pypi.org/project/psycopg2/)
    * `pip3 install psycopg2-binary`
  * [Python library flask](https://flask.palletsprojects.com/en/1.1.x/)
    * `pip3 install flask`

2. Clone this repository to your local environment

4. Navigate into src/app_create_table/app

6. Run the command

  `python3 populate_from_csv.py`
  
7. Run the command

  `bash run.sh`
  
8. Then open your browser to 

  `http://127.0.0.1:5000/`
