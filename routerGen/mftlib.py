#!/usr/bin/env python      

###### ver 0.2
#
# 0.1 init
# 0.2 add whois
#

import socket, select, string

def minMax(varA,varB):
	if int(varA) < int(varB):
		return varA, varB
	elif int(varA) > int(varB):
		return varB, varA
		
def isisRID(var):
	if int(var) < 10:
		var = "000" + var + "." + "000" + var + "." + "000" + var
	else:
		var = "00" + var + "." + "00" + var + "." + "00" + var
	return var
	
def ip(var):
	var = var + "." + var + "." + var + "." + var
	return var
	
def ip_v6(var):
	var = "2001::" + var + ":" + var + ":" + var + ":" + var
	return var

def sn(var):
	net = var.split("/")
	A = net[0]
	B = net[1]
	
	if B == "1":
		mask = "128.0.0.0"
	elif B == "2":
		mask = "192.0.0.0"
	elif B == "3":
		mask = "224.0.0.0"
	elif B == "4":
		mask = "240.0.0.0"
	elif B == "5":
		mask = "248.0.0.0"
	elif B == "6":
		mask = "252.0.0.0"
	elif B == "7":
		mask = "254.0.0.0"
	elif B == "8":
		mask = "255.0.0.0"
	elif B == "9":
		mask = "255.128.0.0"
	elif B == "10":
		mask = "255.192.0.0"
	elif B == "11":
		mask = "255.224.0.0"
	elif B == "12":
		mask = "255.240.0.0"
	elif B == "13":
		mask = "255.248.0.0"
	elif B == "14":
		mask = "255.252.0.0"
	elif B == "15":
		mask = "255.254.0.0"
	elif B == "16":
		mask = "255.255.0.0"
	elif B == "17":
		mask = "255.255.128.0"
	elif B == "18":
		mask = "255.255.192.0"
	elif B == "19":
		mask = "255.255.224.0"
	elif B == "20":
		mask = "255.255.240.0"
	elif B == "21":
		mask = "255.255.248.0"
	elif B == "22":
		mask = "255.255.252.0"
	elif B == "23":
		mask = "255.255.254.0"
	elif B == "24":
		mask = "255.255.255.0"
	elif B == "25":
		mask = "255.255.255.128"
	elif B == "26":
		mask = "255.255.255.192"
	elif B == "27":
		mask = "255.255.255.224"
	elif B == "28":
		mask = "255.255.255.240"
	elif B == "29":
		mask = "255.255.255.248"
	elif B == "30":
		mask = "255.255.255.252"
	elif B == "31":
		mask = "255.255.255.254"
	elif B == "32":
		mask = "255.255.255.255"

	return A + " " + mask
	
def queryWhois(query, server='whois.ripe.net'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            s.connect((server, 43))
        except socket.error, (ecode, reason):
            if ecode==errno.EINPROGRESS:
                continue
            elif ecode==errno.EALREADY:
                continue
            else:
                raise socket.error, (ecode, reason)
            pass
        break                                            

    ret = select.select ([s], [s], [], 30)

    if len(ret[1])== 0 and len(ret[0]) == 0:
        s.close()
        raise TimedOut, "on data"           

    s.setblocking(1)
		
    s.send("%s\n" % query)
    page = ""
    while 1:
        data = s.recv(8196)
        if not data: break
        page = page + data
        pass

    s.close()

    if string.find(page, "IANA-BLK") != -1:
        raise 'no match'

    if string.find(page, "Not allocated by APNIC") != -1:
        raise 'no match'

    return page