from flask import Flask
from quotes import Quote

app = Flask(__name__)


@app.route("/StartDefine", methods=['POST'])
def post_start_define():
    return Quote.PostStartDefine()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=49160, debug=True)
