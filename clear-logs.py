# Author Martin Milev
# this script is an example that can be run on each node - to run the script on each node i would recomment to install puppet or some other configuration management tool on the servers - also a GPO is an option;
# This script checks the size of the C:\ drive if it is bellow 20% the script will delete the oldest files from c:\datacache\ dir
# The script is designed to run as a scheduled task each 15 minutes and we need to run it with  account that has permissions to delete files on C\datachache and to list root volume sizes - eg. admin user or NT System acc; or By Puppet ot other configuration management tool that has the needed permissions 
# The script outputs all of his actions to the standard output to capture this actions we can simply use  python.exe clear-logs.py >> C:\logs\clear-logs.txt  from CMD/Powershell - ofc C:\logs folder should exist

from os import path
import os
from shutil import disk_usage
import sys
from datetime import datetime


#using os library to get the total size and free size
#the realpath parameter is / this means that we are quering C: drive;

def GetFreeSpace():
    try:
        total_bytes, used_bytes, free_bytes = disk_usage(path.realpath('/'))
        freespaceprcnt = round(((free_bytes / total_bytes) * 100), 2)
        return (freespaceprcnt)
    except FileNotFoundError:
        print("{} Unable to locate the root Drive C: check if you have read permissions on the C drive ".format(datetime.now()))
        raise
    except:
        print("{} Unexpected error while getting the free disk space for root drive {}".format(datetime.now(), sys.exc_info()[0]))
        raise


if __name__=="__main__":

#looping to the bellow steps until the freespace is above 20% 
    while GetFreeSpace() < 20:
        try:
            os.chdir('C:/datacache') #changing the python working dir - this is only used for simplicity to work with relevant paths and not full paths
            list_of_files = os.listdir('.') # listing all the files in our current dir it will make a list with our files
            oldest_file = min(list_of_files, key=os.path.getctime) # getting the oldest file from the list
            os.remove(oldest_file) #removing the oldest file since this is a cache dir the best way is to remove the oldest cache first 
        except FileNotFoundError:
            print("{} Check if the directory in listdir exist or if you have a read permissions".format(datetime.now()))
            raise
        except:
            print("{} Unexpected error while trying to delete or locate the oldest file {}".format(datetime.now(), sys.exc_info()[0]))
            raise
        print("{} file {} is deleted".format(datetime.now(), oldest_file)) #printing the result to stdout so can be captured from the console
