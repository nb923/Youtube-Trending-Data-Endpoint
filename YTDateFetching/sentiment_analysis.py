from textblob import TextBlob

class CommentSentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments
    
    def comment_sentiment(self):
        average_sentiment_score = 0.0

        if not self.comments or len(self.comments) <= 0:
            return 0.0

        for comment in self.comments:
            result = TextBlob(comment)
            average_sentiment_score += result.sentiment.polarity

        average_sentiment_score = average_sentiment_score / len(self.comments)

        if average_sentiment_score > 0.1:
            return "Positive"
        elif average_sentiment_score < -0.1:
            return "Negative"
        else:
            return "Neutral"
            

    