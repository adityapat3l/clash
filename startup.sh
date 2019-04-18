#!/bin/bash

cd /home/apatel/clash
cat requirements.txt | xargs -n 1 pip install


# sudo lsof -i -P -n
# sudo kill PID