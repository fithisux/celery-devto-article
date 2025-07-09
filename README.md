## The article

Medium post with more details, [Beginner’s Celery/Flask example]([here](https://fithis2001.medium.com/beginners-celery-flask-example-57e45236016a))

## How to run:

Install first dependencies (dev for development)

```
python -m pip install -r requirements-dev.txt
```

Run docker (Rancher with WSL2 for me)

```
docker compose up
```

(and later stop with `docker compose down -v`)
Gevent is necessary for Windows users.

Start celery task

```
celery -A app.xxx worker --loglevel=info --hostname=blog_app -P gevent
```

Start app

```
python app.py
```

### How to test manually:

In your browser navigate to
```
http://127.0.0.1:5000/hello
```

You will get some json

```
{
  "status": "Task has been submitted",
  "task_id": "26e99828-2285-48be-8c52-ff4221129c0f"
}
```

To see whats going on take the task_id and nvaigate to

```
http://127.0.0.1:5000/hellowait/26e99828-2285-48be-8c52-ff4221129c0f
```

If the task id does not exist you will get a 404

with content

```
{
  "exists": false,
  "result": null
}
```

If pending you will get the same content but with status 204.

Otherwise you will get a 200 status with the result

```
{
  "exists": true,
  "result": "Hello, World!"
}
```

After finishing

```
docker compose down -v
```

### How to test automatically:

First build the docker image

```
docker compose -f .\docker-compose-dev.yml build
```

and then start the app

```
docker compose -f .\docker-compose-dev.yml up
```

Now run the test.

```
pytest .
```

It may take 10 secs to run because of the delay.


After finishing

```
docker compose -f .\docker-compose-dev.yml down -v
```

## References (sources I consulted):

***Tutorial:***

[https://medium.com/@shreshthbansal2505/using-flask-with-celery-and-flower-a-simple-guide-e0268b9d729a]()

***Backend troubleshooting:***

[https://stackoverflow.com/questions/76834173/how-does-celery-asyncresult-function-know-which-broker-or-backend-to-query]()

***Configure Flowerdocker compose:***

[https://hub.docker.com/r/mher/flower]()

***Configure Redis docker compose:***

[https://stackoverflow.com/questions/33304388/calling-redis-cli-in-docker-compose-setup]()

***Flower troubleshooting:***

[https://flower.readthedocs.io/en/latest/config.html#broker-api]()

[https://github.com/mher/flower/issues/114]()

[https://github.com/mher/flower/issues/1431]()
