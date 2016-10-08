### changelogs

add XR and NX-OS support!!!

## Introduction 

how many times did you study a topic and then you said... 'hey... let's try it on a lab!!' ?
and how many times (especially for the difficult topics that require a lot of devices), once you finished to set up the lab you forgot what to do?
what can we do to solve this problem?

I write this tool to avoid this situations. Set up a lab, and put hands on it faster is the key for a effective learning.

I don't care about how interconnect the devices... there are much simulators but I don't focus on this (GNS, VIRL, IOL).  
fortunately CCIERS360 and INE courses suggest me how built connections with a smart logic behind.

```
  +-----------------+                        +-----------------+
  |                 |  10.1.2.1/24           |                 |
  |       R1        |  +------------------+  |       R2        |
  |                 |           10.1.2.2/24  |                 |
  +-----------------+        Vlan12          +-----------------+
```

the physical interface will remain always the same (the physical interface where we are connected with the switch) and we'll create some logical subinterfaces to logically connect other devices.
furthermore this will even helps us to understand what device will meet at the other end.
vlan will contains the concatenation two routers names (<>.vlan)

```python
 print "interface e0/0." + min(1,2) + max(1,2)
```
even for ipv4 and ipv6 we find the same logic
```python
 print "ip address 10." + "." + min(1,2) + "." + max(1,2) + "." + router_name + " 255.255.255.0"
 print "ipv6 address 2001::10" + ":" +  min(1,2) + ":" + max(1,2) + ":" + router_name + "/64"
 print "ipv6 address fe80::10" + ":" + min(1,2) + ":" + max(1,2) + ":" + router_name + " link-local"
```
router_name will represents the router no where we are configuring this ip address.

and from this even a loopback (and so on protocols RID) will be predicible
```python
print 'int loopback0'
ptiny ' ip add ' + router_name + "." + router_name + "." + router_name + "." + router_name + " 255.255.255.255"
```
even a simple traceroute can easily show us the router no that packet is passing by easily loking the 4th octect:
```
R1#traceroute 8.8.8.8 numeric so l0
Type escape sequence to abort.
Tracing the route to 8.8.8.8
VRF info: (vrf in name/id, vrf out name/id)
  1 10.1.2.2 3 msec 2 msec 2 msec
  2 10.2.3.3 2 msec 2 msec 2 msec
  3 10.3.4.4 2 msec 2 msec 3 msec
  4 10.4.5.5 2 msec 3 msec 2 msec
  5 10.5.6.6 4 msec 4 msec 3 msec
  6 10.6.7.7 2 msec 2 msec 3 msec
  7 10.7.8.8 3 msec *  2 msec
           ^
           ^
           ^
           |
           |
          ---
```
this logic easily fits behind a single fisical topology (even for virtual labs too): star topology
```
+------------+                                            +------------+
|            |                                            |            |
|     R6     |  +--------------------+ +---------------+  |    R12     |
|            |                       | |                  |            |
+------------+                       | |                  +------------+
                                     | |
+------------+                       | |                  +------------+
|            |                       | |                  |            |
|     R5     |  +------------------+ | | +-------------+  |    R11     |
|            |                     | | | |                |            |
+------------+                     | | | |                +------------+
                                   | | | |
+------------+                     | | | |                +------------+
|            |  +----------------+ + + + + +-----------+  |            |
|     R4     |                                            |    R10     |
|            |                  +----------+              |            |
+------------+                  |          |              +------------+
                                |    SW    |
+------------+                  |          |              +------------+
|            |                  +----------+              |            |
|     R3     |                                            |     R9     |
|            |  +----------------+ + + + + +-----------+  |            |
+------------+                     | | | |                +------------+
                                   | | | |
+------------+                     | | | |                +------------+
|            |                     | | | |                |            |
|     R2     |  +------------------+ | | +-------------+  |     R8     |
|            |                       | |                  |            |
+------------+                       | |                  +------------+
                                     | |
+------------+                       | |                  +------------+
|            |                       | |                  |            |
|     R1     |  +--------------------+ +---------------+  |     R7     |
|            |                                            |            |
+------------+                                            +------------+
```
and this only that the starting point of our lab!

