import extract
import transform
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

if __name__ == "__main__":

#Importing the songs_df from the extract.py
    load_df=extract.return_dataframe('BQB8a_WFj8f3qSuH2-HtauapmhccC5v9gH_w56Em4h-7XnmuYgTkV_uJYCrBNA89i34xypXhAaeQT_sL6PAIEPM1qfESRgLrpfCz4t1ZzqvpXiiZxM7eY_DbwlHF93njL4I3mVM8upYZob5Wwt2z6n28VCUrFJWJU9TRlYVvrkCz6dNCHA1kmtbzfHl_xHBKTXwaPu7LdkHyobYMVLei1EaKEXR9kg')
    if(transform.Data_Quality(load_df) == False):
        raise ("Failed at Data Validation")
    Transformed_df=transform.Transform_df(load_df)
    #The Two Data Frame that need to be Loaded in to the DataBase

#Loading into Database
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    #SQL Query to Create Played Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """
    #SQL Query to Create Most Listened Artist
    sql_query_2 = """
    CREATE TABLE IF NOT EXISTS fav_artist(
        timestamp VARCHAR(200),
        ID VARCHAR(200),
        artist_name VARCHAR(200),
        count VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
    )
    """
    cursor.execute(sql_query_1)
    cursor.execute(sql_query_2)
    print("Opened database successfully")

    #We need to only Append New Data to avoid duplicates
    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    try:
        Transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database2")

    #cursor.execute('DROP TABLE my_played_tracks')
    #cursor.execute('DROP TABLE fav_artist')

    conn.close()
    print("Close database successfully")