from flask import Flask, request, jsonify, render_template
from utils import get_transcript_from_url
import os

app = Flask(__name__)

# url = "https://youtube.com/watch?v=ePj9P3pJkJ0"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_text/', methods=['POST',])
def get_text():
    url = request.json["text"]

    x = get_transcript_from_url(url)
    resp = None
    if x is not None:
        # print(x)
        resp = {
            'data' : "Subtitles found!",
            'status' : 'ok'
        }
    else:
        resp = {
            'data' : 'Error occured.',
            'status' : 'error'
        }
    return jsonify(resp)

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 33507))
    app.run(debug=True)

