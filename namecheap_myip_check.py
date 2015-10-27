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
api = Api(username, api_key, username, ip_address, sandbox=False, debug=True)
#hosts = api.domains_dns_getHosts(domain_name)

dlist = api.domains_getList()

newip = '173.61.181.25'
oldipv6 =  '2001:0:53aa:64c:41:3e29:52c2:4ae6'
newipv6 =  '2001:0:53aa:64c:8da:2639:52c2:4ae6'
badnames = ('parkingpage.namecheap.com.', oldipv6, newipv6 )
githuba = '192.30.252.153'
githubb = '192.30.252.154'
#            parkingpage.namecheap.com

def dfix(x,h):
        domain_name = x['Name']
        print (h['Name']+"."+x['Name'] +" => To fix")
        api.domains_dns_setHosts(
                        domain_name,
                        [
                                {
                                        'HostName' : 'www',
                                        'RecordType' : 'AAAA',
                                        'Address': newipv6,
                                        'MXPref' : '10',
                                        'TTL' : '100'
                                },
                                {
                                        'Address': 'h4ck3rm1k3.github.io.',
                                        'Name': 'www',
                                        'RecordType': 'CNAME',
                                        'MXPref' : '10',
                                        'TTL' : '100'
                                },
                                {
                                        'HostName' : '@',
                                        'RecordType' : 'A',
                                        'Address': githuba,
                                        'MXPref' : '10',
                                        'TTL' : '100'
                                },
                                {
                                        'HostName' : '@',
                                        'RecordType' : 'A',
                                        'Address': githubb,
                                        'MXPref' : '10',
                                        'TTL' : '100'
                                },                                             
                        ]
                )
        pprint.pprint(api.domains_dns_getHosts(domain_name))
    
def proc(x):
  domain_name = x['Name']
  print ("Looking at domain name " + domain_name)
  try :
    hosts = api.domains_dns_getHosts(domain_name)
    has_a_gha=False
    has_a_ghb=False
    has_www=False
    has_aaaa_www=False

    for h in hosts:
        if h['Type'] in ('URL301','URL','TXT'):
                print("Skipping!")
                return
          
        if h['Name'] == '@':
                if h['Type'] == 'A':
                        if h['Address'] == githubb:
                                has_a_ghb = True
                        elif h['Address'] == githubb:
                                has_a_gha = True
                        else:
                                print ("Other" + h['Name']+"."+x['Name']  + " " + h['Type'] +" =>"+ h['Address'])                        
        elif h['Name'] == 'www':
                if h['Type'] == 'CNAME':
                        has_www=True
                        if 'github' in h['Address']:
                                print ('skipping github')
                                return
                        print (h['Name']+"."+x['Name']  + " " + h['Type'] +" =>"+ h['Address'])
                elif h['Type'] == 'AAAA':
                        has_aaaa_www=True
                        print (h['Name']+"."+x['Name'] + " " + h['Type'] +" =>"+ h['Address'])
                        #pprint.pprint(h)

    if (not (has_aaaa_www and has_www and has_a_ghb and has_a_gha)):
            if (has_aaaa_www or has_www or has_www or has_a_ghb or has_a_gha):
                    print ("Problem\n")
                    print (h['Name']+"."+x['Name'] + " " + h['Type'] +" =>"+ h['Address'])
                    pprint.pprint(x)
                    pprint.pprint(h)
                    if h['Address'] in badnames:
                            dfix(x,h)
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

for x in dlist:
  #pprint.pprint(x)
  proc(x)
