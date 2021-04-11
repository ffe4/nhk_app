from flask import Flask, render_template, request

from nhk import lookup

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query')
    if query is not None:
        return render_template('index.html', query=lookup(query))
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
