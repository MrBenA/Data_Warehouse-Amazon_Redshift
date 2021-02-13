import configparser

# READ CONFIG FILE, SET ROLE ARN
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE STAGING TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist VARCHAR(255),
        auth VARCHAR(255),
        firstName VARCHAR(255),
        gender VARCHAR(2),
        itemInSession INTEGER,
        lastName VARCHAR(255),
        length DOUBLE PRECISION,
        level VARCHAR(255),
        location VARCHAR(255),
        method VARCHAR(255),
        page VARCHAR(255),
        registration TIMESTAMP,
        sessionId INTEGER,
        song VARCHAR(255),
        status INTEGER,
        ts TIMESTAMP,
        userAgent VARCHAR(255),
        userId INTEGER
);
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs INTEGER,
        artist_id VARCHAR(255),
        artist_latitude DOUBLE PRECISION,
        artist_longitude DOUBLE PRECISION,
        artist_location VARCHAR(255),
        artist_name VARCHAR(255),
        song_id VARCHAR(255),
        title VARCHAR(255),
        duration DOUBLE PRECISION,
        year INTEGER
);
""")

# CREATE FACT TABLE

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INTEGER IDENTITY(0,1),
        start_time TIMESTAMP NOT NULL,
        user_id INTEGER NOT NULL,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id VARCHAR NOT NULL,
        location VARCHAR,
        user_agent VARCHAR
)
diststyle even;
""")

# CREATE DIMENSION TABLES

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        gender VARCHAR(255),
        level VARCHAR(255)
)
diststyle all;
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR(255) NOT NULL,
        title VARCHAR(255) NOT NULL,
        artist_id VARCHAR(255),
        year INTEGER,
        duration DOUBLE PRECISION
)
diststyle all;
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255),
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
)
diststyle all;
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP NOT NULL,
        hour INTEGER NOT NULL,
        day INTEGER NOT NULL,
        week INTEGER NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        weekday INTEGER NOT NULL
)
diststyle all;
""")

# LOAD DATA TO STAGING TABLES FROM S3 BUCKET

staging_events_copy = ("""
    COPY staging_events
    FROM 's3://udacity-dend/log_data/'
    iam_role {}
    json 'auto ignorecase'
    blanksasnull
    emptyasnull
    timeformat 'epochmillisecs';
""").format(ARN)

staging_songs_copy = ("""
    COPY staging_songs
    FROM 's3://udacity-dend/song_data/'
    iam_role {}
    json 'auto ignorecase'
    blanksasnull
    emptyasnull;
""").format(ARN)

# LOAD DATA FROM STAGING TABLES TO FINAL FACT & DIMENSION TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT se.ts        AS start_time,
    se.userid       AS user_id,
    se.level        AS level,
    ss.song_id      AS song_id,
    ss.artist_id    AS artist_id,
    se.sessionid    AS session_id,
    se.location     AS location,
    se.useragent    AS user_agent
FROM staging_events se
LEFT OUTER JOIN staging_songs ss ON (se.song = ss.title)
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT se.userid   AS user_id,
    se.firstname            AS first_name,
    se.lastname             AS last_name,
    se.gender               AS gender,
    se.level                AS level
FROM staging_events se
WHERE se.userid IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT ss.song_id  AS song_id,
    ss.title                AS title,
    ss.artist_id            AS artist_id,
    ss.year                 AS year,
    ss.duration             AS duration
FROM staging_songs ss;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT ss.artist_id    AS artist_id,
    ss.artist_name              AS name,
    ss.artist_location          AS location,
    ss.artist_latitude          AS latitude,
    ss.artist_longitude         AS longitude
FROM staging_songs ss;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT start_time                   AS start_time,
    EXTRACT (hour FROM start_time)      AS hour,
    EXTRACT (day FROM start_time)       AS day,
    EXTRACT (week FROM start_time)      AS week,
    EXTRACT (month FROM start_time)     AS month,
    EXTRACT (year FROM start_time)      AS year,
    EXTRACT (dayofweek FROM start_time) AS weekday
FROM songplays;
""")

# QUERY LISTS CALLED BY CREATE_TABLES & ETL PYTHON SCRIPTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
