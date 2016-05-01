#!/bin/bash          
export PATH=/usr/local/bin:$PATH
cd /home/ubuntu/indeed/static/
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
cd /home/ubuntu/indeed/static/output
sudo python deduplicate.py
cd /home/ubuntu/indeed/static/output/transfer
sudo gzip V2.csv
sudo mv ./V2.csv.gz /var/www/html/downloads
sleep 20
echo Starting_Scrapy
cd /home/ubuntu/indeed/
scrapy crawl main_scraper -o /home/ubuntu/indeed/static/output/out_cron.csv

