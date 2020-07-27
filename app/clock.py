import time
from atualizaData                      import dolar, lme, geral
from app                               import socketio
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon=True)
@sched.scheduled_job('interval', minutes=1)
def scheduledo():
    dolar()
    lme()
    geral()
    socketio.emit('SOCKET_UPD',  {'data': time.strftime("%A, %d. %B %Y %I:%M:%S %p")})
    return False
sched.start()