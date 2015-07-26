#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import print_function
import os, sys

def check_for_root():
	print('cheking for root...',end="")
	if not os.geteuid() == 0:
	    sys.exit('Script must be run as root')
	print("[OK]")

def check_for_binarys(binarys_array=[]):
	paths = os.environ["PATH"].split(':') #Tous les répertoires contenant des executables.
	for needed_binary in binarys_array:
		for path in paths:
			if os.path.isfile(path+'/'+needed_binary[0]):
				needed_binary[1] = True

	for needed_binary in binarys_array:
		print('cheking for '+needed_binary[0]+"...",end="")
		if not needed_binary[1]:
			sys.exit("[error]")
		print("[OK]")

def check_file_exist_and_is_writeateble(file_path=""):
	name = file_path.split('/')[-1] #getting the last element of the file_path
	print('cheking if '+name+' exist...',end="")
	if not os.path.isfile(file_path):
		sys.exit("[error]")
	print("[OK]")
	try:
		print('cheking if '+name+' is writeable...',end="")
		file = open(file_path, "w")
		file.close()
		print("[OK]")
		return True
	except:
		print("[error]")
		return False


if __name__ == "__main__":
	needed_binarys = [['scapy',False], ['iptables',False], ['arpspoof',False]]
	check_for_root()
	check_for_binarys(needed_binarys)
	if not check_file_exist_and_is_writeateble("/proc/sys/net/ipv4/ip_forward"):
		sys.exit("")
