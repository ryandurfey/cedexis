#import
import ipaddress #convert IPs to integers
import csv #read in csv files
from operator import itemgetter

filename = "/Users/RDURFE200/Documents/cedexis/lookups/cran_aggs.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    ca = list(reader)
temp_file.close()
print(ca[1])


for i, val in enumerate(ca):
    ip, block = ca[i][1].split('/') #split the cidr block
    block=int(block) #convert block to integer from string
    ip = ipaddress.ip_address(ip)
    if ip.version == 4 : # convert address from ipv4 notation to integer
        block_start_int = int(ipaddress.IPv4Address(ip))
        block_end_int = block_start_int + 2**(32 - block) - 1
    elif ip.version == 6: #convert address from ipv6 notation to integer
        block_start_int = int(ipaddress.IPv6Address(ip))
        block_end_int = block_start_int + 2**(128 - block) - 1
    else:
        block_start_int = 0
        block_end_int = 0
    #Append data to a list of dictionaries so it can be sorted and processed
    ca[i].append(block_start_int)
    ca[i].append(block_end_int)

ca = sorted(ca, key=itemgetter(2))

filename = "/Users/RDURFE200/Documents/cedexis/lookups/cran_aggs_processed.txt"
with open(filename, "w") as temp_file:
    writer = csv.writer(temp_file, delimiter ='\t')
    writer.writerows(ca)
temp_file.close()

