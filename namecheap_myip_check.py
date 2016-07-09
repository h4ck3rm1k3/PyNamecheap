# needs python3
# sudo apt-get install python3-requests

# Run "nosetests" on command line to run these.
from namecheap import Api, ApiError
#from nose.tools import * # pip install nose
import pprint
#api_key = '' # You create this on Namecheap site
#username = ''
#ip_address = '' # Your IP address that you whitelisted on the site

# If you prefer, you can put the above in credentials.py instead

from credentials import api_key, username, ip_address


#newip = '173.61.181.25'
#oldipv6 =  '2001:0:53aa:64c:41:3e29:52c2:4ae6'
#newipv6 =  '2001:0:53aa:64c:8da:2639:52c2:4ae6'
badnames = ('parkingpage.namecheap.com.'  ) #newipv6
githuba = '192.30.252.153'
githubb = '192.30.252.154'
#            parkingpage.namecheap.com

def dfix(x,h):
        domain_name = x['Name']

        print (h['Name']+"."+x['Name'] +" => To fix")
        api.domains_dns_setHosts(
                        domain_name,
                        [
                                # {
                                #         'HostName' : 'www',
                                #         'RecordType' : 'AAAA',
                                #         'Address': newipv6,
                                #         'MXPref' : '10',
                                #         'TTL' : '100'
                                # },
                                {
                                        'HostName' : 'www',
                                        'RecordType' : 'CNAME',
                                        'Address':  domain_name,
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
import shelve
d = shelve.open("cache")

def proc(x):
  domain_name = x['Name']
  print ("Looking at domain name " + domain_name)

  try :

    # has it the github nameserver a?
    has_a_gha=False
    # has it the github nameserver b?
    has_a_ghb=False
    #has_aaaa_www=False ipv6?

    # has cname?
    has_cname=False

    for h in x['hosts']:

        #if h['Type'] in ('URL301','URL','TXT'):
                #print("Skipping! " + h['Type'] + " because not interesting" )
                #pprint.pprint(h)

        if h['Name'] == '@':
                if h['Type'] == 'A':
                        if h['Address'] == githubb:
                                has_a_ghb = True
                        elif h['Address'] == githuba:
                                has_a_gha = True
                        else:
                                print ("Other:" + h['Name']+"."+x['Name']  + " " + h['Type'] +" =>"+ h['Address'])                        
        elif h['Name'] == 'www':
                if h['Type'] == 'CNAME':
                        if h['Address'] == domain_name + ".":
                                has_cname=True
                        elif h['Address'] in	badnames:
                                # replace
                                pass
                        else:
                                print ("Other cname : " + h['Name']+"."+x['Name']  + " " + h['Type'] +" =>"+ h['Address'])
                        if 'github' in h['Address']:
                                print ('skipping github')
                                return
                        #print (h['Name']+"."+x['Name']  + " " + h['Type'] +" =>"+ h['Address'])
                #elif h['Type'] == 'AAAA':
                #        has_aaaa_www=True
                #        print (h['Name']+"."+x['Name'] + " " + h['Type'] +" =>"+ h['Address'])
                #        #pprint.pprint(h)

                
    # after checking all
    if (not (has_a_ghb and has_a_gha and has_cname)):
            #if (has_a_ghb or has_a_gha or has_cname):
            #print ("Problem with %s\n" % domain_name)
            #pprint.pprint(x)
            #print (" has_aaaa_www :" + str(has_aaaa_www))
            print (" has_a_ghb :" + str(has_a_ghb))
            print (" has_a_gha :" + str(has_a_gha))
            print (" has_cname :" + str(has_cname))

            #pprint.pprint(hosts)
            for h in hosts:
                    print (domain_name + "\t"+ h['Type'] + "\t" + h['Address'])
                    #print("Going to fix! %s\n" % )
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

#pprint.pprint([username, api_key, ip_address])
api = Api(username, api_key, username, ip_address, sandbox=False, debug=False)
#hosts = api.domains_dns_getHosts(domain_name)
#pprint.pprint(api.__dict__)

dlist = api.domains_getList()
domains =  {}
with open ('domains.txt') as f:
        for  l in f.readlines():
                l=l.rstrip("\n")
                #print (l)
                domains[l]={}

#pprint.pprint(dlist.__dict__)
for x in dlist:
        domain_name = x['Name']

        hosts = None

        if( domain_name in d ):
                hosts = d[domain_name]
        else:
                try:
                        hosts = api.domains_dns_getHosts(domain_name)
                        d[domain_name]=hosts
                except Exception as e:
                        print (e)
                        
        x['hosts']=hosts

        if domain_name in domains :
                #pprint.pprint(x)
                proc(x)
        else:
                print ("Skipping " + domain_name)
