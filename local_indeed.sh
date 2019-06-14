#!/bin/bash
#PROJECT_DIR="/Users/ryan/repos/indeed_server"
#AWS_KEY="/Users/ryan/.ssh/aws_schlupfi.pem"
COUNTRY='au'
COUNTRY='sg'
COUNTRY='canada'
COUNTRY='usa'
PROJECT_DIR='/home/myanime/indeed_server_'$COUNTRY
AWS_KEY="/home/myanime/.ssh/aws_schlupfi.pem"
cd $PROJECT_DIR/static/
mkdir $PROJECT_DIR/static/output/transfer/
rm $PROJECT_DIR/static/errors.txt
touch $PROJECT_DIR/static/errors.txt
date >> ./runcounter
date +%d-%m-%Y_%H:%M > date
sleep 5
echo Starting_Scrapy
cd $PROJECT_DIR/
source ~/indeedenv/bin/activate
scrapy crawl indeed_scraper -o $PROJECT_DIR/static/output/may.csv
echo may > $PROJECT_DIR/static/output/filename
sleep 10
cd $PROJECT_DIR/static/output
python deduplicate.py
cd $PROJECT_DIR/static/output/transfer
gzip $PROJECT_DIR/static/output/transfer/*.*
scp -i $AWS_KEY -r $PROJECT_DIR/static/output/transfer/* ubuntu@52.59.254.43:./countries/$COUNTRY
rm $PROJECT_DIR/static/output/transfer/*