next step is decide how logically interconnect the devices... let's draw our topology :)
```
												PE                  AS65535
                       +------------+         +------------+         +------------+
                       |            |         |            |         |            |
                       |     R4     |  +---+  |     R3     |  +---+  |     R5     |
                       |            |         |            |   RED   |            |
                       +------+-----+         +------+-----+         +------------+
                              |                      |					CE
                              |         AS1234       |
                              |                      |
      CE                      |                      |
+------------+         +------+-----+         +------+-----+         +------------+
|            |         |            |         |            |         |            |
|     R6     |  +---+  |     R1     |  +---+  |     R2     |  +---+  |     R7     |
|            |   RED   |            |         |            |         |            |
+------------+         +------------+         +------------+         +------------+
	AS65535						PE					ASBR         	ASBR 174  
```
and we can try to generate code:
```
$ python routerGen.py -r 1 -n 2

+++++++++

conf t

hostname R1

int e0/0
 no shu

logging console debugging
no ip domain-lookup

line con 0
 privilege level 15
 exec-timeout 0 0

ip cef

int l0
 ip add 1.1.1.1 255.255.255.255

interface e0/0.12
 enc dot 12
 ip add 10.1.2.1 255.255.255.0
```

this the base generated config with no features configured.

## routerGen.py and bgpGen.py

inside main directory you can find many different scripts. The First difference is what configure:

- routerGen.py will generate main device configuration
- bgpGen.py will generate BGP protocol configuration

inside directory you can find other scripts to be used for different cisco os

Main Config | BGP Config | Os
----------- | ---------- | ------------
routerGen.py | bgpGen.py | IOS
routerGenXR.py | bgpGenXR.py | IOS XR
routerGenNX.py | (to be release) | IOS NX-OS

here below you can find routerGen (for IOS, XR, NX) brief script extension descriptions:

 1. enable IPv6 (addresses are generated with a similar logic than IPv4)
 2. change interface name and number (instead of default e0/0 you can change and fit configurations to fisical topology o multiple virtual environments. eg. gi0/1. this can give you flexibility to change virtual environment like VIRL or GNS without problems)
 3. enable IGP (choose OSPF or ISIS). by default none of these are choosen
 4. insert tuning parameters (carrier-delay, edit igp timers, ecc..)
 5. enable MPLS, TE, RSVP (specify RSVP bandwidth per interface)
 6. enable BFD (tuning are needed)
 7. enable Multicast
 8. set static PIM RP
 9. set IGMP address associated to loopbacks

