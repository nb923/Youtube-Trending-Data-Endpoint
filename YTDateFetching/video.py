class Video:
    def __init__(self, title, tokenized_title, hashtags, comments, sentiment, date):
        self.title = title
        self.tokenized_title = tokenized_title
        self.hashtags = hashtags
        self.comments = comments
        self.sentiment = sentiment
        self.date = date