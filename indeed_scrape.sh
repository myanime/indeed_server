#!/bin/bash
export PATH=/usr/local/bin:$PATH
CURRENT_FILENAME=may
MYDATE=$(date +"%d_%m_%Y")
cd /home/ubuntu/indeed/static/
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
cd /home/ubuntu/indeed/static/output
sudo python deduplicate.py
cd /home/ubuntu/indeed/static/output/transfer
sudo gzip *.*
sudo mv *.* /var/www/html/downloads
sleep 5
echo Starting_Scrapy
cd /home/ubuntu/indeed/
scrapy crawl main_scraper -o /home/ubuntu/indeed/static/output/$CURRENT_FILENAME.csv
echo $CURRENT_FILENAME > /home/ubuntu/indeed/static/output/filename
