#!/usr/bin/env bash
COUNTRY='au'
#COUNTRY='sg'
#COUNTRY='canada'
#COUNTRY='usa'

echo "Poor Mans Cron"
sleep 5
echo "Starting"
gnome-terminal --command=/home/myanime/indeed_server_$COUNTRY/local_indeed.sh --display=:0

while true
do
    echo "Starting in 24hrs"
    sleep 14400
    gnome-terminal --command=/home/myanime/indeed_server/local_indeed.sh --display=:0
done