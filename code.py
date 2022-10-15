from celery import Celery
from time import sleep
print('run')
app = Celery('code1', broker='amqp://cqjouzla:ZXdWkGjatNhWVZC-KbAXvCeeOMdiHTHp@jaguar.rmq.cloudamqp.com/cqjouzla', backend='db+sqlite:///db.sqlite3')

@app.task
def hello():
    return 'hello world'