# stdlib
import time

# 3rd party
import boto3

# datadog
from checks import AgentCheck

client = boto3.client('s3')


class S3ObjectCount(AgentCheck):
    """
    Check s3 bucket and path and emit count of objects
    """

    def check(self, instance):
        year = time.strftime("%Y")
        month = time.strftime("%m")
        day = time.strftime("%d")
        DATE = '%s-%s-%s' % (year, month, day)
        BUCKET = instance['bucket']
        PREFIX = '%s/%s/%s/%s' % (instance['prefix'], year, month, day)

        file_list = self.ListFiles(client, BUCKET, PREFIX)
        file_count = self.CountFiles(file_list)
        instance_tags = instance.get('tags', [])
        self.gauge('s3.object_count.today', file_count,
                   tags=instance_tags + ["bucket:"+BUCKET, "prefix:"+PREFIX, "date:"+DATE])

    def ListFiles(self, client, bucket, prefix):
        paginator = client.get_paginator('list_objects')
        response = paginator.paginate(Bucket=bucket, Prefix=prefix)
        try:
            for page in response:
                for object in page['Contents']:
                   yield object['Key']
        except:
            print("s3 prefix not found")

    def CountFiles(self, file_list):
        count = 0
        for file in file_list:
            count = count + 1
        return count
