# Project: AWS Redshift Data Warehouse

## Project overview
Sparkify offers a music streaming service through desktop and hand-held devices.<br>
The streaming startup has grown their user base and song database and want to move their processes<br>
and data onto the cloud. Their data resides in Amazon S3, as a directory of JSON logs on user activity on the app, as well as<br>
a directory with JSON metadata for the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3,<br>
stages it in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue<br>
finding insights in what songs their users are listening to.

### Repository

#### Files to run project...
- [ **create_tables.py** ] (*Python 3 script*):<br>
  Connects to Redshift cluster and creates database staging, fact and dimension tables as per queries from<br>
  the *sql_queries.py* python file.
  
  

- [ **etl.py** ] (*Python 3 script*):<br>
  2 stage data processing script; 1) Loads data from S3 hosted JSON files to staging tables. 2) Loads data to fact and<br>
  dimension tables from the staging tables.
  
  

- [ **sql_queries.py** ] (*Python 3 script*):<br>
  CREATE, COPY and INSERT SQL statements used by etl.py
  
  

- [ **dwh.cfg** ] (*config text file*):<br>
  Contains user AWS credentials, S3 bucket paths, cluster details, all utilised by project Python scripts.



### Running the project
1. Download project Python scripts and config file, as listed above, to a local directory.
2. Launch a redshift cluster and create an IAM role that has read access to S3.
3. Add AWS credentials, cluster endpoint, database and IAM role details to dwh.cfg.
4. Open your system CLI and change directory to where the project files are saved.<br>
   
        C:\users\username>cd C:\users\username\path\to\project
   
5. Run first Python script to create table schema on Redshift cluster... *create_tables.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 create_tables.py

6. Run second python script to process S3 hosted JSON files to staging tables and final star schema tables... *etl.py*;<br>

        C:\users\username>cd C:\users\username\path\to\project>python3 etl.py 

---
## Dataset
2No. datasets are available for ingest to the Redshift Sparkify data warehouse, required to carry out relevant<br>
song play data analysis.

    Song data: s3://udacity-dend/song_data
    Log data: s3://udacity-dend/log_data

### Song data
Song data resides in JSON format, with each file containing metadata about a specific song, and the song's artist.<br>
Within Sparkify's file storage, song files are partitioned by the first three letters of each song's track ID.

Filepath example...

    song_data/A/B/C/TRABCEI128F424C983.json
    song_data/A/A/B/TRAABJL12903CDCF1A.json

TRAABJL12903CDCF1A.json song file content...

    {
    "num_songs": 1,
    "artist_id": "ARJIE2Y1187B994AB7",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "",
    "artist_name": "Line Renaud",
    "song_id": "SOUPIRU12A6D4FA1E1",
    "title": "Der Kleine Dompfaff",
    "duration": 152.92036,
    "year": 0
    }

###  Log data
User activity logs, collected via the Sparkify music streaming applications, also resides in JSON format.<br>
Each file represents a single day and contains information about each user and their session details for that day.
Within Sparkify's file storage, log files are partitioned by the month and year.

    log_data/2018/11/2018-11-12-events.json
    log_data/2018/11/2018-11-13-events.json

2018-11-12-events.json log file content...

    {
    "artist":null,
    "auth":"Logged In",
    "firstName":"Celeste",
    "gender":"F",
    "itemInSession":0,
    "lastName":"Williams",
    "length":null,
    "level":"free",
    "location":"Klamath Falls, OR",
    "method":"GET",
    "page":"Home",
    "registration":1541077528796.0,
    "sessionId":438,
    "song":null,
    "status":200,
    "ts":1541990217796,
    "userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64)<br>
                AppleWebKit\/537.36 (KHTML, like Gecko)<br>
                Chrome\/37.0.2062.103 Safari\/537.36\"",
    "userId":"53"
    }

---

### Table summary

**Table Name**  | **Description**
--------------- | ---------------
**staging_events** | Staging Table; Full data extraction from JSON event log files.
**staging_songs** | Staging Table; Full data extraction from JSON song files.
**songplays** | Fact Table;  Log data associated with song plays, filtered by user action 'Next Song'.
**users** | Dimension Table; Registered application users
**songs** | Dimension Table; Songs in music database
**artists** | Dimension Table; Artists in music database
**time** | Dimension Table; Timestamps of **songplays** records, broken down into specific units

## Table Schema and samples

### Table: songplays
Cluster distribution: Even<br>

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**songplay_id**  | SERIAL | NOT NULL
**start_time** | TIMESTAMP | NOT NULL
**user_id** | VARCHAR | NOT NULL
**level** | VARCHAR | NOT NULL
**song_id** | VARCHAR |
**artist_id** | VARCHAR |
**session_id** | INT | NOT NULL
**location** | VARCHAR |
**user_agent** | VARCHAR |

Sample...

**songplay_id** | **start_time** | **user_id** | **level** | **song_id** | **artist_id** | **session_id** | **location** | **user_agent**
----------- | ---------- | ------- | ----- | ------- | --------- | ---------- | -------- | ----------
5449 | 2018-11-21 21:56:47.796000 | 15 | paid | SOZCTXZ12AB0182364 | AR5KOSW1187FB35FF4 | 818 | Chicago-Naperville-Elgin, IL-IN-WI | "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36"

........................................................................................................................

### Table: users
Cluster distribution: All<br>

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**user_id**  | INT | NOT NULL
**first_name** | VARCHAR | NOT NULL
**last_name** | VARCHAR | NOT NULL
**gender** | VARCHAR |
**level** | VARCHAR |

Sample...

**user_id** | **first_name** | **last_name** | **gender** | **level**
------- | ---------- | --------- | ------ | -----
15      | Lily       | Koch      | F      | paid

........................................................................................................................

### Table: songs
Cluster distribution: All<br>

**Column name** | **Data type** | **Column description**
----------- | --------- | ------------------
**song_id**  | VARCHAR | NOT NULL
**title** | VARCHAR | NOT NULL
**artist_id** | VARCHAR |
**year** | VARCHAR |
**duration** | FLOAT |

Sample...

**song_id** | **title** | **artist_id** | **year** | **duration**
----------- | -------------- | ------------- | ---------- | ---------
SOZCTXZ12AB0182364 | Setanta matins | AR5KOSW1187FB35FF4 | 0 | 269.58322

........................................................................................................................

### Table: artists
Cluster distribution: All<br>

**Column name** | **Data type** | **Column description**
--------------- | ------------- | ----------------------
**artist_id**  | VARCHAR | NOT NULL
**name** | VARCHAR | NOT NULL
**location** | VARCHAR |
**latitude** | VARCHAR |
**longitude** | VARCHAR |

Sample...

**artist_id** | **name** | **location** | **latitude** | **longitude**
------------- | -------- | ------------ | ------------ | -------------
AR5KOSW1187FB35FF4 | Elena | Dubai UAE | 49.80388 | 15.47491

........................................................................................................................

### Table: time
Cluster distribution: All<br>

**Column name** | **Data type** | **Column description**
--------------- | ------------- | ----------------------
**start_time**  | TIMESTAMP | NOT NULL
**hour** | INT | NOT NULL
**day** | INT | NOT NULL
**week** | INT | NOT NULL
**month** | INT | NOT NULL
**year** | INT | NOT NULL
**weekday** | INT | NOT NULL

Sample...

**start_time** | **hour** | **day** | **week** | **month** | **year** | **weekday**
-------------- | -------- | ------- | -------- | --------- | -------- | -----------
2018-11-21 21:56:47.796000 | 21 | 21 | 47 | 11 | 2018 | 2

........................................................................................................................