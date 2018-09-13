from flask import Flask, request, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def sentiment_analyzer_prediction():
    if request.method == "POST":

        request_data = request.form
        text = request_data['text_input']
        analyzer = SentimentIntensityAnalyzer()
        sentiment = analyzer.polarity_scores(text)
        if sentiment['compound'] >= 0.05:
            sentence_category = 'Positive'
        elif -0.05 <= sentiment['compound'] < 0.05:
            sentence_category = 'Neutral'
        else:
            sentence_category = 'Negative'
        return render_template('home.html', sentence=request_data['text_input'], category=sentence_category,
                               compound=str(sentiment['compound']), positive=str(sentiment['pos'] * 10),
                               negative=str(sentiment['neg'] * 10), neutral=str(sentiment['neu'] * 10))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
