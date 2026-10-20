
from flask import Flask
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import nltk
import os

app = Flask("Sentiment Analyzer")

# Make the bundled VADER lexicon available inside the container.
lexicon_path = os.path.join(os.path.dirname(__file__), "sentiment", "vader_lexicon.zip")
nltk.data.path.append(os.path.dirname(lexicon_path))

sia = SentimentIntensityAnalyzer()

@app.get('/')
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment"

@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):
    scores = sia.polarity_scores(input_txt)
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])

    res = "positive"
    if neg > pos and neg > neu:
        res = "negative"
    elif neu > neg and neu > pos:
        res = "neutral"

    return json.dumps({"sentiment": res})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
