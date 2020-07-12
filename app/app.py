from flask      import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def Homepage():
    return render_template('index.html')


if __name__=='__main__':
   app.run()