this is an exampled configuration with almost all parameters tuned
```
$ python routerGen.py -r 1 -n 2,4 -I isis -6 -m -t -M -R 2.2.2.2 -G 239.0.0.1

+++++++++


 conf t

hostname R1

int e0/0
 no shu

logging console debugging
no ip domain-lookup

line con 0
 privilege level 15
 exec-timeout 0 0

ip cef
mpls ip
mpls ldp router-id l0 force
mpls label protocol ldp
mpls traffic-eng tunnel	
mpls label range 1000 1999				<=== this parameter is based on router name in order to semplify show LFIB table thsoot ***

ipv6 unicast-routing
ip multicast-routing 
ip pim rp-address 2.2.2.2


int l0
 ip add 1.1.1.1 255.255.255.255
 ipv6 add 2001::1:1:1:1/128
 ip router isis
 ipv6 router isis
 ip pim sparse-mode
 ip igmp join 239.0.0.1

interface e0/0.12
 enc dot 12
 ip add 10.1.2.1 255.255.255.0
 ipv6 add 2001:10:1:2::1/64
 ipv6 add fe80::10:1:2:1 link-local
 ip router isis
 isis network point-to-point
 ipv6 router isis
 mpls ip
 mpls traffic-eng tunnel
 ip rsvp bandwidth 10000
 ip pim sparse-mode

interface e0/0.14
 enc dot 14
 ip add 10.1.4.1 255.255.255.0
 ipv6 add 2001:10:1:4::1/64
 ipv6 add fe80::10:1:4:1 link-local
 ip router isis
 isis network point-to-point
 ipv6 router isis
 mpls ip
 mpls traffic-eng tunnel
 ip rsvp bandwidth 10000
 ip pim sparse-mode

router isis
 log-adjacency-changes
 net 47.0000.0001.0001.0001.00
 metric-style wide
 is-type level-2
 mpls ldp sync
 mpls traffic-eng level-2
 mpls traffic-eng router-id l0
 mpls traffic-eng multicast-intact
 address-family ipv6
  multi-topology
```
*** do you remember last tracert... with the label range space that is changing for every router, even the labels reveals the path.
```
R1#traceroute 9.9.9.9 so l0
Type escape sequence to abort.
Tracing the route to 9.9.9.9
VRF info: (vrf in name/id, vrf out name/id)
  1 10.1.2.2 1 msec 1 msec 0 msec
  2 10.2.3.3 [MPLS: Labels 3007/8011 Exp 0] 3 msec 7 msec 2 msec
  3 10.3.4.4 [MPLS: Labels 4007/8011 Exp 0] 2 msec 2 msec 3 msec
  4 10.4.5.5 [MPLS: Labels 5007/8011 Exp 0] 3 msec 4 msec 4 msec
  5 10.5.6.6 [MPLS: Labels 6009/8011 Exp 0] 3 msec 3 msec 2 msec
  6 10.6.7.7 [MPLS: Labels 7000/8011 Exp 0] 2 msec 2 msec 1 msec
  7 10.8.9.8 [MPLS: Label 8011 Exp 0] 1 msec 1 msec 1 msec
  8 10.8.9.9 2 msec *  3 msec
  
```
this example can easily let you understand the transport label ( x label in x / y traceroute syntax) and how generate the vpn label ( y label in x / y traceroute syntax)
```

R1#sh mpls forwarding-table 
Local      Outgoing   Prefix           Bytes Label   Outgoing   Next Hop    
Label      Label      or Tunnel Id     Switched      interface              
1000       2000       8.8.8.8/32       0             Et0/0.12   10.1.2.2    
1001       2001       7.7.7.7/32       0             Et0/0.12   10.1.2.2    
1002       2002       6.6.6.6/32       0             Et0/0.12   10.1.2.2    
1003       2003       5.5.5.5/32       0             Et0/0.12   10.1.2.2    
1004       2004       4.4.4.4/32       0             Et0/0.12   10.1.2.2    
1005       2005       3.3.3.3/32       0             Et0/0.12   10.1.2.2    
1006       Pop Label  2.2.2.2/32       0             Et0/0.12   10.1.2.2    
1007       2007       10.7.8.0/24      0             Et0/0.12   10.1.2.2    
1008       2008       10.6.7.0/24      0             Et0/0.12   10.1.2.2    
1009       2009       10.5.6.0/24      0             Et0/0.12   10.1.2.2    
1010       2010       10.4.5.0/24      0             Et0/0.12   10.1.2.2    
1011       2011       10.3.4.0/24      0             Et0/0.12   10.1.2.2    
1012       Pop Label  10.2.3.0/24      0             Et0/0.12   10.1.2.2    
```
 
 ```
++++ BACKBONE connections in example

routerGen -r 1 -n 2,4 -I isis -6 -m -t -M -R 2.2.2.2 -G 239.0.0.1
routerGen -r 2 -n 1,3 -I isis -6 -m -t -M -R 2.2.2.2 -G 239.0.0.1
routerGen -r 3 -n 2,4 -I isis -6 -m -t -M -R 2.2.2.2 -G 239.0.0.1
routerGen -r 4 -n 1,3 -I isis -6 -m -t -M -R 2.2.2.2 -G 239.0.0.1

----

```

