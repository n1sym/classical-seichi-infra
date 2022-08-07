#!/bin/sh
cd /home/ec2-user/minecraft

sqlite3 -header -csv development.db "select name, count from seichi_count inner join account on seichi_count.id = account.id inner join account_name on account.id = account_name.id;" > seichi_count.csv

NOW=`date "+%Y%m%d"`
cp seichi_count.csv seichi_count_${NOW}.csv 
aws s3 cp seichi_count_${NOW}.csv s3://classical-seichi/seichi_count/
rm seichi_count_${NOW}.csv