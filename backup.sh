#!/bin/sh
cd /home/ec2-user/minecraft

NOW="backup"
WORLD_NAME="world_1"
zip ${NOW}.zip -r ${WORLD_NAME}/
aws s3 cp ${NOW}.zip s3://classical-seichi/world_backup/${WORLD_NAME}/
rm -f ${NOW}.zip

aws s3 cp development.db s3://classical-seichi/db_backup/