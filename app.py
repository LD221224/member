from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    # return "Hello~ flask"


app.run(debug=True)