at this point we can care about another problem... BGP.
another script has been write for this purpose.

this has generate only a BGP specific part of configuration and can be divided in two parts: iBGP and eBGP

1. iBGP (-i), connections are made between loopbacks

a. if -i (iBGP neighbor type --> same ASN) contains a list, router is a RR


```
$ python bgpGen.py -r 2 -a 1234 -46 -i 1,3,4

ip bgp new-format

router bgp 1234
 bgp router-id 2.2.2.2
 no bgp default ipv4
router bgp 1234
 neigh 1.1.1.1 remote-as 1234
 neigh 1.1.1.1 update-source l0
 !
 add ipv4 unicast
  network 2.2.2.2 mask 255.255.255.255
  neigh 1.1.1.1 activate
  neigh 1.1.1.1 send-community both
  neigh 1.1.1.1 route-reflector-client
 !
 add vpnv4 unicast
  neigh 1.1.1.1 activate
  neigh 1.1.1.1 send-community both
  neigh 1.1.1.1 route-reflector-client
 !
 add vpnv6 unicast
  neigh 1.1.1.1 activate
  neigh 1.1.1.1 send-community both
  neigh 1.1.1.1 route-reflector-client
 
router bgp 1234
 neigh 2001::1:1:1:1 remote-as 1234
 neigh 2001::1:1:1:1 update-source l0
 !
 add ipv6 unicast
  network 2001::2:2:2:2/128
  neigh 2001::1:1:1:1 activate
  neigh 2001::1:1:1:1 send-community both
  neigh 2001::1:1:1:1 route-reflector-client
 
...
```
b. if -i (iBGP neighbor type --> same ASN) contains a single number this router is a normal iBGP (like RR client)
```
$ python bgpGen.py -r 1 -a 1234 -46 -i 2

ip bgp new-format

router bgp 1234
 bgp router-id 1.1.1.1
 no bgp default ipv4
 neigh 2.2.2.2 remote-as 1234
 neigh 2.2.2.2 update-source l0
 !
 add ipv4 unicast
  network 1.1.1.1 mask 255.255.255.255
  neigh 2.2.2.2 activate
  neigh 2.2.2.2 send-community both
  neigh 2.2.2.2 next-hop-self
 !
 add vpnv4 unicast
  neigh 2.2.2.2 activate
  neigh 2.2.2.2 send-community both
 !
 add vpnv6 unicast
  neigh 2.2.2.2 activate
  neigh 2.2.2.2 send-community both
 
router bgp 1234
 neigh 2001::2:2:2:2 remote-as 1234
 neigh 2001::2:2:2:2 update-source l0
 !
 add ipv6 unicast
  network 2001::1:1:1:1/128
  neigh 2001::2:2:2:2 activate
  neigh 2001::2:2:2:2 send-community both
  neigh 2001::2:2:2:2 next-hop-self
```
2. eBGP (-e), connections are made between interface specific ip address

