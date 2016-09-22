#!/usr/bin/python

import requests
import json
from sys import argv
import collections
import argparse

parser = argparse.ArgumentParser(description='This is a simple Python tool that fetches data from nginx+ status api')
parser.add_argument('--url', help='Example: http://localhost:8080/status',default='http://localhost:8080/status')
parser.add_argument('--key', help='Return a specific key using dot notation')
parser.add_argument('--lld-caches', help='Use Zabbix low level discovery to find all caches', action="store_true")
parser.add_argument('--lld-zones', help='Use Zabbix low level discovery to find all zones', action="store_true")
parser.add_argument('--debug', help='Dumps all the data in dot notation from the status url', action="store_true")
args = parser.parse_args()

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def main():
  global args
  global parser


  r = requests.get(args.url)
  if r.status_code == 200:

    if args.key:
      d = flatten(r.json(),'','.')
      print d[args.key]

    if args.lld_caches:
      s = { 'data': [] }
      d = r.json()
      caches = d['caches']
      for k in caches:
        s['data'].append({'{#CACHE_NAME}':k})
      print json.dumps(s)

    if args.lld_zones:
      s = { 'data': [] }
      d = r.json()
      server_zones = d['server_zones']
      for k in server_zones:
        s['data'].append({'{#SERVER_ZONE}':k})
      print json.dumps(s)

    if args.debug:
      print json.dumps(flatten(r.json(),'','.'), sort_keys=True,indent=4, separators=(',', ': '))

if __name__ == '__main__':
  main()
