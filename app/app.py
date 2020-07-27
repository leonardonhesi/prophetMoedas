from flask                             import Flask, render_template, jsonify
from flask_cors                        import CORS
from flask_socketio                    import SocketIO, emit
from data                              import get
import json

app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    emit('SOCKET_UPD',  {'data':'Conectado'})

@app.route('/', methods=['GET'])
def Homepage():
    return render_template('index.html')

@app.route('/dolar', methods=['GET'])
def dolarRoute():
    retorno = json.loads(get(Datafrom='dolar').to_json(orient='records'))
    return jsonify(retorno), 200
 
@app.route('/lme', methods=['GET'])
def lmeRoute():
    retorno = json.loads(get(Datafrom='lme').to_json(orient='records'))
    return jsonify(retorno), 200

@app.route('/geral', methods=['GET'])
def geralRoute():
    retorno = json.loads(get(Datafrom='geral').to_json(orient='records'))
    return jsonify(retorno), 200


if __name__=='__main__':
   socketio.run(app, host='0.0.0.0', debug=False)