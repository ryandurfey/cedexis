#import
import boto3
import os
import re
from datetime import date

#credentials already input through awscli, stored in file on computer
#boto3 documentation http://boto3.readthedocs.org/en/latest/reference/services/s3.html#object

local_dir = '~/Documents/Cedexis/data'

client = boto3.client('s3')
result = client.list_objects(Bucket='public-radar', Prefix='Comcast/', Delimiter='/')

for x in result:
    print(x)
for o in result.get('CommonPrefixes'):
    print(o.get('Prefix'))
print(result)

for o in result.get('Contents'):
    print(o.get('Key'))
    # regular expression to match dates in format: 2010-08-27 and 2010/08/27
    date_reg_exp = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}', o.get('Key'))
    print(date_reg_exp)
today = date.today()
print(today)


#get files
#response = client.get_object(Bucket='string', Key='string')
'''
#def download_dir(client, resource, dist, local='/tmp', bucket='public-radar'):
client = boto3.client('s3', 'us-west-2')
dist = 'Comcast/'
bucket = 'public-radar'
local='/Users/RDURFE200/Documents/Cedexis/data/'
resource = boto3.resource('s3')

paginator = client.get_paginator('list_objects')
#For each file in bucket with prefix, if it doesn't already exist, download a copy
for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
    if result.get('Contents') is not None:
        for file in result.get('Contents'):
            if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):
                os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))
                resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))
s3 = boto3.resource('s3')
s3.meta.client.download_file('public-radar', 'Comcast/Comcast_CDN-2016-01-19.480.part-00808.kr.txt.gz', '/Users/RDURFE200/Documents/Cedexis/data/Comcast_CDN-2016-01-19.480.part-00808.kr.txt.gz')
#transfer.download_file('public-radar', 'Comcast/Comcast_CDN-2016-01-19.480.part-00808.kr.txt.gz', '~/Documents/Cedexis/data/Comcast' )
'''



