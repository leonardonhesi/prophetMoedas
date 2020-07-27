import time
from atualizaData                      import dolar, lme, geral
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler(daemon=True)
@sched.scheduled_job('interval', minutes=30)
def scheduledo():
    dolar()
    lme()
    geral()
    return False
sched.start()