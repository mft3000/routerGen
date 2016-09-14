#!/usr/bin/env python

########### ver 0.5
#
# 0.2 init
# 0.3 add AF vpnv4, vpnv6 in iBGP
# 0.4 add af vrf (-V XXX)
# 0.5 add redistribute 0.0.0.0/0 ge 32 for VRF

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
        print ""
        print "ip bgp new-format"
        print ""
        print "router bgp " + asn
        print " bgp router-id " + rid
        print " no bgp default ipv4"

        if len(neigh_list.split(",")) == 1:

            if af == 4 or af == 46:
                rr = ip(neigh_list)
                print " neigh " + rr + " remote-as " + asn
                print " neigh " + rr + " update-source l0"
                print " !"
                print " add ipv4 unicast"
                print "  network " + rid + " mask 255.255.255.255"
                print "  neigh " + rr + " activate"
                print "  neigh " + rr + " send-community both"
                print "  neigh " + rr + " next-hop-self"
                print " !"
                print " add vpnv4 unicast"
                print "  neigh " + rr + " activate"
                print "  neigh " + rr + " send-community both"
                print " !"
                if af != 4:
                    print " add vpnv6 unicast"
                    print "  neigh " + rr + " activate"
                    print "  neigh " + rr + " send-community both"
                    print " "

            if af == 6 or af == 46:
                rr = ip_v6(neigh_list)
				
                print "router bgp " + asn
                print " neigh " + rr + " remote-as " + asn
                print " neigh " + rr + " update-source l0"
                print " !"
                print " add ipv6 unicast"
                print "  network 2001::" + rid.replace('.',':') + "/128"
                print "  neigh " + rr + " activate"
                print "  neigh " + rr + " send-community both"
                print "  neigh " + rr + " next-hop-self"
                print " "

        else:

            for neigh in neigh_list.split(','):

                if af == 4 or af == 46:
                    rrc_add = ip(neigh)
                    print "router bgp " + asn
                    print " neigh " + rrc_add + " remote-as " + asn
                    print " neigh " + rrc_add + " update-source l0"
                    print " !"
                    print " add ipv4 unicast"
                    print "  network " + rid + " mask 255.255.255.255"
                    print "  neigh " + rrc_add + " activate"
                    print "  neigh " + rrc_add + " send-community both"
                    print "  neigh " + rrc_add + " route-reflector-client"
                    print " !"
                    print " add vpnv4 unicast"
                    print "  neigh " + rrc_add + " activate"
                    print "  neigh " + rrc_add + " send-community both"
                    print "  neigh " + rrc_add + " route-reflector-client"
                    print " !"
                    if af != 4:
                        print " add vpnv6 unicast"
                        print "  neigh " + rrc_add + " activate"
                        print "  neigh " + rrc_add + " send-community both"
                        print "  neigh " + rrc_add + " route-reflector-client"
                        print " "

                if af == 6 or af == 46:
                    rrc_add = ip_v6(neigh)
					
                    print "router bgp " + asn
                    print " neigh " + rrc_add + " remote-as " + asn
                    print " neigh " + rrc_add + " update-source l0"
                    print " !"
                    print " add ipv6 unicast"
                    print "  network 2001::" + rid.replace('.',':') + "/128"
                    print "  neigh " + rrc_add + " activate"
                    print "  neigh " + rrc_add + " send-community both"
                    print "  neigh " + rrc_add + " route-reflector-client"
                    print " "

        if whois is True:

            if af == 4 or af == 46:

                print " add ipv4 unicast"
                print "  redistribute static route-map TAG"

                print " "
                print "route-map TAG permit 10"
                print " match tag 100"
                print " "

                query = "-T route -i origin AS" + asn
                result = queryWhois(query, "whois.ripe.net").split("\n")

                for line in result:
                    if re.search("route:", line):
                        print "ip route " + sn(line.strip("route:          ")) + " null0 tag 100"

            if af == 6 or af == 46:
                print " add ipv6 unicast"
                print "  redistribute static route-map TAG"

                print " "
                print "route-map TAG permit 10"
                print " match tag 100"
                print " "

                query = "-T route6 -i origin AS" + asn
                result = queryWhois(query, "whois.ripe.net").split("\n")

                for line in result:
                    if re.search("route6:", line):
                        print "ipv6 route " + line.strip("route6:          ") + " null0 tag 100"


