from celery import Celery

app = Celery('tasks', broker='redis://celery_broker:6379')


@app.task
def save_message_to_db(pydantic_message):
    print(pydantic_message)
