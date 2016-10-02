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

dlist = api.domains_getList()
from yaml import load, dump
l = {}
for x in dlist:
        
        domain_name = x['Name']

#        print (domain_name)
        
        # try:
        #         x['hosts']=api.domains_dns_getHosts(domain_name)
        # except Exception as e:
        #         print (e)
        
        l[domain_name]=x
        #pprint.pprint(x)

output = dump(l, Dumper=Dumper)
print (output)
