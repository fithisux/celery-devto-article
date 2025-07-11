from flask import Flask, jsonify, g
from celery import Celery
from celery.result import AsyncResult
import time
import redis
import config_app


redis_server = redis.Redis(config_app.REDIS_HOST, config_app.REDIS_PORT)
redis_server.set('taskid_list', '')

app = Flask(__name__)

# Configure Celery
xxx = Celery(app.name, backend=config_app.CELERY_RESULT_BACKEND, broker=config_app.CELERY_BROKER_URL)

# Define a Celery task
@xxx.task
def say_hello():
    time.sleep(10)
    return "Hello, World!"


# API route to trigger the task
@app.route('/hello', methods=['GET'])
def trigger_task(trail=True):
    task = say_hello.delay()
    taskid_list_str = redis_server.get('taskid_list').decode('utf-8')
    taskid_list = taskid_list_str.split(";")
    taskid_list.append(task.id)
    redis_server.set('taskid_list', ";".join(taskid_list))
    print("append ", taskid_list)
    return jsonify({"task_id": task.id, "status": "Task has been submitted"}), 202

# API route to wait the task
@app.route('/hellowait/<task_id>', methods=['GET'])
def wait_on_task(task_id):
    some_result = AsyncResult(task_id, app=xxx)

    taskid_list_str = redis_server.get('taskid_list').decode('utf-8')
    taskid_list = taskid_list_str.split(";")
    print("scan ", taskid_list)
    if task_id not in taskid_list:
        return jsonify({"result": None, "exists": False}), 404

    if some_result.ready():
        result_data = some_result.get()
        some_result.forget()
        taskid_list.remove(task_id)
        redis_server.set('taskid_list', ";".join(taskid_list))
        print("forget ", taskid_list)
        return jsonify({"result": result_data, "exists": True}), 200
    else:
        print(some_result.state)
        return jsonify({"result": None, "exists": True}), 200

if __name__ == '__main__':
    app.run(debug=True)