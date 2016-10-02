# needs python3
# sudo apt-get install python3-requests
from namecheap import Api, ApiError
import pprint
from credentials import api_key, username, ip_address
badnames = ('parkingpage.namecheap.com.'  ) #newipv6
githuba = '192.30.252.153'
githubb = '192.30.252.154'
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

api = Api(username, api_key, username, ip_address, sandbox=False, debug=False)

import yaml
from yaml import load, dump

stream = open("toplevel.yaml", "r")
docs = yaml.load_all(stream)

l = {}

for x in  docs:
    for y in x.keys():
        print y
                
        try:
            l[y]=api.domains_dns_getHosts(y)
        except Exception as e:
            print (e)

output = dump(l, Dumper=Dumper)
print (output)
