import time
from atualizaData                      import dolar, lme, geral
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
@sched.scheduled_job('interval', minutes=30)
def scheduledo():
    dolar()
    lme()
    geral()
    return False
sched.start()