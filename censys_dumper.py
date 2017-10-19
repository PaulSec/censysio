# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Name:     censys.py
# Purpose:  Censysio API Script
# By:       Originally Jerry Gamblin
# -----------------------------------------------

import argparse
import json
import requests
import sys
import datetime
import csv

class Censys:

    def __init__(self):

        self.API_URL = "https://www.censys.io/api/v1"
        self.UID = "XXXXXXXXXXXXXXX"
        self.SECRET = "XXXXXXXXXXXXXXX"

    def search_certificates(self, query):
        pages = float('inf')
        page = 1

        res = []
        while page <= pages:
            params = {'query' : query, 'page' : page}
            tmp_url = "{}/search/certificates".format(self.API_URL)
            data = requests.post(tmp_url, json=params, auth=(self.UID, self.SECRET)).json()
            for r in data['results']:
                subject_dn = r['parsed.subject_dn'].encode('utf-8')
                issuer_dn = r['parsed.issuer_dn'].encode('utf-8')
                fingerprint_sha256 = r['parsed.fingerprint_sha256']
                try:
                    common_name = subject_dn.split('CN=')[1].split(',')[0]
                except Exception, e:
                    common_name = ""
                tmp = {
                    'common_name': common_name,
                    'subject_dn': subject_dn,
                    'issuer_dn': issuer_dn,
                    'fingerprint_sha256': fingerprint_sha256,
                    'link': 'https://censys.io/certificates/{}'.format(fingerprint_sha256)
                }
                res.append(tmp)

            pages = int(data['metadata']['pages'])
            page += 1
        return res

    def lookup_ip(self, ip):
        url = "https://www.censys.io/api/v1/view/ipv4/{}".format(ip)
        return requests.get(url, auth=(self.UID, self.SECRET)).json()

    def search_ips(self, query):
        pages = float('inf')
        page = 1

        res = []
        while page <= pages:
            params = {'query' : query, 'page' : page}
            tmp_url = "{}/search/ipv4".format(self.API_URL)
            data = requests.post(tmp_url, json=params, auth=(self.UID, self.SECRET)).json()
            for r in data['results']:
                ip = r["ip"]
                proto = r["protocols"]
                proto = [p.split("/")[0] for p in proto]
                proto.sort(key=float)
                protoList = ','.join(map(str, proto))
                tmp = {
                    'ip': ip,
                    'ports': protoList,
                    'country': r.get("location.country", 'N/A'),
                    'province': r.get("location.province", 'N/A'),
                    'link': 'https://censys.io/ipv4/{}'.format(ip)
                }
                res.append(tmp)

            pages = int(data['metadata']['pages'])
            page += 1
        return res

parser = argparse.ArgumentParser(description = 'Censys.io Web Server Search')
parser.add_argument('-ips', '--ips', action="store_true", dest="ips", help='Flag to look for ips', default=False)
parser.add_argument('-certificates', '--certificates', action="store_true", dest="certificates", help='Flag to loog for certificates', default=False)
parser.add_argument('-q', '--query', action="store", dest="query", help='Query to perform', required=True)
parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output file', default=None)
args = parser.parse_args()
censys = Censys()
if args.ips:
    filename = 'results/ips_{}.csv'.format(str(datetime.date.today()))
    res = censys.search_ips(args.query)
elif args.certificates:
    filename = 'results/certificates_{}.csv'.format(str(datetime.date.today()))
    res = censys.search_certificates(args.query)
else:
    sys.exit(0)

if args.output_file:
    keys = res[0].keys()
    with open(filename, 'wb') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(res)
    print "File {} successfuly written.".format(filename)
else:
    print json.dumps(res)