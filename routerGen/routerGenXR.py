#!/usr/bin/env python      

######### ver 0.1 draft
#
# 0.1 init
# 

import re, sys, argparse
from random import randint

from mftlib import minMax, queryWhois, sn, isisRID, ip

def tuningGlobal():
	if tuning == True:
		print "process-max-time 50"
		print "ip routing protocol purge interface"
		print "ip tcp path-mtu-discovery"
		print "ip tcp window-size 65535"

def Global():
	print "logging console debugging"
	print "telnet vrf default ipv4 server max-servers 10"
	print ""

def tuningInt():
	if tuning == True:
		print " carrier-delay msec 0"
		
def tuningRouting():
	if tuning == True:
		if igp == "ospf":
			if bfd == True:
				print " bfd all-interfaces"
			else:
				print " no bfd all-interfaces"
			print " timers throttle spf 50 100 5000"
			print " timers throttle lsa all 0 20 1000"
			print " timer lsa arrival 20"
			print " timers pacing flood 15"
			print " passive-interface lo0"
		else:
			if bfd == True:
				print " bfd all-interfaces"
			else:
				print " no bfd all-interfaces"
			print " passive-interface lo0"
		
def mplsGlobal():
	if mpls == True:
		print "mpls ldp "
		print " router-id " + hostNum + "." + hostNum + "." + hostNum + "." + hostNum
		for i in range(lengh):
			if hostNum == intf[i]:
				continue	 
		
			mini, maxi = minMax(hostNum,intf[i])
		
			print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
			print " !"
		print " "
		print "mpls label range 10" + hostNum + "000 10" + hostNum + "999"
		print " "

def vrf(name, rd, rt):
	print 
	print "vrf " + name
	print " address-family ipv4 unicast"
	print "  export route-target " + rt
	print "  import route-target " + rt
	if ipv6:
		print "  !"
		print "  address-family ipv6 unicast"
		print "   export route-target " + rt
		print "   import route-target " + rt
	print ""

def teGlobal():
	if mpls == True:	
		 if te == True:
			 print "mpls traffic-eng "
			 for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
		
				mini, maxi = minMax(hostNum,intf[i])
		
				print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print " !"
			 print " "
			 
			 print "rsvp"
			 for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
		
				mini, maxi = minMax(hostNum,intf[i])
		
				print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
			 	print "  bandwidth " + rsvp
				print " !"
			 print " "

def multicastGlobal(vrf):

	if vrf == '':
		if multicast == True:
			print "multicast-routing"
			print " address-family ipv4"
			for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
			
				mini, maxi = minMax(hostNum,intf[i])
			
				print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print " !"
			print ""
			print "router igmp"
			print "  interface lo0"
			print "   join-group " + igmp
			print ""
			print "router pim"
			print " address-family ipv4"
			for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
			
				mini, maxi = minMax(hostNum,intf[i])
			
				print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print " !"

			print " rp-address " + rp
			print ""
	else:
		if multicast == True:
			print "multicast-routing"
			print " vrf " + vrf
			print "  address-family ipv4"
			if mdt != '':
				print "  mdt default " + mdt
				print "  mdt source l0"
			for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
			
				mini, maxi = minMax(hostNum,intf[i])
			
				print "  interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print "  !"
			print ""
			print "router igmp"
			print "  vrf " + vrf
			print "  interface lo10"
			print "   join-group " + igmp
			print ""
			print "router pim"
			print " vrf " + vrf
			print "  address-family ipv4"
			for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
			
				mini, maxi = minMax(hostNum,intf[i])
			
				print "  interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print "  !"

			print "  rp-address " + rp
			print ""


def mplsRouting():
	if mpls == True:
		if igp == "ospf":
			print " mpls ldp sync"
			if te == True:
				print " mpls traffic-eng router-id l0"
				if multicast == True:
					print " mpls traffic-eng multicast-intact"
				print " area 0"
				print "  mpls traffic-eng"
		else:
			print " mpls ldp sync"
			if te == True:
				print " mpls traffic-eng level-" + level
				print " mpls traffic-eng router-id l0"
				if multicast == True:
					print " mpls traffic-eng multicast-intact"

