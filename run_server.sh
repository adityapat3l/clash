#!/bin/bash


cd /home/apatel/clash
source venv/bin/activate

sudo gunicorn --bind 0.0.0.0:80 webui.index:server