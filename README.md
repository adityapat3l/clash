# Welcome to Clashboard

Clash of Clans is one of the largest mobile games on the App Store
with over a million monthly users. This project is meant to provide 
analytics behind what drives your clan, tracking your clan members's progress
over time. This uses the Official Clash of Clans API


## Getting Started

You will need some credentials to get started:

1) [Clash of Clans API KEY](https://developer.clashofclans.com/#/login)
2) A mysql database (I use [Remote Mysql](https://remotemysql.com/), which is free)

##### optional

If you don't use these, you'll need to comment out some code.

1) Celery Broker: [CloudAMPQ](https://www.cloudamqp.com/) (Free Tier)
2) Timber Logging: [Timber IO](https://timber.io/) (Free upto a Limit)

### Note:
```
This Project is Broken into 2 parts:
1) Clashapp: The backend
2) Webui: The fronend
```

### Installing
##### Install Requirements
```
pip3 install -r requirement.txt
```

##### To start up Clashapp
First time:
```
export PYTHONPATH=~/clash
python3 -m clashapp.db_initializer
```
Automated cronjob:
```
export PYTHONPATH=~/clash
python3 -m clashapp.hourly_update
```

##### To start up Webui
In Production:
```
chmod +x run_server.sh
./run_server.sh
```

In Development:
```
export PYTHONPATH=~/clash
python3 -m webui.index
```
