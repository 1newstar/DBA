#!/usr/bin/env python
# encoding: utf-8
# author: weiyuanke123@gmail.com
import sys
import os
import time
import getopt
import re
import threading


#mysql命令路径
mysqlcmd = os.popen("find /usr -name mysql -type f 2>/dev/null|head -n 1").read().strip()
if len(mysqlcmd.strip()) == 0:
    print 'no mysql cmd'
    exit(-1)
#采集的数据hoststr ->[var_dict, var_dict, ....]
datadict = {}

def Usage():
    print 'mystatus.py usage:'
    print '-h,--help: print help message.'
    print "-c, --conf: 'host=192.168.1.1port=3306user=accountpassword=123456'"

def parse_host_str(hoststr):
    matchobj = re.match(r'host=(.*)port=(.*)user=(.*)password=(.*)', hoststr)
    if not matchobj:
        return None
    host = matchobj.group(1).strip()
    port = matchobj.group(2).strip()
    user = matchobj.group(3).strip()
    password = matchobj.group(4).strip()
    return (host, port, user, password)

#hoststr事例: host=10.103.38.141port=3306user=accountpassword=`c2#^@j_
def sample_host(host, port, user, password):
    var_dict = {}
    cmd = mysqlcmd + " -u'" + user + "' -h " + host + " -P " +port + " -p'" + password+"' "
    cmd = cmd + ''' -e "show status" 2>/dev/null '''
    output = os.popen(cmd).read().strip();
    for line in output.split('\n'):
        line_split = re.split('\t| ', line);
        if len(line_split) == 2:
            var_dict[line_split[0]] = line_split[1]
    if datadict.has_key(host):
        datadict[host].append(var_dict)
    else:
        datadict[host] = [var_dict]

def show():
    for key in datadict.keys():
        if len(datadict[key]) < 2:
            continue
        time_per = int(datadict[key][-1]['Uptime']) - int(datadict[key][-2]['Uptime'])
        #slow log qps
        Slow_queries_qps = (int(datadict[key][-1]['Slow_queries']) - int(datadict[key][-2]['Slow_queries']))/time_per
        #query qps
        query_qps = (int(datadict[key][-1]['Queries']) - int(datadict[key][-2]['Queries']))/time_per;
        print "host\tSlow\tquery_qps"
        print key+"\t"+str(Slow_queries_qps)+"\t"+str(query_qps)

if __name__ == '__main__':
    hoststrs = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hc:n:')
    except getopt.GetoptError, err:
        Usage()
        sys.exit(2)
    for op, val in opts:
        if op == '-h':
            Usage()
            sys.exit(0)
        elif op == '-c':
            hoststrs = hoststrs + val.split('; ')
        elif op == '-n':
            num_of_iter = int(val)

    if len(hoststrs) == 0:
        Usage()
        sys.exit(0)

    for hoststr in hoststrs:
        (host, port, user, password) = parse_host_str(hoststr)
        sample_host(host, port, user, password)
    time.sleep(2)
    for hoststr in hoststrs:
        (host, port, user, password) = parse_host_str(hoststr)
        sample_host(host, port, user, password)
    show()
