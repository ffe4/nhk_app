import re
from io import BytesIO

from flask import Flask, render_template, request, abort, send_file

from nhkdict import NHKDict, NHKAudio

app = Flask(__name__)

nhk = NHKDict("data/nhk_dict.xml")
snd = NHKAudio("file:data/Accent-snd.db?mode=ro")


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("query")
    if query is not None:
        results = make_results(nhk.lookup(query))
        return render_template("index.html", query=query, results=results)
    return render_template("index.html")


def make_results(results):
    html = "\n".join([item.head + item.body for item in results])
    html = html.replace("NetDicResID:Accent-gi:speaker::", "/static/speaker.png")
    speaker_icon = re.compile(
        r'<img src="NetDicResID:Accent-ugi:(?P<unicode>[1234567890ABCDEF]*?):" style="height:1em;vertical-align:middle;border:none;" alt="�" data-txt-len="1" />'
    )
    html = re.sub(speaker_icon, lambda x: chr(int(x.group("unicode"), 16)), html)
    audio_link = re.compile(
        r'<a class="NetDicAudioLink" href="NetDicResID:Accent-snd:(?P<filename>\w*?):">'
    )
    html = re.sub(audio_link, lambda x: f'<audio controls src="snd/{x.group("filename")}"></audio>', html)
    return html


@app.route("/snd/<name>", methods=["GET"])
def audio(name):
    file = snd.get(name)
    if not file:
        abort(404)
    return send_file(
        BytesIO(file),
        mimetype='audio/mp3',
    )


if __name__ == "__main__":
    app.run()
