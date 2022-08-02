import json
import os
from datetime import datetime

import boto3


def json_dt(o):
    if isinstance(o, datetime):
        return o.isoformat()


def change_record(action, host_name, host_addr):
    domain_name = os.environ.get('DomainName')
    if domain_name:
        host_name = F"{host_name}.{domain_name}."
    client = boto3.client('route53')
    change_batch = {
        "Comment": "optional comment about the changes in this change batch request",
        "Changes": [
            {
                "Action": action,
                "ResourceRecordSet": {
                    "Name": host_name,
                    "Type": "A",
                    "TTL": 300,
                    "ResourceRecords": [
                        {
                          "Value": host_addr
                        }
                    ]
                }
            }
        ]
    }
    print("change_batch: " + json.dumps(change_batch, default=json_dt))
    response = client.change_resource_record_sets(
        HostedZoneId=os.environ.get('HostedZoneId'),
        ChangeBatch=change_batch
    )
    print("result: " + json.dumps(response, default=json_dt))
    return response


def get_hostname_from_tags(tags):
    host_name = ''
    for tag in tags:
        if tag['Key'].lower() == 'hostname':
            host_name = tag['Value'].lower()
    return host_name


def check_action(state):
    if state == 'running':
        action = 'UPSERT'
    elif state == 'stopping':
        action = 'DELETE'
    else:
        action = ''
    return action


def lambda_handler(event, context):
    result = dict()
    print('event: ' + json.dumps(event, default=json_dt))
    action = check_action(event['detail']['state'])
    if action:
        ec2 = boto3.resource('ec2')
        instance = ec2.Instance(event['detail']['instance-id'])
        host_name = get_hostname_from_tags(instance.tags)
        if host_name:
            host_addr = instance.public_ip_address
            result = change_record(action, host_name, host_addr)
    return json.dumps(result, default=json_dt)