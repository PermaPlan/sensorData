from flask import Flask
print("YEEEEEEAAAAAAHHHH!")


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def test():
    return "Yeah this works"


app.run(debug=True, host="0.0.0.0")
