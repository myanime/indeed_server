#!/usr/bin/env bash
COUNTRY='au'
echo "Poor Mans Cron"
sleep 5
echo "Starting"
osascript -e 'tell application "Terminal" to do script "/Users/ryan/repos/indeed_server/local_indeed.sh"'

while true
do
    echo "Starting in 24hrs"
    sleep 14400
    osascript -e 'tell application "Terminal" to do script "/Users/ryan/repos/indeed_server/local_indeed.sh"'
done