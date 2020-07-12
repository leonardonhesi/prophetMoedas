from flask      import Flask, render_template, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_url_path='/templates')
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/', methods=['GET'])
def Homepage():
    return app.send_static_file('index.html')

if __name__=='__main__':
   app.run()