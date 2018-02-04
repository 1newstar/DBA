# -*- coding:utf-8 -*-

import sys
import os
import re



class appsfire_database():
    def __init__(self):
        self.datalist = []

    def get_ip(self):
        cmd = "ip addr|grep inet|awk '{print $2}'|awk -F '/' '{print $1}'|grep -v '127'"
        ip_list = []
        for ip in os.popen(cmd).readlines():
            ip_list.append(ip.strip())
        return ip_list

    def get_pid(self,daemon):
        cmd = "pidof " + daemon
        try:
            pid_list = os.popen(cmd).readlines()[0].split()
        except IndexError:
            pid_list = None
        else:
            pid_list.sort()
        return pid_list

    def get_bin(self,pid):
        cmd = "ls -l /proc/" + pid + "/exe | awk '{print $11}'"
        sbin = os.popen(cmd).readlines()[0].strip()
        return sbin

    def get_port(self,pid):
        cmd = "ss -luntp|grep '," + pid + "' | awk '{print $5}'|awk -F ':' '{print $2}'"
        port = os.popen(cmd).readlines()[0].strip()
        return port

    def get_mysql(self):
        ip_list = self.get_ip()
        pid_list = self.get_pid("mysqld")
        if pid_list == None:
            return self.datalist
        else:
            for pid in pid_list:
                pid = pid.strip()
                sbin = self.get_bin(pid)
                port = self.get_port(pid)
                cmd = "mysqld -V"
                version = os.popen(cmd).readlines()[0].strip()

                cmd = "ps -ef | grep mysql[d] |grep -v 'mysqld_safe'"
                pid_str = os.popen(cmd).readlines()[0].strip()
                if '--defaults-file=' in pid_str:
                    matchobj = re.match(r'.*--defaults-file=(.*)--basedir=(.*)--datadir=(.*)--plugin-dir=(.*)--user=(.*)--log-error=(.*)--pid-file=.*',pid_str)
                    conf = matchobj.group(1).strip()
                    basedir = matchobj.group(2).strip()
                    datadir = matchobj.group(3).strip()
                    log = matchobj.group(6).strip()
                else:
                    matchobj = re.match(r'.*--basedir=(.*)--datadir=(.*)--plugin-dir=(.*)--user=(.*)--log-error=(.*)--pid-file=.*',pid_str)
                    basedir = matchobj.group(1).strip()
                    datadir = matchobj.group(2).strip()
                    log = matchobj.group(5).strip()
                    conf_list = ["/etc/my.cnf", "/etc/mysql/my.cnf", "/usr/etc/my.cnf", "{0}/my.cnf".format(basedir),"~/.my.cnf"]
                    for i in conf_list:
                        if os.path.exists(i):
                            conf = i
                            break
                self.datalist.append({'ip': ip_list, 'pid': pid, 'port': port, 'bin': sbin, 'version': version, 'conf': conf,'datadir': datadir, 'log': log})
            return self.datalist

    def get_redis(self):
        ip_list = self.get_ip()
        pid_list = self.get_pid("redis-server")
        if pid_list == None:
            return self.datalist
        else:
            for pid in pid_list:
                pid = pid.strip()
                sbin = self.get_bin(pid)
                port = self.get_port(pid)
                cmd = "redis-cli -p " + port + " info"
                result = os.popen(cmd).read()
                if 'NOAUTH Authentication required' not in result:
                    for line in os.popen(cmd).readlines():
                        data = line.strip()
                        r_version = re.match('redis_version:(.*)', data)
                        if r_version is not None:
                            version = r_version.group(1).strip()
    
                        r_conf = re.match('config_file:(.*)', data)
                        if r_conf is not None:
                            conf = r_conf.group(1).strip()
    
                    # datadir,log
                    for line in open(conf, 'r').readlines():
                        data = line.strip()
                        r_datadir = re.match('dir(.*)', data)
                        if r_datadir is not None:
                            datadir = r_datadir.group(1).strip()
                        r_log = re.match('logfile(.*)', data)
                        if r_log is not None:
                            log = r_log.group(1).strip()
                else:
                    password = raw_input('plz input password（redis-server on port:{0}）:'.format(port))
                    version, conf, datadir, log = self.appsfire_redis_auth(port, password)
    
                self.datalist.append({'ip': ip_list, 'pid': pid, 'port': port, 'bin': sbin, 'version': version, 'conf': conf,'datadir': datadir, 'log': log})
            return self.datalist

    def appsfire_redis_auth(self,port, password):
        cmd = "redis-cli  -p " + port + " -a " + password + " info"
        for line in os.popen(cmd).readlines():
            data = line.strip()
            r_version = re.match('redis_version:(.*)', data)
            if r_version is not None:
                version = r_version.group(1).strip()
            r_conf = re.match('config_file:(.*)', data)
            if r_conf is not None:
                conf = r_conf.group(1).strip()
        for line in open(conf, 'r').readlines():
            data = line.strip()
            r_datadir = re.match('dir(.*)', data)
            if r_datadir is not None:
                datadir = r_datadir.group(1).strip()
            r_log = re.match('logfile(.*)', data)
            if r_log is not None:
                log = r_log.group(1).strip()
        return (version, conf, datadir, log)

    def get_mongo(self):
        pass

    def get_oracle(self):
        pass




if __name__ == "__main__":
    ops = appsfire_database()
    ops.get_mysql()
    ops.get_redis()
    for i in ops.datalist:
        print i
"""
plz input password（redis-server on port:6380）:zyadmin
{'bin': '/usr/sbin/mysqld', 'datadir': '/var/lib/mysql', 'version': 'mysqld  Ver 5.7.18 for Linux on i686 (MySQL Community Server (GPL))', 'log': '/var/log/mysqld.log', 'conf': '/tmp/my.cnf', 'ip': ['172.19.106.62'], 'pid': '6489', 'port': '3306'}
{'bin': '/usr/local/bin/redis-server', 'datadir': '/alidata/redis/data/6379', 'version': '3.2.9', 'log': '/alidata/redis/log/redis6379.log', 'conf': '/alidata/redis/conf/redis6379.conf', 'ip': ['172.19.106.62'], 'pid': '15872', 'port': '6379'}
{'bin': '/usr/local/bin/redis-server', 'datadir': '/alidata/redis/data/6380', 'version': '3.2.9', 'log': '/alidata/redis/log/redis6380.log', 'conf': '/alidata/redis/conf/redis6380.conf', 'ip': ['172.19.106.62'], 'pid': '16827', 'port': '6380'}
"""