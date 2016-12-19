#!/usr/bin/python2

def read_ipblocklist (filename):

    # retreives the IP blocking inclusion list and reads it into a list
    # returns: that list

    with open(filename) as f:
        lines = f.read().splitlines()

    return lines

def write_ipblocklist(listtowrite, filename):

    # writes a python list of IPs to block to the ip blocking inclusions file

    ipblocklist = open(filename,'w')

    for item in listtowrite:
        ipblocklist.write("%s\n" % item)

    return

def resolve_googleipranges():

    # returns a list of IP ranges for outbound SMTP from Google
    from dns.resolver import Resolver
    sys_r = Resolver()

    # query for the list of domains included in Google's SPF records
    answers = sys_r.query('_spf.google.com', 'TXT')

    # format the returned answer into a list
    rrset = str(answers.rrset)
    spfdomains = rrset.split(' ')

    # return only entries that have "include:"
    # and then split them on the ':' to return only the dns addresses
    spfdomains = [ x for x in spfdomains if 'include:' in x ]
    spfdomains = [ i.split(':', 1)[1] for i in spfdomains ]

    # iterate these to get a full list of IP addresses

    ipranges = list()

    for domain in spfdomains:
        answers = sys_r.query(domain, 'TXT')
        rrset = str(answers.rrset)
        iplist = rrset.split(' ')
        iplist = [ x for x in iplist if 'ip4' in x ]
        iplist = [ i.split(':', 1)[1] for i in iplist]
        ipranges = ipranges + iplist

    return ipranges


def main():
    import subprocess

    IP_BLOCKLIST="/opt/pmx/etc/ip-blocking-exceptions"

    # get a list of domains included in Google's SPF records
    ipranges = resolve_googleipranges()
    allowedips = read_ipblocklist(IP_BLOCKLIST)

    # merge what's currently in the file with the new list
    mergedlist = sorted(list (set(ipranges + allowedips)))

    # write the results into the IP Blocklist Exceptions file
    write_ipblocklist(mergedlist, IP_BLOCKLIST)

    subprocess.call(['/opt/pmx6/bin/pmx-share', '--publication', 'Policy_Inbound', 'sync'], shell=False)

if __name__ == '__main__':
  main()
