#import
import boto3

client = boto3.client('s3')
result = client.list_objects(Bucket='public-radar',
                             Prefix='Comcast/',
                             Delimiter='/'
                             )
for o in result.get('CommonPrefixes'):
    print(o.get('Prefix'))