if __name__ == "__main__":
	lengh = None
	intf = []
	ospf = "YES"
	isis = "YES"
	area = "0"
	level = "2"
	tuning = "YES"
	
	# telnet = "no"
	# ip = "127.0.0.1"
	
	parser = argparse.ArgumentParser(description='routeGenXR.py for automatic generation of IOS XR configuration')
	parser.add_argument('-r','--router', help='router where config parameters',required=False, default=None)
	parser.add_argument('-n','--neighbor', help='neighbor(s) of this router, if multiple use comma , eg. 1,2,3', required=False, default=None)
	
	parser.add_argument('-6','--ipv6', action='store_true', help='add ipv6 unicast routing',required=False, default=False)
	
	parser.add_argument('-i','--interface', help='specify interface media', choices=['gi', 'te'], required=False, default='gi')
	parser.add_argument('--int_no', required=False, default="0")
	
	parser.add_argument('-I','--igp', help='specify to use ospf or isis as igp', choices=['ospf', 'isis'], required=False, default=None)
	parser.add_argument('-T','--tuning', action='store_true', help='IGP Tuning parameters', required=False, default=False)

	parser.add_argument('-m','--mpls', action='store_true', help='use mpls', required=False, default=False)
	parser.add_argument('-t','--te', action='store_true', help='use te', required=False, default=False)
	parser.add_argument('-b','--bw', help='specify different RSVP bw than 10000 (default)', required=False, choices=['1000', '10000', '100000', '1000000'], default='10000')
	
	parser.add_argument('-B','--bfd', action='store_true', help='use bfd (Require -T option)', required=False, default=False)
	
	parser.add_argument('-M','--multicast', action='store_true', help='add multicast routing', required=False, default=False)
	parser.add_argument('-R','--rp', help='specify static RP', required=False, default="1.1.1.1")
	parser.add_argument('-G','--igmp', help='specify join group', required=False, default="239.250.0.1")
	
	parser.add_argument('-V','--vrf', help='spec a VRF name and RD (use , as delimiter), if even use \',PIC\' RD is auto generated', required=False, default=None)
	parser.add_argument('--mdt', help='spec a mdt ip address under VRF', required=False, default='')
	args = parser.parse_args()

	router = args.router
	neighbor = args.neighbor
	igp = args.igp
	ipv6 = args.ipv6
	multicast = args.multicast
	te = args.te
	tuning = args.tuning
	igmp = args.igmp
	rp = args.rp
	mpls = args.mpls
	rsvp = args.bw
	bfd = args.bfd
	interfaceName = args.interface
	int_no = args.int_no
	mdt = args.mdt

	
	if router == None or neighbor == None:
		hostName = raw_input("enter router number: ")
		
		while True:
			num = raw_input("entrer router neighbor: ")
				
			if num != "done":
			
				try:
					intf.append(num)
				except:
					print "Invalid input"
		    
			else:
				break
				
		intf.sort()	
	else:
			
		hostName = router
		list = neighbor
		for count in range(0,len(list.split(","))):
			intf.append(list.split(",")[count])
		intf.sort()

	print ""
	print "+++++++++"
	print ""
	print "conf t"
	print ""
	
	lengh = len(intf)

	hostNum = hostName
	lo = hostNum + "." + hostNum + "." + hostNum + "." + hostNum
	lo_vrf = "172." + hostNum + "." + hostNum + "." + hostNum
	lo_csc = "192." + hostNum + "." + hostNum + "." + hostNum
	
	if igp == None:
		if args.vrf != None:
			try:
				parms = len(args.vrf.split(','))
				if parms == 2:
					vrf_name = args.vrf.split(',')[0].upper()
					rd = args.vrf.split(',')[1]
					rt = args.vrf.split(',')[1]
					if ':' not in rd:
						print "invalid syntax: RD require \"x:x\"" 
						exit()
				else:
					vrf_name = args.vrf.split(',')[0].upper()
					rd = args.vrf.split(',')[1].split(':')[0] + ":" + hostNum + str(randint(1,999))
					rt = args.vrf.split(',')[1]
					if ':' not in rd:
						print "invalid syntax: RD require \"x:x\"" 
						exit()
			except:
				print "invalid sintax: \"VRF,RD\" required" 
				exit()

	print "hostname R" + hostName

	print ""
	print "interface " + interfaceName + "0/0/0/" + int_no
	print " no shut"
	
	print ""
	tuningGlobal()
	Global()
	if igp == None:
		if args.vrf != None:
			vrf(vrf_name, rd, rt)

	if args.vrf == None:
		print "int l0"
		print " ipv4 add " + lo + "/32"
		if ipv6 == True:
			print " ipv6 add 2001::" + lo.replace(".", ":") + "/128"
		print
	else:
		print "interface l10"
		print " vrf " + vrf_name
		print " ipv4 add " + lo_vrf + "/32"
		if ipv6 == True:
			print " ipv6 add 2001::" + lo_vrf.replace(".", ":") + "/128"
		
	print ""

	for i in range(lengh):
		if hostNum == intf[i]:
			continue	 
		
		mini, maxi = minMax(hostNum,intf[i])
		
		print "interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
		print " encapsulation dot1q " + mini + maxi
		if igp == None:
			if args.vrf != None:
				print " vrf " + vrf_name
		print " ipv4 add 10." + mini + "." + maxi + "." + hostNum + " 255.255.255.0"
		if ipv6 == True:
			print " ipv6 add 2001:10:" + mini + ":" + maxi + "::" + hostNum + "/64"
			print " ipv6 add fe80::10:" + mini + ":" + maxi + ":" + hostNum + " link-local"
		print 

	if igp == "ospf":
		print "router ospf abc"
		print " log adjacency changes"
		print " router-id " + lo
		mplsRouting()
		print " area 0"
		print "  int l0"
		print "  !"
		for i in range(lengh):
			if hostNum == intf[i]:
				continue	 
		
			mini, maxi = minMax(hostNum,intf[i])
		
			print "  interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
			print "   network point-to-point"
			print "  !"
			
		tuningRouting()
		print ""

		if ipv6 == True:
			print "router ospfv3 abc"
			print " log adjacency changes"
			print " router-id " + lo
			print " area 0"
			print "  int l0"
			print "  !"
			for i in range(lengh):
				if hostNum == intf[i]:
					continue	 
			
				mini, maxi = minMax(hostNum,intf[i])
			
				print "  interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
				print "   network point-to-point"
				print "  !"	
		print ""
	if igp == "isis":
		print "router isis abc"
		print " net 47.000" + area + "." + isisRID(hostNum) + ".00"
		print " is-type level-" + level
		mplsRouting()
		print " address-family ipv4 unicast "
		print "  metric-style wide"
		print " !"
		if ipv6 == True:
			print " address-family ipv6 unicast"
			# print "  multi-topology"	
			print " !"
		print " interface l0"
		print "  passive "
		print "  address-family ipv4 unicast "
		print "  !"
		if ipv6 == True:
			print "  address-family ipv6 unicast"
			print " !"
			
		for i in range(lengh):
			if hostNum == intf[i]:
				continue	 

			mini, maxi = minMax(hostNum,intf[i])

			print " interface " + interfaceName + "0/0/0/" + int_no + "." + mini + maxi
			print "  hello-padding disable"
			print "  point-to-point"
			print "  address-family ipv4 unicast "
			print "   !"
			if ipv6 == True:
				print "  address-family ipv6 unicast"
				print "   !"
		tuningRouting()
	
	print " "
	mplsGlobal()
	teGlobal()
	if multicast == True:
		if args.vrf != None:
			multicastGlobal(vrf_name)
		else:
			multicastGlobal()
	print
	
	print ""
	print "commit"
	print ""
