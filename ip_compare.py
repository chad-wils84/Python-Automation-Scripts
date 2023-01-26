__author__ = 'Chad Wilson'
__version__ = '1.0'

"""
This script takes in two text files containing IP addresses and finds the MATCHING IPs between them. 
When you launch this program, you will be prompted by two file dialog windows. (Recommended you select the smallest file first)
Select the desired .txt file.
The location where you run the script will output two files. 
_IP_Matched.txt includes the matching IPs between the two files. 
The other _All_Invalid_IPs.txt will output all the invalid IPs found between the two text files.
"""

import ipaddress
import tkinter as tk
from tkinter import filedialog

def main():
    # Hide Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open two file dialog boxes
    file1_path = filedialog.askopenfile(title="File1 - Smallest file HERE")
    file2_path = filedialog.askopenfile(title="File2 - Larger file HERE")

    # Read the file 1 line at a time and remove blank entries
    file1 = file1_path.readlines()
    file1 = list(filter(None, file1))

    file2 = file2_path.readlines()
    file2 = list(filter(None, file2))

    # Remove IP duplicates from each file
    remove_duplicates_file1 = list(set(file1))
    remove_duplicates_file2 = list(set(file2))

    # Removes \n (new line) from each IP and creates a new list
    file1_sanitize = [ip.strip("\n") for ip in remove_duplicates_file1]
    file2_sanitize = [ip.strip("\n") for ip in remove_duplicates_file2]

    # Combine all IPs together to validate if the IP valid 
    all_ips = list(set(file1_sanitize + file2_sanitize))

    # Create a new file w/ matched IP   
    matched_ips = open("_IP_Matched.txt", "w")

    # Create a file w/ Invalid IP
    invalid_ips = open("_All_Invalid_IPs.txt", "w")

    # Validate IP addresses
    def validateip(ip_list):
        invalid_ip_list = []
        for ip in ip_list:
            try:
                if ipaddress.ip_address(ip):
                    pass
            except ValueError:
                invalid_ip_list.append(ip)
                invalid_ips.write(ip)
                invalid_ips.write('\n')
        return invalid_ip_list

    # Converts IPs in the list from IP strings to long IP integers
    # e.g. '100.71.9.98' to 1682377058
    def convert_ip_to_long_ip(list, invalids_list):
        ip_list = []
        # Converts IPs to long IP addresses if valid
        for ip in list:
            try:
                new_ip = int(ipaddress.ip_address(ip))
                ip_list.append(new_ip)
        # Exception error raised if IPs are not valid to delete
            except ValueError:
                if ip in invalids_list:
                    del ip
        return ip_list

    # Sorts the list of IPs
    def sort_ips(ip_list):
        return sorted(ip_list, key= lambda x: ''.join(('00' + x.split('.')[i])[-3::] for i in range(4)))

    # Uses Binary search algorithm to compare IP in file1 with file2
    def binary_search_compare(file1, ip1):
        low_ip = 0
        high_ip = len(file1) - 1
        while low_ip <= high_ip:
            mid = (low_ip + high_ip) // 2
            guess = file1[mid]
            if guess == ip1:
                return guess
            if guess > ip1:
                high_ip = mid - 1
            else:
                low_ip = mid + 1
        return None

    # Go through each IP in order to validate that each is valid
    list_invalid_ips = validateip(all_ips)

    #Sort the IPs ascending smallest to largest
    sorted_ipfile1 = sort_ips(file1_sanitize)
    sorted_ipfile2 = sort_ips(file2_sanitize)

    # Convert sorted IPs to long version form
    long_ip_file1 = convert_ip_to_long_ip(sorted_ipfile1, list_invalid_ips)
    long_ip_file2 = convert_ip_to_long_ip(sorted_ipfile2, list_invalid_ips)

    # Iterate through each IP in file1 
    for ip in long_ip_file1:
        # Use binary search to compare each long IP in file1 with IPs in file2
        found_ip = binary_search_compare(long_ip_file2, ip)
        # None represents no match if there's a match we skip
        if found_ip == None:
            pass
        else:
            matched_ips.write(f"{str(ipaddress.ip_address(found_ip))}\n")

main()