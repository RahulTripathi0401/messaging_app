#!/bin/sh
echo "$1" > port.txt
export FLASK_RUN_PORT=$1
export FLASK_APP=server.py
export FLASK_DEBUG=1
python3 -m flask run
# python3 server.py $1
