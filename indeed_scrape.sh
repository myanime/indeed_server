#!/bin/bash
export PATH=/usr/local/bin:$PATH
CURRENT_FILENAME=may
HOME_DIR=media
PROJECT_DIR=indeed
MYDATE=$(date +"%d_%m_%Y")
cd /home/$HOME_DIR/$PROJECT_DIR/static/
mkdir /home/$HOME_DIR/$PROJECT_DIR/static/output/transfer/
rm /home/$HOME_DIR/$PROJECT_DIR/static/errors.txt
touch /home/$HOME_DIR/$PROJECT_DIR/static/errors.txt
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd /home/$HOME_DIR/$PROJECT_DIR/
scrapy crawl selenium_scraper -o /home/$HOME_DIR/$PROJECT_DIR/static/output/$CURRENT_FILENAME.csv
echo $CURRENT_FILENAME > /home/$HOME_DIR/$PROJECT_DIR/static/output/filename
sleep 10
cd /home/$HOME_DIR/$PROJECT_DIR/static/output
python deduplicate.py
cd /home/$HOME_DIR/$PROJECT_DIR/static/output/transfer
gzip *.*
mv *.* /home/$HOME_DIR/countries/au/
scp -i /home/$HOME_DIR/.ssh/aws_schlupfi.pem -r /home/$HOME_DIR/countries/au/* ubuntu@52.59.254.43:./countries/au