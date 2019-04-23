#!/bin/bash

cd /home/apatel/clash
mkdir logs
cat requirements.txt | xargs -n 1 pip install


# sudo lsof -i -P -n
# sudo kill PID

# gunicorn --bind 0.0.0.0:8000 webui.index:server

# celery -A webui.webapp.celery worker --loglevel=debug
