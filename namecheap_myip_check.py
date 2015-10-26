# Run "nosetests" on command line to run these.
from namecheap import Api, ApiError
#from nose.tools import * # pip install nose
import pprint
#api_key = '' # You create this on Namecheap site
#username = ''
#ip_address = '' # Your IP address that you whitelisted on the site

# If you prefer, you can put the above in credentials.py instead

from credentials import api_key, username, ip_address

pprint.pprint([username, api_key, ip_address])
api = Api(username, api_key, username, ip_address, sandbox=False, debug=False)
#hosts = api.domains_dns_getHosts(domain_name)

dlist = api.domains_getList()

oldipv6 =  '2001:0:53aa:64c:41:3e29:52c2:4ae6'
newipv6 =  '2001:0:53aa:64c:8da:2639:52c2:4ae6'
badnames = ('parkingpage.namecheap.com.', oldipv6)
#            parkingpage.namecheap.com
for x in dlist:
  #pprint.pprint(x)
  domain_name = x['Name']
  try :
    hosts = api.domains_dns_getHosts(domain_name)
    #pprint.pprint(hosts)
    for h in hosts:
      if h['Name'] == 'www':
        print (h['Name']+"."+x['Name'] +" =>"+ h['Address'])
        if h['Address'] in badnames:
          print (h['Name']+"."+x['Name'] +" => To fix")
          api.domains_dns_setHosts(
                  domain_name,[{'HostName' : 'www',
                                'RecordType' : 'AAAA',
                                'Address': newipv6,
                                'MXPref' : '10',
                                'TTL' : '100'}])


  except Exception as e:
        if str(e) ==(
                        '2030288 - Cannot complete this command as'
                        ' this domain is not using proper DNS servers'
        ) :
                print ("\nswitchdns\n")
                api.domains_dns_setDefault(domain_name)
        else:
                print ("\nException\n")
                print (e)
