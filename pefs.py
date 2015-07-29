#!/usr/bin/env python
#-*- coding: utf-8 -*-

####################[Libs]##################

from __future__ import print_function
import os, sys, subprocess, re


####################[Vars]##################

needed_binarys = [
                    ['scapy',False],
                    ['iptables',False],
                    ['arpspoof',False],
                    ['netstat',False],
                    ['sslstrip',False],
                    ['timeout', False]
                 ]
ipv4forward = "/proc/sys/net/ipv4/ip_forward"
ipv4_regex = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"


###################[Colors]#################

W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple
C = '\033[36m'  # cyan
GR = '\033[37m'  # gray

##################[Functions]###############


def check_for_strings_value(list_of_value=[]):
    for elem in list_of_value:
        if not isinstance(elem, str):
            return False
    return True 

def print_ok():
    print(W+"["+G+"OK"+W+"]")
def print_err():
    print(W+"["+R+"error"+W+"]")
def print_timeout():
    print(W+"["+O+"Timeout"+W+"]")

def formated_print(string='',length='60',char='.',lchar='\n',color=GR,align="<"):
    if not check_for_strings_value([string,length,char,lchar]):
        sys.exit("\n\n"+R+"formated_print should only get strings as input!"+W)
    the_format = "{0:%s%s%s.%s}" % (char,align,length,length)
    print(color+the_format.format(string)+W,end=lchar)

def check_for_linux():
    formated_print('cheking if it is run on linux',lchar="")
    if sys.platform == "linux" or sys.platform == "linux2":
        print_ok()
    else:
        print_err()
        sys.exit(1)
        

def check_for_root():
	formated_print('cheking if it is run as root',lchar="")
	if not os.geteuid() == 0:
	    print_err()
	    sys.exit(1)
	print_ok()

def check_for_binarys(binarys_array=[]):
    if not isinstance(binarys_array,list):
        sys.exit("\n\n"+R+"binary array should only be a list"+W)
    paths = os.environ["PATH"].split(':') #Tous les répertoires contenant des executables.
    for needed_binary in binarys_array:
        for path in paths:
            if os.path.isfile(path+'/'+needed_binary[0]):
                needed_binary[1] = True

    for needed_binary in binarys_array:
        formated_print('cheking if '+needed_binary[0]+" is installed",lchar="")
        if not needed_binary[1]:
            print_err()
            sys.exit(1)
        print_ok()

def check_file_exist_and_is_writeateble(file_path=""):
    name = file_path.split('/')[-1] #getting the last element of the file_path
    formated_print('cheking if '+name+' exist',lchar="")
    if not os.path.isfile(file_path):
        print_err()
        sys.exit(1)
    print_ok()
    try:
        formated_print('cheking if '+name+' is writeable',lchar="")
        file = open(file_path, "w")
        file.close()
        print_ok()
    except:
        print_err()
        sys.exit(1)


def runcommand_with_timeout(command=[],timeout="3"):
    if not isinstance(command,list):
        sys.exit("\n\n"+R+"comands are ment to be a list"+W)
    formated_print('running '+' '.join(command)+" ",lchar="",color=B)
    command[:0] = ["timeout",timeout]
    proc = subprocess.Popen(command, bufsize=0, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode == 124:
        print_timeout()
    elif proc.returncode == 0:
        print_ok()
    else:
        print_err()
    return stdout, stderr, proc.returncode

def get_gateways():
    formated_print("Gathering network info",align="^")
    stdout, stderr, rcode = runcommand_with_timeout(["hostname", "-I"])
    if rcode != 0:
        sys.exit("\n\n"+R+"Warning! could not run netstat, exiting..."+W)
    ip_patern = re.compile(ipv4_regex)
    for elem in stdout.split("\n"):
        if len(elem) == 0: continue
        tmp = elem.strip()
        test = ip_patern.match(tmp.strip())
        if test:
           print("Acceptable ip address")
        else:
           print("Unacceptable ip address")
        


def checking_function():
    formated_print("Cheking for requirements",align="^")
    check_for_linux()
    check_for_root()
    check_for_binarys(needed_binarys)
    check_file_exist_and_is_writeateble(ipv4forward)


if __name__ == "__main__":
    checking_function()
    get_gateways()





