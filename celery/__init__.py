from celery import Celery

app = Celery('argus_celery', 
    broker='amqp://localhost', 
    backend="amqp://localhost",
    include="arguswatch.celery.takss")

@app.task
def add(x, y):
    return x + y

if __name__ == '__main__':
    app.start()
