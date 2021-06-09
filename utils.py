from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from fpdf import FPDF
import textwrap
# from punctuator import Punctuator
import os
import requests

yt = YouTubeTranscriptApi()
formatter = TextFormatter()
# p = Punctuator('Demo-Europarl-EN.pcl')

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
            output = formatter.format_transcript(_get_url)
            text = punctuate_text(output)
            create_files(text)
            text_to_pdf(text, 'static/file.pdf')
        except Exception as e:
            print(e.with_traceback(e.__traceback__))
            return None
        # create files
    # return None
    return text


def punctuate_text(text):
    # output = p.punctuate(text)
    r = requests.post("http://bark.phon.ioc.ee/punctuator", data={
        'text': text
    })
    output = r.text
    
    return output

def create_files(text):
    with open("static/file.txt", 'w') as f:
        f.writelines(text)
    f.close()
    
def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 13
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_font("NotoSans", style="", fname="NotoSans-Regular.ttf", uni=True)
    pdf.add_font("NotoSans", style="B", fname="NotoSans-Bold.ttf", uni=True)
    pdf.add_font("NotoSans", style="I", fname="NotoSans-Italic.ttf", uni=True)
    pdf.add_font("NotoSans", style="BI", fname="NotoSans-BoldItalic.ttf", uni=True)
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='NotoSans', size=fontsize_pt)
    splitted = text.split('\n\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, 10, wrap, ln=1)

    pdf.output(filename, 'F')
