#!/bin/bash

pid_file="./app.pid"
pid=`cat $pid_file`

if [ -f "$pid_file" ]; then
  echo "killing pid $pid"
  kill -1 $pid
else
  echo "$pid_file does not exist."
fi