def ebgpON(router, neigh_list, asn, af, whois, vrf = ''):

    rrc = []
    if bgp == "YES":
        rid = ip(router)
        print ""
        print "ip bgp new-format"
        print ""
        print "router bgp " + asn
        print " bgp router-id " + rid
        print " no bgp default ipv4"

        local = router
        neigh = neigh_list.split(',')[0]

        mini, maxi = minMax(local,neigh)

        if vrf == '':
			if af == 4 or af == 46:
				print " neigh 10." + mini + "." + maxi + "." + neigh + " remote-as " + neigh_list.split(",")[1]
				print " !"
				print " add ipv4 unicast"
				print "  network " + rid + " mask 255.255.255.255"
				print "  neigh 10." + mini + "." + maxi + "." + neigh + " activate"
				print "  neigh 10." + mini + "." + maxi + "." + neigh + " send-comm both"
				print "  "

			if af == 6 or af == 46:
				print "router bgp " + asn
				print " neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " remote-as " + neigh_list.split(",")[1]
				print " !"
				print " add ipv6 unicast"
				print "  network 2001::" + local + ":" + local + ":" + local + ":" + local + "/128"
				print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " activate"
				print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " send-comm both"
				print "  "
        else:
            if af == 4 or af == 46:
                print " !"
                print " add ipv4 vrf " + vrf
                print "  redistribute connected route-map VRF-C-4"
                print "  redistribute static"
                print "  neigh 10." + mini + "." + maxi + "." + neigh + " remote-as " + neigh_list.split(",")[1]
                print "  neigh 10." + mini + "." + maxi + "." + neigh + " activate"
                print "  neigh 10." + mini + "." + maxi + "." + neigh + " send-comm both"
                print "  neigh 10." + mini + "." + maxi + "." + neigh + " as-override"
                print
                print "ip prefix-list VRF-C-4-PFX permit 0.0.0.0/0 ge 32"
                print
                print " route-map VRF-C-4 permit 10"
                print "  match ip address prefix-list VRF-S-4-PFX"

            if af == 6 or af == 46:
                print "router bgp " + asn
                print " !"
                print " add ipv6 vrf " + vrf
                print "  redistribute connected route-map VRF-C-6"
                print "  redistribute static"
                print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " remote-as " + neigh_list.split(",")[1]
                print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " activate"
                print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " send-comm both"
                print "  neigh 2001:10:" + mini + ":" + maxi + "::" + neigh + " as-override"
                print 
                print "ipv6 prefix-list VRF-C-6-PFX permit ::/0 ge 128"
                print
                print " route-map VRF-C-6 permit 10"
                print "  match ipv6 address prefix-list VRF-C-6-PFX"

        if whois == True:
            if af == 4 or af == 46:
                print " !"
                print " add ipv4 unicast"
                print "  redistribute static route-map TAG"

                print " "
                print "route-map TAG permit 10"
                print " match tag 100"
                print " "

                query = "-T route -i origin AS" + asn
                result = queryWhois(query, "whois.ripe.net").split("\n")

                for line in result:
                    if re.search("route:", line):
                        print "ip route " + sn(line.strip("route:          ")) + " null0 tag 100"

            if af == 6 or af == 46:
                print " !"
                print " add ipv6 unicast"
                print "  redistribute static route-map TAG"

                print " "
                print "route-map TAG permit 10"
                print " match tag 100"
                print " "

                query = "-T route6 -i origin AS" + asn
                result = queryWhois(query, "whois.ripe.net").split("\n")

                for line in result:
                    if re.search("route6:", line):
                        print "ipv6 route " + line.strip("route6:          ") + " null0 tag 100"

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