#import
import boto3

#credentials already input through awscli, stored in file on computer

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



