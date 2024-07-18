from fetch_trending_videos import FetchYoutubeData
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2 import sql

def main():
    youtube_data_fetcher = FetchYoutubeData()
    video_objects = youtube_data_fetcher.get_current_video_data()

    for video in video_objects:
        print(f"Title: {video.title}")
        print(f"Tokenized Title: {video.tokenized_title}")
        print(f"Hashtags: {video.hashtags}")
        print(f"Comments: {video.comments}")
        print(f"Sentiment: {video.sentiment}")
        print("---------")

    # insert_data(video_objects)

def insert_data(video_objs):
    load_dotenv()

    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    connection = psycopg2.connect(
        dbname=DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )

    cur = connection.cursor()

    for video in video_objs:
        cur.execute(sql.SQL("INSERT INTO videos (title, tokenized_title, hashtags, comments, sentiment, date) VALUES (%s, %s, %s, %s, %s, %s)"), [video.title, video.tokenized_title, video.hashtags, video.comments, video.sentiment, video.date])
    
    connection.commit()
    cur.close()
    connection.close()

if __name__ == "__main__":
    main()
