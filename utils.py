from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from fpdf import FPDF
import os

yt = YouTubeTranscriptApi()
formatter = TextFormatter()
pdf = FPDF()
pdf.add_page()   
pdf.set_font("Arial", size = 15)


# noinspection PyTypeChecker
def extract_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?==
    return None


def get_transcript_from_url(url):
    url_id = extract_video_id(url)
    # print(url_id)
    text = None

    if url_id is not None:
        try:
            _get_url = yt.get_transcript(url_id)
            text = formatter.format_transcript(_get_url)
            create_files(text)
        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            return None
        # create files
    # return None
    return text


def create_files(text):
    with open("static/file.txt", 'w') as f:
        f.writelines(text)
    
    with open("file.txt", 'r') as f:
        for x in f:
            pdf.cell(200, 10, txt = x, ln = 1, align = 'C')
        pdf.output("static/file.pdf")
