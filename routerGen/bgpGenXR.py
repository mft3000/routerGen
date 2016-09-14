#!/usr/bin/env python

######### ver 0.1 draft
#
# 0.1 init
#

import re, sys, argparse

from mftlib import queryWhois, sn, minMax, ip, ip_v6

bgp = "YES"
whois = False
ibgp = "None"
ebgp = "None"
ipv4 = False
ipv6 = False

def ibgpON(router, neigh_list, asn, af, whois):
	rrc = []
	if bgp == "YES":
		rid = ip(router)
		print
		print "router bgp " + asn
		print " bgp router-id " + rid
		print 

		if len(neigh_list.split(",")) == 1:

			if af == 4 or af == 46:
				rr = ip(neigh_list)

				print " address-family ipv4 unicast"
				print "  network " + rid + "/32"
				print " !"
				print " address-family vpnv4 unicast"
				print " !"
				if af != 4:
					print " address-family vpnv6 unicast"
					print " !"
				print " neighbor " + rr
				print "  remote-as " + asn
				print "  update-source l0"
				print "  address-family ipv4 unicast"
				print "   next-hop-self"
				print "  !"
				print "  address-family vpnv4 unicast"
				print "  !"
				if af != 4:
					print "  address-family vpnv6 unicast"
					print "  !"

			if af == 6 or af == 46:
				rr = ip_v6(neigh_list)
				

				print "router bgp " + asn
				print " address-family ipv6 unicast"
				print "  network 2001::" + rid.replace('.',':') + "/128"
				print " !"
				print " neighbor " + rr
				print "  remote-as " + asn
				print "  update-source l0"
				print "  address-family ipv6 unicast"
				print "   next-hop-self"
				print "  !"

		else:

			print " address-family ipv4 unicast"
			print "  network " + rid + "/32"
			print " !"
			print " address-family vpnv4 unicast"
			print " !"
			if af != 4:
				print " address-family vpnv6 unicast"
				print " !"

			for neigh in neigh_list.split(','):

				if af == 4 or af == 46:
					rrc_add = ip(neigh)
					print " neighbor " + rrc_add
					print "  remote-as " + asn
					print "  update-source l0"
					print "  address-family ipv4 unicast"
					print "   route-reflector-client"
					print "  !"
					print "  address-family vpnv4 unicast"
					print "   route-reflector-client"
					print "  !"
					if af != 4:
						print "  address-family vpnv6 unicast"
						print "   route-reflector-client"
						print "  !"

				if af == 6 or af == 46:
					rrc_add = ip_v6(neigh)

					print " address-family ipv6 unicast"
					print "  network 2001::" + rid.replace('.',':') + "/128"
					print " !"
					print " neighbor " + rrc_add
					print "  remote-as " + asn
					print "  update-source l0"
					print "  address-family ipv6 unicast"
					print "   route-reflector-client"
					print "  !"

		if whois == True:
			if af == 4 or af == 46:
				print " !"
				print "router bgp " + asn
				print " address-family ipv4 unicast"
				print "  redistribute static route-policy TAG"

				print
				print "route-policy TAG"
				print " if tag is 100 then"
				print "  pass"
				print " endif"
				print "end-policy"
				print 

				query = "-T route -i origin AS" + asn
				result = queryWhois(query, "whois.ripe.net").split("\n")

				print "router static "
				print " address-family ipv4 unicast"
				for line in result:
					if re.search("route:", line):
						print "  " + sn(line.strip("route:          ")) + " null0 tag 100"

			if af == 6 or af == 46:
				print " !"
				print "router bgp " + asn
				print " address-family ipv6 unicast"
				print "  redistribute static route-policy TAG"

				print
				print "route-policy TAG"
				print " if tag is 100 then"
				print "  pass"
				print " endif"
				print "end-policy"
				print 

				query = "-T route6 -i origin AS" + asn
				result = queryWhois(query, "whois.ripe.net").split("\n")

				print "router static "
				print " address-family ipv6 unicast"
				for line in result:
					if re.search("route6:", line):
						print "  " + line.strip("route6:          ") + " null0 tag 100"


