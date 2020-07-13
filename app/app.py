from flask                             import Flask, render_template, jsonify
from flask_cors                        import CORS
from flask_socketio                    import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
import time

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

def scheduledo():
    socketio.emit('SOCKET_UPD',  {'data': time.strftime("%A, %d. %B %Y %I:%M:%S %p")})
sched = BackgroundScheduler(daemon=True)
sched.add_job(scheduledo, "interval", minutes=1)
sched.start()

@app.route('/', methods=['GET'])
def Homepage():
    return render_template('index.html')

if __name__=='__main__':
   socketio.run(app, host='0.0.0.0')