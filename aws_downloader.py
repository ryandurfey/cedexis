#imports
import csv
import sys, os
import os
import arrow
import datetime


filename = "/Users/RDURFE200/Documents/cedexis/lookups/s3_credentials.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    asc = dict(reader)
temp_file.close()
print(asc)
LOCAL_PATH = '/Users/RDURFE200/Documents/cedexis/data'
AWS_ACCESS_KEY_ID = asc.get('access_key')
AWS_SECRET_ACCESS_KEY = asc.get('secret_access_key')
bucket_name = asc.get('bucket')

#get today's date and calculate yesterday's date
#aws s3 cp s3://public-radar/Comcast/ ~/Documents/Cedexis --recursive --exclude "*" --include "*2016-02-28.27811*"
#aws s3 cp s3://public-radar/Comcast/ ~/Documents/Cedexis --recursive --exclude "*" --include "*2016-02-28.480*"

#os.system('your_command')



now = datetime.datetime.now()
print (now.year)
print(now)
print(now.day)
print(now.month)
# yesterday =

perf_file_download = '#aws s3 cp s3://public-radar/Comcast/ ~/Documents/cedexis/data --recursive --exclude "*" --include "*' + yesterday +'.480'
tune_file_download = '#aws s3 cp s3://public-radar/Comcast/ ~/Documents/cedexis/data --recursive --exclude "*" --include "*' + yesterday +'.27811'

os.system(perf_file_download)
os.system(tune_file_download)

#unzip files in ~/Documents/cedexis/data
#read in names of files
#figure out which ones are gzip
#unzip them

