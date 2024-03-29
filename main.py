"""
Flask Application for Sentiment Analysis Web App
"""

from flask import Flask, request, jsonify, render_template
from bert_main import predict_all
from youtube_api import FetchData
import numpy as np
from utils import hamta_nyckel
from googleapiclient.errors import HttpError

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze sentiment of comments from a YouTube channel.

    Returns:
        json: Sentiment analysis results or error message.
    """
    nyckel = hamta_nyckel()

    # Retrieves JSON data sent with the POST request.
    data = request.get_json()
    # Extracts the value associated with the key 'channel_name' from the JSON data.
    channel_name = data.get('channel_name')

    # Fetching Comments from YouTube API
    try:
        # Creates an instance of the FetchData class to fetch comments
        # from the specified YouTube channel.
        api = FetchData(channel_name, nyckel)
        # Calls the method to fetch the comments from the latest video posted by
        # the channel.
        comments = api.get_latest_comments()
    except (HttpError, IndexError, ValueError) as e:
        # If an HttpError, IndexError, or ValueError occurs during the API call,
        # catch the exception. Store its string representation in the 'error'
        # variable.
        error = str(e)

        # Returns a JSON response with empty sentiment analysis results and
        # the error message.
        return jsonify({
            'negatives': '',
            'neutrals': '',
            'positives': '',
            'error': error,
        })

    # Handling No Comments
    if len(comments) == 0:
        # If no comments were retrieved from the channel, set the error message.
        error = """No comments could be retrived for this channel. 
        Please use another channel name"""
        # Returns a JSON response with empty sentiment analysis results and the error
        # message.
        return jsonify({
            'negatives': '',
            'neutrals': '',
            'positives': '',
            'error': error,
        })

    # Now we have handled all errors and can procced:
    # Processing Comments for Sentiment Analysis

    # Convert comments into a numpy array for processing.
    comments_array = np.array(comments)
    # Perform sentiment analysis on the comments.
    probas = predict_all(comments_array)
    # Convert sentiment probabilities to strings.
    negatives, neutrals, positives = map(str, probas)

    # Returns a JSON response with sentiment analysis results and an empty error
    # message.
    return jsonify({
        'negatives': negatives,
        'neutrals': neutrals,
        'positives': positives,
        'error': '',
    })


if __name__ == '__main__':
    app.run(debug=False)
