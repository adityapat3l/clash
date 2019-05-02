#!/bin/bash


cd /home/apatel/clash
source venv/bin/activate

export PYTHONPATH=~/clash/
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
venv/bin/gunicorn --bind localhost:8080 -w 2 webui.index:server