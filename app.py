# import necessary packages
from flask import Flask, request, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# initiate app
app = Flask(__name__)

# route to home page template
@app.route('/')
def home():
    return render_template('home.html')

# methods allowed are POST and GET- call is made when url is hit every time
@app.route('/', methods=['POST', 'GET'])
# function
def sentiment_analyzer_prediction():
    '''
    Function executes for POST calls. It takes data which is in forms from HTML and verifies for text_input which is sentence text area.
    Vader SentimentIntensityAnalyzer object is loaded into variable, then polarity scores methods is applied which gives all pos, neg, neu and compound scores
    of the sentence.
    :return: returns compound, negative, positive and neutral scores in HTML template.
    '''
    try:
        if request.method == "POST":

            request_data = request.form
            text = request_data['text_input']
            analyzer = SentimentIntensityAnalyzer()
            sentiment = analyzer.polarity_scores(text)
            # threshold kept as suggested by https://github.com/cjhutto/vaderSentiment team.
            # Tune values if you need another threshold to define sentence category
            if sentiment['compound'] >= 0.05:
                sentence_category = 'Positive'
            elif -0.05 <= sentiment['compound'] < 0.05:
                sentence_category = 'Neutral'
            else:
                sentence_category = 'Negative'
            return render_template('home.html', sentence=request_data['text_input'], category=sentence_category,
                                   compound=str(sentiment['compound']), positive=str(sentiment['pos'] * 10),
                                   negative=str(sentiment['neg'] * 10), neutral=str(sentiment['neu'] * 10))
    # catch exceptions and display to end user in case of any errors
    except Exception as e:
        return render_template('home.html', error=e)


if __name__ == '__main__':
    app.run()
