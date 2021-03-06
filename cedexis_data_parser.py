'''
Purpose of this script is:
1. Read in Cedexis data for Comcast CDN
2. Eliminate any unneeded rows and columns to trim size of file
3. Decode base64 encoded via header data and parse out values for edge server
4. Decode all coded columns including network, country, state, and city
5. Parse User Agent String to extract hardware OS and Browser
'''


#imports
import ipaddress #convert IPs to integers
import csv #read/write csv files
import base64 #decode base64 via header
import re #parsing via header text to extract server info
import arrow # date/time library for parsing timestamps
from user_agents import parse #user agent parsing library


#import file with cedexis data and read into list of lists
pathname = '/Users/RDURFE200/Downloads/Cedexis/'
data_filename = 'Comcast_CDN_Tune-2016-05-15.27811.part-00836.kr.txt'
fileloc = pathname + data_filename
with open(fileloc) as cd_file:
    reader = csv.reader(cd_file, delimiter='\t')
    cd=list(reader)
cd_file.close()


#get the test type from the 4th column in the data for use in filename
test_type_dict = {'0':'Response_Time', '1':'Availability', '14':'Throughput'}
test_type=test_type_dict.get(cd[1][3]) #any row, fourth column contains data


#Remove columns 2, 3, 6, 8, 13, 15, 20& remove rows where client country in column 14 <> 223 USA
cd = [[c[0], c[1], c[4], c[5], c[7], c[9], c[10], c[11], c[12], c[14], c[16], c[17], c[18], c[19], c[21]] for c in cd if c[14]=='223']


#convert base 64 via header and strip out unecessary data
for x, val in enumerate(cd):
    try:
        cd[x][1] = cd[x][1].replace('%3D','=') #padding encoded improperly for base64
        cd[x][1] = base64.b64decode(cd[x][1]).decode('utf-8')
        atsmid = re.search(r"(odol-atsmid.*?net)", cd[x][1]).group(1) #get mid tier server
        atsec = re.search(r"(odol-atsec.*?net)", cd[x][1]).group(1) #get edge tier server
        atsec_code = re.search(r"\[(.*?)\]", cd[x][1]).group(1) #get via codes
        atsec_st = atsec.split('.')[2] #get state from edge tier server
        atsec_city = atsec.split('.')[3] #get city from edge tier server
        cd[x][1] = atsec
        cd[x].extend((atsmid.split('.')[0], atsec_st, atsec_city, atsec_code))
    except:
        cd[x][1] = 'no data'
        cd[x].extend(('no data', 'no data', 'no data', 'no data'))
        pass


#read in country, state, city, and network mapping files
filename = "/Users/RDURFE200/Downloads/Cedexis/Lookups/countries.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    countries_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Downloads/Cedexis/Lookups/states.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    states_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Downloads/Cedexis/Lookups/cities.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    cities_dict = dict(reader)
temp_file.close()

filename = "/Users/RDURFE200/Downloads/Cedexis/Lookups/asns.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    asns_dict = dict(reader)
temp_file.close()


#Parse user agent string using this library https://pypi.python.org/pypi/user-agents
for y, val in enumerate(cd):
    try:
        ua_string = cd[y][14]
        user_agent = parse(ua_string) #parse user agent string in column 14
        device = user_agent.device.family # returns 'iPhone'
        browser = user_agent.browser.family # returns 'Mobile Safari'
        os = user_agent.os.family # returns 'iOS'
        cd[y].extend((device, os, browser))
    except:
        cd[y].extend(( 'no device data', 'no os data', 'no browser data'))
        pass


#convert coded columns to readable data, add a rounded time column, and also strip out cidr block from client IP
cd = [[c[0], arrow.get(c[0]).floor('hour').format('YYYY-MM-DD HH:mm:ss'), c[1], c[2], c[3], countries_dict.get(c[4]), states_dict.get(c[5]), cities_dict.get(c[6]), asns_dict.get(c[7]), c[8], countries_dict.get(c[9]), states_dict.get(c[10]), cities_dict.get(c[11]), asns_dict.get(c[12]), c[13][:-3], c[14], c[15], c[16], c[17], c[18], c[19], c[20], c[21]] for c in cd]


#map comcast client ip addresses to crans
#read in CRAN_Aggregates mapping file with 4 columns, cidr block, cran, integer start, integer end
filename = "/Users/RDURFE200/Documents/cedexis/lookups/cran_aggs_processed.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    ca = list(reader)
temp_file.close()
#iterate over Cedexis data and where network = comcast, search for client IP in our cran to cidr block mapping file
for z, val in enumerate(cd):
    if cd[z][13]=='COMCAST-7922': # only search if client is on comcast
        #convert client ip to integer based on whether it is IPv4 or IPv6
        cd_num = int(ipaddress.ip_address(cd[z][14]))
        #set parameters for bisection search of cran_aggs file
        low = 0
        high = len(ca)
        mid = (high+low)//2 #integer division
        while True: #loop until break
            if (high-low)<=1:  #once window is narrowed to two possibilities, check both
                #check low range
                if cd_num >= int(ca[low][2]) and cd_num <= int(ca[low][3]):
                    cd[z].append(ca[low][0])
                elif cd_num >= int(ca[high][2]) and cd_num <= int(ca[high][3]):
                    cd[z].append(ca[high][0])
                else:
                    cd[z].append('no match')
                break
            #check client ip against mid point and narrow bisection search window
            if cd_num >= int(ca[mid][2]):
                low = mid
                mid = (high+low)//2
            else:
                high = mid
                mid = (high+low)//2


#add in column labels into first line of list
cd.insert(0, ['timestamp', 'timestamp rounded', 'atsec', 'response code', 'measurement', 'resolver country', 'resolver state', 'resolver city', 'resolver network', 'resolver ip', 'client country', 'client state', 'client city','client network', 'client ip stripped', 'agent', 'atsmid', 'atsec_state', 'atsec_city', 'atsec_code', 'hardware', 'os', 'browser', 'client cran'])


#Write text file
fileloc = pathname + data_filename[:-3] + test_type +'.txt'
with open(fileloc, "w") as temp_file:
    writer = csv.writer(temp_file, delimiter = '\t')
    writer.writerows(cd)
temp_file.close()
print(fileloc)


'''
Original Column List from TXT file from Cedexis
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
edge server state
edge server city
edge server cache response code
mid tier server
user agent hardware
user agent os
user agent browser


Original column list

'''

