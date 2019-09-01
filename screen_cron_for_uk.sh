#!/usr/bin/env bash
while true
do
    rm /home/myanime/indeed_server_uk/static/output/may.csv
    touch /home/myanime/indeed_server_uk/static/output/may.csv
    /home/myanime/indeed_server_uk/local_indeed.sh
    echo "Starting in 24hrs"
    sleep 43200
done