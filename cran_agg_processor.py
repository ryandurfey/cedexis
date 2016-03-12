
import ipaddress #convert IPs to integers
import csv #read in csv files
import base64 #convert via header
import os
from pathlib import Path

filename = "/Users/RDURFE200/Documents/cedexis/cran_aggs.txt"
with open(filename) as temp_file:
    reader = csv.reader(temp_file, delimiter='\t')
    ca = list(reader)
temp_file.close()

for i, val in enumerate(ca):
    #split cider block
    #convert block to integer
    #If IP address is ipv4,
        # convert to start integer
        # add the cidr block to end integer
    #Elif IP address is ipv6
        # convert to start integer
        # add the cidr block to end integer
    #else:
        #start num = 0
        #end num = 0
    #append value to ca

filename = "/Users/RDURFE200/Documents/cedexis/cran_aggs_processed.txt"
with open(filename, "w") as temp_file:
    writer = csv.writer(temp_file)
    writer.writerows(ca)
temp_file.close()