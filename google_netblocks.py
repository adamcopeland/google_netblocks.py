def read_ipblocklist (filename):

    # retreives the IP blocking inclusion list and reads it into a list
    # returns: that list

    with open(filename) as f:
        lines = f.read().splitlines()

    return lines

def write_ipblocklist(new_blocklist, filename):

    # writes a python list of IPs to block to the ip blocking inclusions file

    ipblocklist = open(filename,'w')
    for item in new_blocklist:
        ipblocklist.write("%s\n" % item)

    return
