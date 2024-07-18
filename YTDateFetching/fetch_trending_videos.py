import requests
import re
import os
from nltk.corpus import stopwords
from dotenv import load_dotenv
from video import Video
from sentiment_analysis import CommentSentimentAnalysis
from datetime import datetime

class FetchYoutubeData:
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("MY_KEY")
        self.API_URL = 'https://www.googleapis.com/youtube/v3/videos'
        self.COMMENT_API_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
        self.STOP_WORDS = set(stopwords.words('english'))

    def get_trending_videos(self):
        parameters = {
            'part': 'snippet',
            'chart': 'mostPopular',
            'regionCode': 'US',
            'maxResults': 5,
            'key': self.API_KEY
        }
        
        response = requests.get(self.API_URL, params=parameters)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get trending videos: {response.status_code}")
            return None

    def get_comments(self, video_id):
        parameters = {
            'part': 'snippet',
            'videoId': video_id,
            'maxResults': 100,
            'key': self.API_KEY
        }

        response = requests.get(self.COMMENT_API_URL, params=parameters)

        if response.status_code == 200:
            comments_data = response.json().get('items', [])
            comments = []

            for item in comments_data:
                comments.append(item.get('snippet', {}).get('topLevelComment', {}).get('snippet', {}).get('textOriginal', ''))

            return comments
        else:
            print(f"Failed to get comments {video_id}: {response.status_code}")
            return []

    def get_hashtags(self, description):
        return re.findall(r"#(\w+)", description)

    def tokenize_title(self, title):
        tokens = re.findall(r'\b\w+\b', title.lower())
        token_list = []

        for token in tokens:
            if token not in self.STOP_WORDS:
                token_list.append(token)

        return token_list

    def get_current_video_data(self):
        response = self.get_trending_videos()
        
        if response:
            videos = response.get('items', [])
        else:
            videos = []

        video_list = []

        for video in videos:
            title = video['snippet']['title']
            description = video['snippet']['description']
            video_id = video['id']
            
            title_tokens = self.tokenize_title(title)
            hashtags = self.get_hashtags(description)
            comments = self.get_comments(video_id)

            sentiment_obj = CommentSentimentAnalysis(comments)

            sentiment_score = sentiment_obj.comment_sentiment()
            
            video_obj = Video(title, title_tokens, hashtags, comments, sentiment_score, datetime.now().date())
            video_list.append(video_obj)

        return video_list
