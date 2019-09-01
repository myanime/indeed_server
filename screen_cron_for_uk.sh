#!/usr/bin/env bash
while true
do
    echo "Starting in 24hrs"
    rm /home/myanime/indeed_server_uk/static/output/may.csv
    touch /home/myanime/indeed_server_uk/static/output/may.csv
    /home/myanime/indeed_server_uk/local_indeed.sh
    sleep 43200
done