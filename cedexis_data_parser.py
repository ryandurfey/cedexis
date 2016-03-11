#import libraries
import ipaddress #convert IPs to integers
import csv #read in csv files
import base64 #convert via header

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
filepath = "Comcast_CDN-2016-02-28.480.part-01005.kr.txt"
with open(filepath) as cd_file:
    cd = csv.reader(cd_file, delimiter='\t')
filepath.close()

#read in data type for use in filename
tt_d = {0:'Response_Time', 1:'Availability', 14:'Throughput'}
test_type=get.cd[1][3] #any row, fourth column

#remove non-critical rows and columns to reduce data size
cd = [c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14] where c[14]=='223' for c in cd]


#convert base 64 via header and strip out unecessary data
#create mid tier column
node_loc=cd[1].split('.')
#create cache state column
state = node_loc[2]
#create cache city column
city = node_loc[3]

#read in country, state, city, and network mapping files
filepath = "countries.txt"
with open(filepath) as country_file:
    country_dict = csv.reader(country_file, delimiter=',')
filepath.close()
filepath = "states.txt"
with open(filepath) as state_file:
    state_dict = csv.reader(state_file, delimiter=',')
filepath.close()
filepath = "cities.txt"
with open(filepath) as city_file:
    city_dict = csv.reader(city_file, delimiter=',')
filepath.close()
filepath = "asns.txt"
with open(filepath) as asn_file:
    asn_dict = csv.reader(asn_file, delimiter=',')
filepath.close()


#convert coded columns to readable data
cd = [c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11], c[12], c[13], c[14] for c in cd]
#create time rounding column


#map comcast client ip addresses to crans
#read in CRAN_Aggregates mapping file
low=0
high=len(ca)
mid = (high+low)//2 #integer division
for z in enumerate(cd):
    #convert client ip to integer based on whether it is IPv4 or IPv6
    cd_num = int()
    #Check if bisection window is down to two values
    while true:
        if (high-low)<=1:
            #check low range
            if cd_num
            #check high range
            #set "no match" if no match found
            break
        #check client ip against mid point and narrow bisection window
        if cd_num >= ca[mid][2]:
            low = mid
            mid = mid = (high+low)//2
        else:
            high = mid
            mid = mid = (high+low)//2

#write tab delimited processed data file


'''
Original column list
Column ID	Name
0	timestamp
1	unique_node_id
2	provider_id
3	probe_type
4	response_code
5	measurement
6	resolver market
7	resolver country
8	resolver region
9	resolver state
10	resolver city
11	resolver asn
12	resolver ip
13	client market 
14	client country
15	client region
16	client state
17	client city
18	client ASN
19	client ip stripped
20	HTTP Referrer Header MD5
21	agent
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
Status API Training Shop Blog About Pricing
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
