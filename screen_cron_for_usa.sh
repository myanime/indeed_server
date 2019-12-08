#!/usr/bin/env bash
while true
do
    rm /home/myanime/indeed_server_usa/static/output/may.csv
    touch /home/myanime/indeed_server_usa/static/output/may.csv
    /home/myanime/indeed_server_usa/local_indeed.sh
    echo "Starting in 8hrs"
    sleep 28800
    /home/myanime/indeed_server_usa/local_indeed.sh
    echo "Starting in 8hrs"
    sleep 28800
    /home/myanime/indeed_server_usa/local_indeed.sh
    echo "Starting in 8hrs"
    sleep 28800

done