#!/usr/bin/env python      

########## ver 0.1
#
# 0.1 first start
#

import re, sys, argparse
from random import randint

from mftlib import minMax, queryWhois, sn, isisRID, ip

def features():
	print "feature interface-vlan"
	print "license grace-period"
	if igp == "ospf":
		print "feature ospf"
		if ipv6 == True:
			print "feature ospfv3"
	if igp == "isis":
		print "feature isis"
	if mpls:
		print "install feature-set mpls"
		print "feature-set mpls"
		print " feature mpls ldp"
		print "! under vdc"
		print "! allow feature-set mpls"
		if te:
			print "feature mpls traffic-engineering"
	if multicast:
		print "feature pim"
	if vrf != None:
		print "feature mpls l3vpn"
		print "feature bgp"
		print "feature tunnel"
		if multicast:
			if mdt != '':
				print "feature mvpn"

def auth(state=False):
	print
	if state:
		print "username cisco password cisco"
		print 
		print "enable password cisco"
		print 
		print "line console"
		print " login local"
		print " exec-timeout 10"
		print 
	else:
		print "no username cisco password cisco"
		print 
		print "no enable password cisco"
		print 
		print "line console"
		print "  no login local"
		print "  exec-timeout 0"
		print 

def tuningGlobal():
	if tuning == True:
		print "process-max-time 50"
		print "ip routing protocol purge interface"
		print "ip tcp path-mtu-discovery"
		print "ip tcp window-size 65535"

def Global():
	print "logging console"
	print "no ip domain-lookup"
	print 
	print "line console"
	print "  exec-timeout 0"
	print 
	# print "ip bgp new-format"
	# print ""

def tuningInt():
	if tuning == True:
		print "  carrier-delay msec 0"
		if bfd == True:
			print "  bfd int 100 min 100 mult 3"
		
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
		print "mpls label range " + hostNum + "000 " + hostNum + "999"
		print "mpls ldp configuration"
		print "  logging neighbor-changes"
		print "  router-id loopback 0 force"
		print "  no shutdown"
		if te == True:
			print "mpls traffic-eng configuration"
			print "  no shutdown"
		print
#		if igp == "ospf":
#			print "mpls ldp igp sync holddown 10000"
		
def vrf(name, rd, rt):
	print 
	print "vrf context " + name
	print " rd " + rd
	if multicast:
		print " ip pim rp-address " + rp
		if mdt != '':
			print " mdt default " + mdt
			print " mdt source l0"
			print " mdt enforce-bgp-mdt-safi"
	print " address-family ipv4 unicast"
	print "  route-target export " + rt
	print "  route-target import " + rt
	if ipv6:
		print " address-family ipv6 unicast"
		print "  route-target export " + rt
		print "  route-target import " + rt
	print

def mplsInt():
	if mpls == True:	
		 print "  mpls ip"
		 if te == True:
			 print "  mpls traffic-eng tunnel"
			 print "  mpls traffic-eng bandwidth " + rsvp

def pimInt():
	print "  ip pim sparse-mode"

def ipv6Global():
	if ipv6 == True:
		print
#		print "ipv6 unicast-routing"

def multicastGlobal(vrf = ''):
	if vrf == '':
		print "ip pim rp-address " + rp
		print 
	else:
		print 
		
def mplsRouting():
	if mpls == True:
		if igp == "ospf":
			print "  mpls ldp sync"
			if te == True:
				print "  mpls traffic-eng area 0"
				print "  mpls traffic-eng router-id l0"
				if multicast == True:
					print "  mpls traffic-eng multicast-intact"
		else:
			print "  mpls ldp sync"
			if te == True:
				print "  mpls traffic-eng level-" + level
				print "  mpls traffic-eng router-id l0"
				if multicast == True:
					print "  mpls traffic-eng multicast-intact"

