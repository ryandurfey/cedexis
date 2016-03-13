#import libraries
import ipaddress #convert IPs to integers
import csv #read in csv files
import base64 #convert via header
import os
from pathlib import Path
import re
import arrow # date/time library


#key concepts - enumerate over lists, list comprehensions where practical, bisection of mapping

''' Data Defintions
cd = cedexis data list of lists
ca = cran aggregates list of lists
co = countries file
st = state
ci = cities
as = AS number of network
'''

#ask user for a date range with default of today only
#loop through files for processing
#search amazon s3 location for files
#download files to hard drive
#unzip


#import file with cedexis data and read into list of lists
pathname = '/Users/RDURFE200/Documents/Cedexis/data/'
data_filename = 'Comcast_CDN_Tune-2016-03-08.27811.part-01067.kr.txt'
fileloc = pathname + data_filename
with open(fileloc) as cd_file:
    reader = csv.reader(cd_file, delimiter='\t')
    cd=list(reader)
cd_file.close()

#read in data type for use in filename
test_type_dict = {'0':'Response_Time', '1':'Availability', '14':'Throughput'}
test_type=test_type_dict.get(cd[1][3]) #any row, fourth column

#Remove columns 2, 3, 6, 8, 13, 15, 20& remove rows where client country in column 14 <> 223
cd = [[c[0], c[1], c[4], c[5], c[7], c[9], c[10], c[11], c[12], c[14], c[16], c[17], c[18], c[19], c[21]] for c in cd if c[14]=='223']


#convert base 64 via header and strip out unecessary data
for x, val in enumerate(cd):
    try:
        cd[x][1] = cd[x][1].replace('%3D','=')
        cd[x][1] = base64.b64decode(cd[x][1]).decode('utf-8')
        start = cd[x][1].find('odol-atsec-')
        end = cd[x][1].find('.comcast.net',70) #start at position 70 and look for this text
        cd[x][1] = cd[x][1][start+11:end]
        print(cd[x][1])
    except:
        pass
'''
#create mid tier column
node_loc=cd[1].split('.')
#create cache state column
state = node_loc[2]
#create cache city column
city = node_loc[3]
'''


#read in country, state, city, and network mapping files
filename = "/Users/RDURFE200/Documents/cedexis/lookups/countries.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    countries_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Documents/cedexis/lookups/states.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    states_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Documents/cedexis/lookups/cities.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    cities_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Documents/cedexis/lookups/asns.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    asns_dict = dict(reader)
temp_file.close()

#convert coded columns to readable data
cd = [[c[0], arrow.get(c[0]).floor('hour').format('YYYY-MM-DD HH:mm:ss'), c[1], c[2], c[3], countries_dict.get(c[4]), states_dict.get(c[5]), cities_dict.get(c[6]), asns_dict.get(c[7]), c[8], countries_dict.get(c[9]), states_dict.get(c[10]), cities_dict.get(c[11]), asns_dict.get(c[12]), c[13][:-3], c[14]] for c in cd]

#map comcast client ip addresses to crans
#read in CRAN_Aggregates mapping file with 4 columns, cidr block, cran, integer start, integer end
filename = "/Users/RDURFE200/Documents/cedexis/lookups/cran_aggs_processed.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    ca = list(reader)
temp_file.close()

low = 0
high = len(ca)
mid = (high+low)//2 #integer division
z=0
for z, val in enumerate(cd):
    #convert client ip to integer based on whether it is IPv4 or IPv6
    if cd[z][13]=='COMCAST-7922': # only search if client is on comcast
        cd_num = int(ipaddress.ip_address(cd[z][14]))
        while True: #loop until break
            if (high-low)<=1:
                #check low range
                if cd_num >= int(ca[low][2]) and cd_num <= int(ca[low][3]):
                    cd[z].append(ca[low][0])
                elif cd_num >= int(ca[high][2]) and cd_num <= int(ca[high][3]):
                    cd[z].append(ca[high][0])
                else:
                    cd[z].append('no match')
                break
            #check client ip against mid point and narrow bisection window
            if cd_num >= int(ca[mid][2]):
                low = mid
                mid = (high+low)//2
            else:
                high = mid
                mid = (high+low)//2

cd.insert(0, ['timestamp', 'timestamp rounded', 'server', 'response code', 'measurement', 'resolver country', 'resolver state', 'resolver city', 'resolver network', 'resolver ip', 'client country', 'client state', 'client city','client network', 'client ip stripped', 'agent', 'cran'])
#add in column labels

#Write text file

fileloc = pathname + data_filename[:-3] + test_type +'.txt'
with open(fileloc, "w") as temp_file:
    writer = csv.writer(temp_file, delimiter = '\t')
    writer.writerows(cd)
temp_file.close()

print(fileloc)








'''
0	timestamp
1   timestamp rounded to 15 min interval*
2	server hostname
3   server state*
4   server city*
5   mid tier hostname
6	response_code
7	measurement
8	resolver country
9	resolver state
10	resolver city
11	resolver asn
12	resolver ip
13	client country
14	client state
15	client city
16	client asn
17	client ip stripped
18	agent

Original column list
Column ID	Name
0	timestamp
1	unique_node_id
2	provider_id*
3	probe_type*
4	response_code
5	measurement
6	resolver market*
7	resolver country
8	resolver region*
9	resolver state
10	resolver city
11	resolver asn
12	resolver ip
13	client market *
14	client country
15	client region*
16	client state
17	client city
18	client ASN
19	client ip stripped
20	HTTP Referrer Header MD5*
21	agent

Remove columns, 2, 3, 6, 8, 13, 15
223 = country code us

Ending column list
Column ID	Name
0	timestamp
1   timestamp rounded to 15 min interval
2	server hostname
3   server state
4   server city
5   mid tier hostname
6	response_code
7	measurement
8	resolver country
9	resolver state
10	resolver city
11	resolver asn
12	resolver ip
13	client country
14	client state
15	client city
16	client asn
17	client ip stripped
18	agent
'''

