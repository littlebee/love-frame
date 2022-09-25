#!/bin/bash

# this script is meant to be run from your local development machine,
# in the scatbot project root dir
#
# parameters:
# <user@host> - required.
# <user> - optional. If user home directory is not /home/pi, provide the username only.
#
# example:
# ./upload.sh pi@raspberrypi.local

if [ "$1" == "" ]; then
  echo "Error: missing parameter.  usage: sbin/upload.sh [USER@]IP_ADDRESS_OR_NAME"
  echo "   ex:  sbin/upload.sh pi@raspberrypi.local"
  exit 1
fi

targetUser=pi
if [ "$2" != "" ]; then
  targetUser=$2
  echo "I see you"
  echo $targetUser
fi

# echo on
set -x

# stop on errors
set -e

TARGET_DIR="/home/$targetUser/love-frame"
TARGET_HOST=$1

rsync --progress --partial -avz \
--exclude=__pycache__/ \
--exclude=node_modules \
--exclude=data/ \
--exclude=.git \
--exclude=results* \
--exclude=camera_test_output* \
. $TARGET_HOST:$TARGET_DIR

