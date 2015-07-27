#!/usr/bin/env python
#-*- coding: utf-8 -*-

####################[Libs]##################

from __future__ import print_function
import os, sys


####################[Vars]##################

needed_binarys = [['scapy',False], ['iptables',False], ['arpspoof',False]]
ipforward = "/proc/sys/net/ipv4/ip_forward"


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

def formated_print(string='',length='37',char='.',lchar='\n'):
    the_format = "{0:%s<%s.%s}" % (char,length,length)
    print(B+the_format.format(string)+W,end=lchar)

def check_for_linux():
    formated_print('cheking if it is run on linux',lchar="")
    if sys.platform == "linux" or sys.platform == "linux2":
        print(W+"["+G+"OK"+W+"]")
    else:
        print(W+"["+R+"error"+W+"]")
        sys.exit(1)
        

def check_for_root():
	formated_print('cheking if it is run as root',lchar="")
	if not os.geteuid() == 0:
	    print(W+"["+R+"error"+W+"]")
	    sys.exit(1)
	print(W+"["+G+"OK"+W+"]")

def check_for_binarys(binarys_array=[]):
    paths = os.environ["PATH"].split(':') #Tous les répertoires contenant des executables.
    for needed_binary in binarys_array:
        for path in paths:
            if os.path.isfile(path+'/'+needed_binary[0]):
                needed_binary[1] = True

    for needed_binary in binarys_array:
        formated_print('cheking if '+needed_binary[0]+" is installed",lchar="")
        if not needed_binary[1]:
            print(W+"["+R+"error"+W+"]")
            sys.exit(1)
        print(W+"["+G+"OK"+W+"]")

def check_file_exist_and_is_writeateble(file_path=""):
    name = file_path.split('/')[-1] #getting the last element of the file_path
    formated_print('cheking if '+name+' exist',lchar="")
    if not os.path.isfile(file_path):
        print(W+"["+R+"error"+W+"]")
        sys.exit(1)
    print(W+"["+G+"OK"+W+"]")
    try:
        formated_print('cheking if '+name+' is writeable',lchar="")
        file = open(file_path, "w")
        file.close()
        print(W+"["+G+"OK"+W+"]")
    except:
        print(W+"["+R+"error"+W+"]")
        sys.exit(1)


if __name__ == "__main__":
    check_for_linux()
    check_for_root()
    check_for_binarys(needed_binarys)
    check_file_exist_and_is_writeateble(ipforward)






