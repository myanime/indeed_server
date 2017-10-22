#!/bin/bash
export PATH=/usr/local/bin:$PATH
CURRENT_FILENAME=may
MYDATE=$(date +"%d_%m_%Y")
cd /home/media/indeed/static/
mkdir /home/media/indeed/static/output/transfer/
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd /home/media/indeed/
scrapy crawl selenium_scraper -o /home/media/indeed/static/output/$CURRENT_FILENAME.csv
echo $CURRENT_FILENAME > /home/media/indeed/static/output/filename
sleep 10
cd /home/media/indeed/static/output
sudo python deduplicate.py
cd /home/media/indeed/static/output/transfer
#sudo gzip *.*
#mv *.* /home/media/countries/au/
#scp -i /home/media/.ssh/aws_schlupfi.pem -r /home/media/countries/au/* ubuntu@52.59.254.43:./countries/au