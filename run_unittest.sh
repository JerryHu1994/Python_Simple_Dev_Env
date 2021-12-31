#!/bin/bash
redis-server &
python server.py &
python -m pytest
killall python
pkill "redis-server"
echo "Exiting..."