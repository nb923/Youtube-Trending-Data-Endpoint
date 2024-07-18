from video_json import VideoJSON
from fastapi import FastAPI, HTTPException
import os
from dotenv import load_dotenv
import psycopg2
from datetime import date
from typing import List, dict

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

api = FastAPI()

def get_from_date(date):
    connection = psycopg2.connect(
        dbname = DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )

    cur = connection.cursor()

    cur.execute("SELECT title, tokenized_title, hashtags, comments, sentiment, date FROM videos WHERE date = %s", (date))
    data = cur.fetchall()

    cur.close()
    connection.close()

    if not data:
        raise HTTPException(status_code=404, detail="No Videos Apply To The Query")

    videos = []

    for row in data:
        video = VideoJSON(*row)
        videos.append(video)

    return videos

def get_videos_by_keyword(keyword):
    connection = psycopg2.connect(
        dbname=DB_NAME,
        user = DB_USER,
        password = DB_PASSWORD,
        host = DB_HOST,
        port = DB_PORT
    )

    cur = connection.cursor()

    cur.execute("SELECT title, tokenized_title, hashtags, comments, sentiment, fetch_date FROM videos WHERE LOWER(title) LIKE %s OR LOWER(hashtags) LIKE %s", (date))
    data = cur.fetchall()

    cur.close()
    connection.close()

    if not data:
        raise HTTPException(status_code=404, detail="No Videos Apply To The Query")

    videos = []

    for row in data:
        video = VideoJSON(*row)
        videos.append(video)

    return videos

@api.get("/videos-by-date", response_model=List[dict])
def fetch_videos(date: date):
    info = get_from_date(date)
    list_of_videos = []

    for video in info:
        video = video.to_dict()
        list_of_videos.append(video)

    return list_of_videos

@api.get("/videos-by-keyword", response_model=List[dict])
def get_videos(keyword: str):
    info = get_from_date(date)
    list_of_videos = []

    for video in info:
        video = video.to_dict()
        list_of_videos.append(video)

    return list_of_videos
