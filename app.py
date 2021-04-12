import re

from flask import Flask, render_template, request

from nhkdict import NHKDict

app = Flask(__name__)

nhk = NHKDict("data/nhk_dict.xml")


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
    pattern = re.compile(
        r'<img src="NetDicResID:Accent-ugi:(?P<unicode>[1234567890ABCDEF]*?):" style="height:1em;vertical-align:middle;border:none;" alt="�" data-txt-len="1" />'
    )
    html = re.sub(pattern, lambda x: chr(int(x.group("unicode"), 16)), html)
    return html


if __name__ == "__main__":
    app.run()
