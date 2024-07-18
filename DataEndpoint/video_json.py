class VideoJSON:
    def __init__(self, title, tokenized_title, hashtags, comments, sentiment, date):
        self.title = title
        self.tokenized_title = tokenized_title
        self.hashtags = hashtags
        self.comments = comments
        self.sentiment = sentiment
        self.date = date

    def to_dict(self):
        date = self.date.strftime('%Y-%m-%d')

        return {
            "title": self.title,
            "tokenized_title": self.tokenized_title,
            "hashtags": self.hashtags,
            "comments": self.comments,
            "sentiment": self.sentiment,
            "date": date
        }