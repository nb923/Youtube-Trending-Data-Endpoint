from fetch_trending_videos import FetchYoutubeData

def main():
    youtube_data_fetcher = FetchYoutubeData()
    video_objects = youtube_data_fetcher.get_current_video_data()

    return video_objects

if __name__ == "__main__":
    main()
