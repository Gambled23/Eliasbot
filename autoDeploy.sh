#!/bin/bash

cd /home/cesar/eliasbot
source venv/bin/activate

while true do
    screen -dmS eliasbot python3 bot.py
    sleep $((24 * 60 * 60))
    screen -X -S eliasbot quit
    sleep 10
done