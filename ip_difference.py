__author__ = 'Chad Wilson'
__version__ = '1.0'

"""
This script takes in two text files containing IP addresses and finds the DIFFERENCES between them. 
When you launch this program, you will be prompted by two file dialog windows. (Recommended you select the smallest file first).
Select the desired .txt files.
The location where you run the script will output two files. 
_IP_Difference.txt includes the IP differences between the two files. 
The other _All_Invalid_IPs.txt will output all the invalid IPs found between the two text files.
"""

import ipaddress
import tkinter as tk
from tkinter import filedialog
from difflib import Differ

def main():
    # Hide Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open two file dialog boxes
    file1_path = filedialog.askopenfile(title="File1 - Smallest file HERE")
    file2_path = filedialog.askopenfile(title="File2 - Larger file HERE")

    # Read the file 1 line one at a time and remove blank entries
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
    difference_ips = open("_IP_Difference.txt", "w")

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
    def binary_search(file1, ip1):
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

    # Finds the difference between 2 lists and returns the difference in another list 
    def ip_difference(list_1, list_2):
        differ = Differ()
        ip_list = []
        for line in differ.compare(list_1, list_2):
            if line.startswith("+ ") :
                ip_list.append(line.replace(line[0], "", 1).strip())       
        return ip_list
    
    # Go through each IP in order to validate that each is valid
    list_invalid_ips = validateip(all_ips)

    #Sort the IPs ascending smallest to largest
    sorted_ipfile1 = sort_ips(file1_sanitize)
    sorted_ipfile2 = sort_ips(file2_sanitize)

    # Convert sorted IPs to long version form
    long_ip_file1 = convert_ip_to_long_ip(sorted_ipfile1, list_invalid_ips)
    long_ip_file2 = convert_ip_to_long_ip(sorted_ipfile2, list_invalid_ips)

    # Found IPs are added here
    found_list = []
    # Look for found IPs between the two files
    for ip in long_ip_file1:
        found_ip = binary_search(long_ip_file2, ip)
        if found_ip == None:
            pass
        else:
            found_list.append(ip)
    
    # Take the found list and find the difference between this and the 2nd file
    # Output is converted to strings
    diff_list = ip_difference(found_list, long_ip_file2)
    
    # Iterate through the difference list and convert each long IP to integers then write to file
    for ip in diff_list:
        ip_as_integers = int(ip)
        difference_ips.write(f"{str(ipaddress.ip_address(ip_as_integers))}\n")
        
main()