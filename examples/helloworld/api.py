from flask import Flask
from flask import abort
import random
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/sometimes/works")
def hello():
    if random.random() < 0.5;
        abort('404')
    return "OK"




if __name__ == "__main__":
    app.run()
