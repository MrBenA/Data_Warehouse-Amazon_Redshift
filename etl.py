import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Executes SQL COPY queries to extracts event and log data from JSON files and loads to staging tables.
    """

    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
        print('Success, staging table loaded!')


def insert_tables(cur, conn):
    """
    Executes SQL INSERT queries to extract staging table data and inserts to fact and dimension tables.
    """

    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        print('Success, table insert complete!')


def main():
    """
    - Establishes connection with Redshift cluster and sparkify database and gets
        cursor to it.

    - Load staging table data from S3 json files.

    - Load data from staging tables to fact and dimension tables.

    - Finally, closes the connection.
    """

    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()