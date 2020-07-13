from flask          import Flask, render_template, jsonify
from flask_cors     import CORS
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__, 
            static_url_path='',
            static_folder='templates',
            template_folder='templates'
            )
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
socketio = SocketIO(app)

@socketio.on('connect')
def test_connect():
    emit('SOCKET_UPD',  {'data':'Conectado'})

if (os.name != 'nt'):
   from flask_crontab import Crontab
   crontab = Crontab(app)
   @crontab.job(minute= "*/10", hour= "*", day= "*", month= "*", day_of_week= "*")
   def atualizaDados():
      emit('SOCKET_UPD',  {'data':'dadosAtualizados'})

@app.route('/', methods=['GET'])
def Homepage():
    return render_template('index.html')

if __name__=='__main__':
   # app.run()
   socketio.run(app, host='0.0.0.0')