def ebgpON(router, neigh_list, asn, af, whois, vrf = ''):

	rrc = []
	if bgp == "YES":
		rid = ip(router)
		print
		print "route-policy pass"
  		print " pass"
  		print "end-policy"
		print
		print "router bgp " + asn
		print " bgp router-id " + rid
		print 

		local = router
		neigh = neigh_list.split(',')[0]

		mini, maxi = minMax(local,neigh)

		if vrf == '':
			if af == 4 or af == 46:
				print " address-family ipv4 unicast"
				print "  network " + rid + "/32"
				print " !"
				print " neighbor 10." + mini + "." + maxi + "." + neigh
				print "  remote-as " + neigh_list.split(",")[1]
				print "  address-family ipv4 unicast"
				print "   send-community-ebgp"
				print "   route-policy pass in"
				print "   route-policy pass out"
				print "  "

			if af == 6 or af == 46:
				print "router bgp " + asn
				print " address-family ipv6 unicast"
				print "  network 2001::" + local + ":" + local + ":" + local + ":" + local + "/128"
				print " !"
				print " neighbor 2001:10:" + mini + ":" + maxi + "::" + neigh
				print "  remote-as " + neigh_list.split(",")[1]
				print "  address-family ipv6 unicast"
				print "   send-community-ebgp"
				print "   route-policy pass in"
				print "   route-policy pass out"
				print "  "

		else:
			if af == 4 or af == 46:
				print " !"
				print " vrf " + vrf
				print "  rd auto"
				print "  address-family ipv4 unicast "
				print "   redistribute connected route-policy VRF-C-4"
				print "   redistribute static"
				print "  !"
				print "  neighbor 10." + mini + "." + maxi + "." + neigh
				print "   remote-as " + neigh_list.split(",")[1]
				print "   address-family ipv4 unicast"
				print "    send-community-ebgp"
				print "    route-policy pass in"
				print "    route-policy pass out"
				print "    as-override"
				print 
				print "route-policy VRF-C-4"
				print " if destination in (0.0.0.0/0 ge 32) then"
				print "  pass"
				print " endif"
				print "end-policy"
				print

			if af == 6 or af == 46:
				print "router bgp " + asn
				print " !"
				print " vrf " + vrf
				print "  rd auto"
				print "  address-family ipv6 unicast "
				print "   redistribute connected route-policy VRF-C-6"
				print "   redistribute static"
				print "  !"
				print "  neighbor 2001:10:" + mini + ":" + maxi + "::" + neigh
				print "   remote-as " + neigh_list.split(",")[1]
				print "   address-family ipv6 unicast"
				print "    send-community-ebgp"
				print "    route-policy pass in"
				print "    route-policy pass out"
				print "    as-override"
				print 
				print "route-policy VRF-C-6"
				print " if destination in (::/0 ge 128) then"
				print "  pass"
				print " endif"
				print "end-policy"
				print


		if whois == True:
			if af == 4 or af == 46:
				print " !"
				print "router bgp " + asn
				print " address-family ipv4 unicast"
				print "  redistribute static route-policy TAG"

				print
				print "route-policy TAG"
				print " if tag is 100 then"
				print "  pass"
				print " endif"
				print "end-policy"
				print 

				query = "-T route -i origin AS" + asn
				result = queryWhois(query, "whois.ripe.net").split("\n")

				print "router static "
				print " address-family ipv4 unicast"
				for line in result:
					if re.search("route:", line):
						print "  " + sn(line.strip("route:          ")) + " null0 tag 100"

			if af == 6 or af == 46:
				print " !"
				print "router bgp " + asn
				print " address-family ipv6 unicast"
				print "  redistribute static route-policy TAG"

				print
				print "route-policy TAG"
				print " if tag is 100 then"
				print "  pass"
				print " endif"
				print "end-policy"
				print 

				query = "-T route6 -i origin AS" + asn
				result = queryWhois(query, "whois.ripe.net").split("\n")

				print "router static "
				print " address-family ipv6 unicast"
				for line in result:
					if re.search("route6:", line):
						print "  " + line.strip("route6:          ") + " null0 tag 100"

def main():

	parser = argparse.ArgumentParser(description='bgpGen.py for automatic generation of IOS BGP configuration')
	parser.add_argument('-r','--router', help='router where config bgp',required=True)
	parser.add_argument('-a','--asn', help='local AS number', required=True)
	parser.add_argument('-4','--ipv4', action='store_true', help='specify ipv4 address family',required=False)
	parser.add_argument('-6','--ipv6', action='store_true', help='specify ipv6 address family',required=False)
	parser.add_argument('-V','--vrf', help='specify vrf name (PE role)', required=False, default='')
	parser.add_argument('-i','--ibgp', help='specify ibgp neighbor, if multiple use coma , eg 1,3,5', required=False)
	parser.add_argument('-e','--ebgp', help='specify ebgp neighbor, REMOTE,REMOTE_ASN',required=False)
	parser.add_argument('-w','--whois', action='store_true', help='RIR database lookup to install real routes',required=False)
	args = parser.parse_args()

	router = args.router
	ibgp = str(args.ibgp)
	ebgp = str(args.ebgp)
	asn = str(args.asn)
	whois = args.whois
	ipv4 = args.ipv4
	ipv6 = args.ipv6
	vrf = args.vrf

	
	af = 0
	
	if ipv4 == True:
		af = 4
	if ipv6 == True:
		af = 6
	if ipv4 == True and ipv6 == True:
		af = 46
		
	if af == 0:
		print 'no af specified'
		exit()
	
	if ebgp != "None" and ibgp != "None":
		ibgpON(router,ibgp,asn,af,whois)
		ebgpON(router,ebgp,asn,af,whois, vrf)
	elif ebgp != "None":
		ebgpON(router,ebgp,asn,af,whois, vrf)
	elif ibgp != "None":
		ibgpON(router,ibgp,asn,af,whois)

if __name__ == "__main__":
	main()