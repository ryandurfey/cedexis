#import
import csv
import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

'''
client = boto3.client('s3')
s3 = boto3.resource('s3')
bucket = s3.Bucket('public-radar')
response = client.list_objects(Bucket='public-radar', Prefix = '/Comcast/')

client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

client = boto3.client(
    's3',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY)
s3 = boto3.resource('s3')
bucket = 'public-radar'
client.list_objects(bucket.list("files/", "/"))

#client.list_objects(Bucket='public-radar')
#client.list_objects(bucket.list('Comcast/')


filename = "/Users/RDURFE200/Documents/cedexis/lookups/s3_credentials.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    asc = dict(reader)
temp_file.close()
print(asc)

LOCAL_PATH = '/Users/RDURFE200/Documents/cedexis/data'
AWS_ACCESS_KEY_ID = asc.get('access_key')
AWS_SECRET_ACCESS_KEY = asc.get('secret_access_key')
'''