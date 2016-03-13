#imports
import csv
import boto3
import boto
import sys, os
from boto.s3.key import Key

filename = "/Users/RDURFE200/Documents/cedexis/lookups/s3_credentials.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    asc = dict(reader)
temp_file.close()
print(asc)

#access the file using the URL: http://s3.amazonaws.com/bucket_name/key but you can also use the boto library to download the files.

LOCAL_PATH = '/Users/RDURFE200/Documents/cedexis/data'
AWS_ACCESS_KEY_ID = asc.get('access_key')
AWS_SECRET_ACCESS_KEY = asc.get('secret_access_key')
bucket_name = asc.get('bucket')
'''
s3 = boto3.resource('s3')
my_bucket = s3.Bucket('cedexis/Comcast/')
for object in mybucket.objects.all():
    print(object)
'''
from boto3 import client
conn = client('s3')
# again assumes boto.cfg setup, assume AWS S3
 for key in conn.list_objects(Bucket='bucket_name')['Contents']:
     print(key['Key'])

'''
client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
'''

'''
from subprocess import call
call(["ls", "-l"])
'''

'''
# connect to the bucket
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(bucket_name)
# go through the list of files
bucket_list = bucket.list()
print(bucket_list)
for l in bucket_list:
  keyString = str(l.key)
  # check if file exists locally, if not: download it
  if not os.path.exists(LOCAL_PATH+keyString):
    l.get_contents_to_filename(LOCAL_PATH+keyString)
'''