let's generate base configuration for router R2 -> R7
```
routerGen -r 2 -n 7
routerGen -r 7 -n 2
```
-e extension accept a list that must contain the neighbor router number an the ASN (Rno,ASN). this will generate the configuration as below
```
$ python bgpGen.py -r 7 -a 174 -46 -e 2,1234

router bgp 174
 bgp router-id 7.7.7.7
 no bgp default ipv4
 neigh 10.2.7.2 remote-as 1234
 !
 add ipv4 unicast
  network 7.7.7.7 mask 255.255.255.255
  neigh 10.2.7.2 activate
  neigh 10.2.7.2 send-comm both
  
router bgp 174
 neigh 2001:10:2:7::2 remote-as 1234
 !
 add ipv6 unicast
  network 2001::7:7:7:7/128
  neigh 2001:10:2:7::2 activate
  neigh 2001:10:2:7::2 send-comm both
```
NOTE: if you specify -w extension... a RIPE DB lookup will be performed (if ASN is a real public ASN) in order to advertise real data and make simulation more realistic
```
$ python bgpGen.py -r 6 -a 174 -46 -e 1,1234 -w

...
 !
 add ipv4 unicast
  redistribute static route-map TAG
 
route-map TAG permit 10
 match tag 100
 
ip route 149.107.0.0 255.255.240.0 null0 tag 100
ip route 149.12.221.0 255.255.255.0 null0 tag 100
ip route 149.242.0.0 255.255.0.0 null0 tag 100
ip route 149.34.48.0 255.255.252.0 null0 tag 100
ip route 149.6.120.0 255.255.255.0 null0 tag 100
ip route 149.71.176.0 255.255.248.0 null0 tag 100
ip route 149.71.56.0 255.255.252.0 null0 tag 100
ip route 149.86.110.0 255.255.254.0 null0 tag 100
ip route 154.44.136.0 255.255.255.0 null0 tag 100
ip route 154.49.209.0 255.255.255.0 null0 tag 100
ip route 154.56.194.0 255.255.254.0 null0 tag 100
ip route 154.60.200.0 255.255.248.0 null0 tag 100
ip route 185.142.236.0 255.255.255.0 null0 tag 100
ip route 185.142.238.0 255.255.255.0 null0 tag 100
ip route 185.16.220.0 255.255.252.0 null0 tag 100
ip route 185.27.202.0 255.255.255.0 null0 tag 100
ip route 185.37.156.0 255.255.255.0 null0 tag 100
ip route 185.37.157.0 255.255.255.0 null0 tag 100
ip route 185.45.132.0 255.255.252.0 null0 tag 100
ip route 185.45.181.0 255.255.255.0 null0 tag 100
ip route 185.45.182.0 255.255.255.0 null0 tag 100
ip route 185.56.180.0 255.255.254.0 null0 tag 100
ip route 185.56.182.0 255.255.254.0 null0 tag 100
ip route 185.68.248.0 255.255.254.0 null0 tag 100
ip route 185.8.140.0 255.255.255.0 null0 tag 100
ip route 185.8.142.0 255.255.255.0 null0 tag 100
ip route 188.64.32.0 255.255.248.0 null0 tag 100
ip route 193.105.197.0 255.255.255.0 null0 tag 100
ip route 193.107.240.0 255.255.252.0 null0 tag 100
ip route 193.108.179.0 255.255.255.0 null0 tag 100
ip route 193.148.7.0 255.255.255.0 null0 tag 100
ip route 193.25.172.0 255.255.255.0 null0 tag 100
ip route 193.29.239.0 255.255.255.0 null0 tag 100
ip route 193.47.84.0 255.255.255.0 null0 tag 100
ip route 193.53.16.0 255.255.255.0 null0 tag 100
ip route 193.53.17.0 255.255.255.0 null0 tag 100
ip route 193.53.18.0 255.255.255.0 null0 tag 100
ip route 193.53.19.0 255.255.255.0 null0 tag 100
ip route 193.53.20.0 255.255.255.0 null0 tag 100
ip route 193.53.21.0 255.255.255.0 null0 tag 100
ip route 193.93.200.0 255.255.252.0 null0 tag 100
ip route 193.96.108.0 255.255.254.0 null0 tag 100
ip route 195.189.178.0 255.255.255.0 null0 tag 100
ip route 195.191.244.0 255.255.254.0 null0 tag 100
ip route 195.20.216.0 255.255.254.0 null0 tag 100
ip route 195.62.74.0 255.255.254.0 null0 tag 100
ip route 195.80.18.0 255.255.255.0 null0 tag 100
ip route 204.34.237.0 255.255.255.0 null0 tag 100
ip route 212.20.128.0 255.255.224.0 null0 tag 100
ip route 213.146.160.0 255.255.224.0 null0 tag 100
ip route 217.71.112.0 255.255.240.0 null0 tag 100
ip route 217.9.192.0 255.255.240.0 null0 tag 100
ip route 31.211.184.0 255.255.248.0 null0 tag 100
ip route 37.157.32.0 255.255.248.0 null0 tag 100
ip route 5.83.240.0 255.255.240.0 null0 tag 100
ip route 80.245.32.0 255.255.224.0 null0 tag 100
ip route 80.91.64.0 255.255.224.0 null0 tag 100
ip route 80.91.75.0 255.255.255.0 null0 tag 100
ip route 81.161.58.0 255.255.255.0 null0 tag 100
ip route 81.2.128.0 255.255.192.0 null0 tag 100
ip route 82.129.0.0 255.255.128.0 null0 tag 100
ip route 82.129.0.0 255.255.192.0 null0 tag 100
ip route 82.129.64.0 255.255.192.0 null0 tag 100
ip route 82.138.64.0 255.255.192.0 null0 tag 100
ip route 82.138.64.0 255.255.254.0 null0 tag 100
ip route 88.151.224.0 255.255.248.0 null0 tag 100
ip route 88.151.231.0 255.255.255.0 null0 tag 100
ip route 90.159.220.0 255.255.252.0 null0 tag 100
ip route 90.159.224.0 255.255.248.0 null0 tag 100
ip route 90.159.232.0 255.255.252.0 null0 tag 100
ip route 90.159.236.0 255.255.252.0 null0 tag 100
ip route 91.189.104.0 255.255.248.0 null0 tag 100
ip route 91.198.26.0 255.255.255.0 null0 tag 100
ip route 91.221.146.0 255.255.255.0 null0 tag 100
ip route 91.221.147.0 255.255.255.0 null0 tag 100
ip route 91.229.180.0 255.255.255.0 null0 tag 100
ip route 92.120.0.0 255.255.0.0 null0 tag 100
ip route 93.190.116.0 255.255.252.0 null0 tag 100
ip route 94.102.192.0 255.255.248.0 null0 tag 100
ip route 95.210.9.0 255.255.255.0 null0 tag 100
 !
 add ipv6 unicast
  redistribute static route-map TAG
 
route-map TAG permit 10
 match tag 100
 
ipv6 route 2001:67c:12e8::/48 null0 tag 100
ipv6 route 2001:978::/32 null0 tag 100
 ```
