from flask import Flask
import ex4 as util

app = Flask(__name__)

@app.route("/<category>", methods = ['POST'])
def index(category):
    json= util.findAndJsonParseMostTrendingWords(category)
    return json, {'Access-Control-Allow-Origin': '*'}

if __name__== "__main__":
    app.run(debug=True)