if __name__ == "__main__":

	lengh = None
	intf = []
	ospf = "YES"
	isis = "YES"
	area = "0"
	level = "2"
	tuning = "YES"
	module = "2"

	ospf_process = '1'
	isis_process = 'abc'
	
	#telnet = "no"
	#ip = "127.0.0.1"
	
	parser = argparse.ArgumentParser(description='routeGen.py for automatic generation of IOS configuration')
	parser.add_argument('-r','--router', help='router where config parameters',required=False, default=None)
	parser.add_argument('-n','--neighbor', help='neighbor(s) of this router, if multiple use comma , eg. 1,2,3', required=False, default=None)
	
	parser.add_argument('-6','--ipv6', action='store_true', help='add ipv6 unicast routing',required=False, default=False)
	
	parser.add_argument('-i','--interface', help='specify interface media', choices=['eth'], required=False, default="eth")
	parser.add_argument('--int_no', required=False, default="1")
	
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
		#### if no router and neighbor is specified a loop will start to specify dinamically multiple neighbors
		hostName = raw_input("enter router number: ")
		print 
		print "[ Write \'done\' when finish! ]"
		print
		while True:
			num = raw_input("entrer router neighbor: ")
				
			if num != "done":
			
				try:
					intf.append(num)
				except:
					print "Invalid input"
		    
			else:
				break
				
	else:
			
		hostName = router

		for neigh in neighbor.split(','):
			intf.append(neigh)

	intf.sort()

	print
	print "+++++++++"
	print 
	print "BETA RELEASE: not already tested"
	print 
	print "+++++++++"
	print 
	print "conf t"
	print 

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

	print 
	print "interface " + interfaceName + module + "/" + int_no
	print "  switchport"
	print "  switchport mode trunk"
	print "  no shutdown"
	print

	features()
	print

	tuningGlobal()
	Global()
	mplsGlobal()
	# auth(False)
	if igp == None:
		if args.vrf != None:
			vrf(vrf_name, rd, rt)
	ipv6Global()
	if multicast == True:
		if args.vrf != None:
			multicastGlobal(vrf_name)
		else:
			multicastGlobal()
	print

	if args.vrf == None:
		print "interface Loopback0"
		print "  ip add " + lo + "/24"
		if ipv6 == True:
			print "  ipv6 add 2001::" + lo.replace(".", ":") + "/128"
			print "  ipv6 link-local fe80::" + lo.replace(".", ":")
		if igp == "ospf":
			print "  ip router ospf " + ospf_process + " area " + area 
			if ipv6 == True:
				print "  ipv6 router ospfv3 " + ospf_process + " area " + area 
		elif igp == "isis":
			print "  ip router isis " + isis_process
			if ipv6 == True:
				print "  ipv6 router isis " + isis_process
		if multicast == True:
			pimInt()
			print "  ip igmp join " + igmp
		print
	else:
		print "interface Loopback10"
		print "  vrf member " + vrf_name
		print "  ip add " + lo_vrf + "/24"
		if ipv6 == True:
			print "  ipv6 add 2001::" + lo_vrf.replace(".", ":") + "/128"
			print "  ipv6 link-local fe80::10:" + lo_vrf.replace(".", ":")
		if multicast == True:
			pimInt()
			print "  ip igmp join " + igmp
		print 

	for i in range(lengh):
		if hostNum == intf[i]:
			continue
		
		mini, maxi = minMax(hostNum,intf[i])

		print "Vlan " + mini + maxi
		print 
		
		print "interface Vlan " + mini + maxi
		if igp == None:
			if args.vrf != None:
				print " vrf member " + vrf_name
		print "  ip add 10." + mini + "." + maxi + "." + hostNum + "/24"
		if ipv6 == True:
			print "  ipv6 add 2001:10:" + mini + ":" + maxi + "::" + hostNum + "/64"
			print "  ipv6 link-local fe80::10:" + mini + ":" + maxi + ":" + hostNum + " "
		if igp == "ospf":
			print "  ip router ospf " + ospf_process + " area " + area 
			print "  ip ospf network point-to-point"
			if ipv6 == True:
				print "  ipv6 router ospfv3 " + ospf_process + " area " + area 
				print "  ospfv3 network point-to-point"
		elif igp == "isis":
			print "  ip router isis " + isis_process
			print "  isis network point-to-point"
			if ipv6 == True:
				print "  ipv6 router isis " + isis_process
		print "  no shutdown"
		tuningInt()
		mplsInt()
		if multicast == True:
			pimInt()
		print 

	if igp == "ospf":
		print "router ospf " + ospf_process
		print "  log-adjacency-changes"
		print "  router-id " + lo
		tuningRouting()
		mplsRouting()
		print 

		if ipv6 == True:
			print "router ospfv3 " + ospf_process
			print "  log-adjacency-changes"
			print "  router-id " + lo		
		print 
	elif igp == "isis":
		print "router isis " + isis_process
		print "  log-adjacency-changes"
		print "  net 47.000" + area + "." + isisRID(hostNum) + ".00"
#		print "  address-family ipv4 unicast"
#		print "  metric-style wide"
		print "  is-type level-" + level
		tuningRouting()
		mplsRouting()

		if ipv6 == True:
			print "  address-family ipv6 unicast"
			print "   multi-topology"		
	print 