++++ BGP connections in example
```
bgpGen -r 2 -a 1234 -46 -i 1,3,4 			! RR
bgpGen -r 1 -a 1234 -46 -i 2
bgpGen -r 3 -a 1234 -46 -i 2
bgpGen -r 4 -a 1234 -46 -i 2

routerGen -r 2 -n 7
routerGen -r 7 -n 2
bgpGen -r 2 -a 1234 -4 -e 6,174
bgpGen -r 6 -a 174 -4 -e 1,1234 -w
```
----

The list of extensions of routerGen is not finished... there are some additional configuration that can be usefull in case of MPLS VPN - PE-CE configurations

 10. VRF NAME: this generate VRF definitions and the interface configuration. if you attach other parameters (like multicast, for mVPN) that may refer to VRF... script will generate VRF based configuration. 
 11. mdt multicast address under AF: if VRF is set you can choose a MDT default multicast address to support mVPN configuration

here follows an additional configuration to Router 3 in order to set MPLS VPN PE-CE connection with router 5
```
$ python routerGen.py -r 3 -n 5 -V RED,12874:1 -M -R 5.5.5.5 -6 --mdt 239.123.123.1

+++++++++

...

vrf definition RED
 rd 12874:1
 address-family ipv4 unicast
  mdt default 239.123.123.1
  bgp next-hop l0
  route-target export 12874:1
  route-target import 12874:1
 address-family ipv6 unicast
  route-target export 12874:1
  route-target import 12874:1


ipv6 unicast-routing
ip multicast-routing vrf RED
ip pim vrf RED rp-address 5.5.5.5


int l10
 vrf forwarding RED
 ip add 172.3.3.3 255.255.255.255
 ipv6 add 2001::172:3:3:3/128
 ip pim sparse-mode
 ip igmp join 239.250.0.1

interface e0/0.35
 enc dot 35
 vrf forwarding RED
 ip add 10.3.5.3 255.255.255.0
 ipv6 add 2001:10:3:5::3/64
 ipv6 add fe80::10:3:5:3 link-local
 ip pim sparse-mode
```
 even bgpGen.py has been edit to accept configuration under "address-family ipv4 vrf XXXX" with -V extension
