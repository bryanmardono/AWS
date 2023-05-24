import boto3
import os

def change_log_group_retention(log_group_name, retention_period):
    client = boto3.client('logs')
    client.put_retention_policy(
        logGroupName=log_group_name,
        retentionInDays=retention_period
    )

def lambda_handler(event, context):
    if 'detail' in event and 'eventName' in event['detail']:
        if event['detail']['eventName'] == 'CreateLogGroup':
            log_group_name = event['detail']['requestParameters']['logGroupName']
            change_log_group_retention(log_group_name, 14)
    else:
        client = boto3.client('logs')
        response = client.describe_log_groups()
        for log_group in response['logGroups']:
            if log_group['retentionInDays'] == 0:
                change_log_group_retention(log_group['logGroupName'], 14)

s3_client = boto3.client('s3')
bucket_name = 'retention_script'

# Create the S3 bucket
s3_client.create_bucket(Bucket=bucket_name)

# Upload the script to the S3 bucket
s3_client.upload_file(__file__, bucket_name, 'logroup_retention.py')