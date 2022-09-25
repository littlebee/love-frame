#!/bin/bash


src/love_frame.py > app.log 2>&1 &
pid=$!
echo $pid > ./app.pid

echo "Started server ($pid)"