```
router bgp 12874
 bgp router-id 3.3.3.3
 no bgp default ipv4
 !
 add ipv4 unicast vrf RED
  redistribute connected route-map VRF-C-4
  redistribute static
  neigh 10.3.5.5 remote-as 65535
  neigh 10.3.5.5 activate
  neigh 10.3.5.5 send-comm both
  neigh 10.3.5.5 as-override

ip prefix-list VRF-C-4-PFX permit 0.0.0.0/0 ge 32

route-map VRF-C-4 permit 10
 match ip address prefix-list VRF-S-4-PFX

  
router bgp 12874
 !
 add ipv6 unicast vrf RED
  redistribute connected route-map VRF-C-6
  redistribute static
  neigh 2001:10:3:5::5 remote-as 65535
  neigh 2001:10:3:5::5 activate
  neigh 2001:10:3:5::5 send-comm both
  neigh 2001:10:3:5::5 as-override

ipv6 prefix-list VRF-C-6-PFX permit ::/0 ge 128

route-map VRF-C-6 permit 10
 match ipv6 address prefix-list VRF-C-6-PFX
```

normally -V extansion accept only 2 parameters in list (RED,12874:1) and so RD will be the same as RT.
if you specify a third parameter (like -V RED,12874:1,PIC) the RD will be randomly generated from 1 to 65535 and the specified one will be threat as RT
```
vrf definition RED
 rd 12874:64826
 address-family ipv4 unicast
  mdt default 239.123.123.1
  bgp next-hop l0
  route-target export 12874:1
  route-target import 12874:1
 address-family ipv6 unicast
  route-target export 12874:1
  route-target import 12874:1
```
so you can try another features like a PIC Edge that require path diversity.

```
++++ PE - CE in example

routerGen -r 3 -n 5 -V RED,12874:1,PIC -M -R 5.5.5.5 -6 --mdt 239.123.123.1
bgpGen -r 3 -a 12874 -46 -e 5,65535 -V RED
routerGen -r 5 -n 3 -6 -M -R 5.5.5.5 -G 239.250.1.1
bgpGen -r 5 -a 65535 -46 -e 3,12874

routerGen -r 1 -n 6 -V RED,12874:1,PIC -M -R 5.5.5.5 -6 --mdt 239.123.123.1
bgpGen -r 1 -a 12874 -46 -e 6,65535 -V RED
routerGen -r 6 -n 1 -6 -M -R 5.5.5.5 -G 239.250.1.1
bgpGen -r 6 -a 65535 -46 -e 1,12874
```
----

I hope you can understand the potential of this scripts (in one hour I lunch up and running a 20 router lab with Inter-AS opt C scenarion, CSC, TE, ecc...) and I sure this can helps in your road to success.


this code has been written quick and dirty long time ago and now pubblished with new features (vrf, MDT, ecc). is not so good to read but it works.
with lucky I hope to find some spare time to adapt the code for new enhanceds, like support for additional networking OS's (like XR and NX... work in progress), enter the device and drop the config ecc...



please check also (in the future on gitHub)

showRunIOU.py: enter inside router (from a device list: R1:localhost:2001), lunch 'term len 0; show run' save and zip device configuration

ts.py: are you ready for your CCIE Tshoot Lab? really?! why don't you prepare a complex scenario and start to add some random mistakes with this script???
