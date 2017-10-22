
import json
import urllib.parse
import boto3
import ast
import os
import collections
from datetime import date
from botocore.errorfactory import ClientError

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    prefix = '' # S3 key prefix (e.g. backups/)
    s3Event = json.loads(event['Records'][0]['Sns']['Message'])
    
    source_bucket = s3Event['Records'][0]['s3']['bucket']['name']
    source_key = urllib.parse.unquote_plus(s3Event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    source_size = s3Event['Records'][0]['s3']['object']['size']
    
    fileName = os.path.basename(source_key)
    name = os.path.splitext(fileName)[0]
    extension = os.path.splitext(fileName)[1]
    project = source_key.replace(prefix+'latest/','',1).replace('/'+fileName,'',1)
    
    
    print("Project: " + project)
    print("FileName: " + fileName)
    print("Name: " + name)
    print("Extension: " + extension)
    
    today = date.today()
    week = today.strftime('%Y-%W')
    ymd = today.strftime('%Y-%m-%d')
    ym = today.strftime('%Y-%m')
    year = today.strftime('%Y')
    weekDay = today.strftime('%A')
    month = today.strftime('%B')
    
    
    #target_bucket = source_bucket
    target_bucket = os.environ['target_bucket']
    
    #target_latest_key = prefix+'latest/{}/{}'.format(project,fileName)
    #target_daily_key = prefix+'daily/{}/{}_{}.{}{}'.format(project,name,ymd,weekDay,extension)
    #target_weekly_key = prefix+'weekly/{}/{}_{}{}'.format(project,name,week,extension)
    target_monthly_key = prefix+'monthly/{}/{}_{}.{}{}'.format(project,name,ym,month,extension)
    #target_yearly_key = prefix+'yearly/{}/{}_{}{}'.format(project,name,year,extension)
    
    targets = {target_bucket:target_monthly_key}
    
    print("Targets: " + json.dumps(targets, indent=2))
    
    try:
        for dest_bucket, dest_key in targets.items():
            try:
                s3.head_object(Bucket=dest_bucket, Key=dest_key)
                print('Skipping {}/{}, it already exists.'.format(dest_bucket, dest_key))
            except ClientError:
                print('Copying from {}/{} to {}/{} ...'.format(source_bucket, source_key, dest_bucket, dest_key))
                copy_source = {'Bucket':source_bucket, 'Key':source_key}
                s3.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource=copy_source)
        return 'Success'
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}.'.format(source_key, source_bucket))
        raise e

