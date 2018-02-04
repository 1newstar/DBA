# -*- coding:utf-8 -*-

import sys
import os
import re


class appsfire_web():
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
        pid_list = os.popen(cmd).readlines()[0].split()
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

    def get_httpd(self):
        ip_list = self.get_ip()
        pid_list = self.get_pid(" httpd ")
        pid = pid_list[0]
        sbin = self.get_bin(pid)
        port = self.get_port(pid)
        cmd = "httpd -V"
        for httpd_str in os.popen(cmd).readlines():
            if "Server version" in httpd_str:
                matchobj = re.match('Server version:(.*)',httpd_str)
                version = matchobj.group(1).strip()
            elif "HTTPD_ROOT" in httpd_str:
                matchobj = re.match(' -D HTTPD_ROOT="(.*)"',httpd_str)
                dir = matchobj.group(1) + '/'
            elif "SERVER_CONFIG_FILE" in httpd_str:
                matchobj = re.match(' -D SERVER_CONFIG_FILE="(.*)"',httpd_str)
                conf = matchobj.group(1)
            elif "DEFAULT_ERRORLOG" in httpd_str:
                matchobj = re.match(' -D DEFAULT_ERRORLOG="(.*)"',httpd_str)
                log = matchobj.group(1)
        conf = dir + conf
        log = dir + log
        httpd_detail = self.analyze_httpd(conf)
        # 找到拓展配置路径
        cmd = """grep "Include.*conf" /etc/httpd/conf/httpd.conf | awk '{print $2}'"""
        conf_extend = os.popen(cmd).readlines()[0].strip()
        # 找到所有的拓展配置文件
        dir_extend = dir + conf_extend[:-6]
        for filename in os.listdir(dir_extend):
            file = dir_extend + filename
            result = self.analyze_httpd(file)
            httpd_detail = httpd_detail + result
        # 循环所有配置文件过滤，并汇总结果


        self.datalist.append({'ip': ip_list, 'pid': pid, 'port': port, 'bin': sbin, 'version': version, 'conf': conf, 'log': log,'httpd_detail':httpd_detail})
        return self.datalist

    def analyze_httpd(self,file):
        httpd_list = []
        for line in open(file, 'r').readlines():
            if re.match('#|^$', line):
                continue
            else:
                httpd_list.append(line.strip())

        num = []
        n = {}
        for i in range(len(httpd_list)):
            if "<VirtualHost" in httpd_list[i]:
                n['start'] = i
            elif "</VirtualHost>" in httpd_list[i]:
                n['end'] = i
                num.append(n)
                n = {}
        final_list = []
        for i in num:
            final_list.append(httpd_list[i['start']:i['end'] + 1])
        httpd = []
        for item in final_list:
            httpd_dict = {}
            for i in item:
                if "<VirtualHost" in i:
                    matchops = re.match('<VirtualHost.*:(.*)>', i)
                    httpd_dict['ServerPort'] = matchops.group(1).strip()
                elif "DocumentRoot" in i:
                    matchops = re.match('DocumentRoot(.*)', i)
                    httpd_dict['DocumentRoot'] = matchops.group(1).strip()
                elif "ServerName" in i:
                    matchops = re.match('ServerName(.*)', i)
                    httpd_dict['ServerName'] = matchops.group(1).strip()
                elif "ErrorLog" in i:
                    matchops = re.match('ErrorLog(.*)', i)
                    httpd_dict['ErrorLog'] = matchops.group(1).strip()
                elif "CustomLog" in i:
                    matchops = re.match('CustomLog(.*)', i)
                    httpd_dict['CustomLog'] = matchops.group(1).strip()
            httpd.append(httpd_dict)
        return httpd




    def get_nginx(self):
        pass



if __name__ == "__main__":
    ops = appsfire_web()
    print ops.get_httpd()

"""
[{'bin': '/usr/sbin/httpd', 'version': 'Apache/2.2.15 (Unix)', 'httpd_detail': [{'CustomLog': 'logs/ks.toberoot.com-access_log common', 'ServerName': 'ks.toberoot.com', 'ErrorLog': 'logs/ks.toberoot.com-error_log', 'ServerPort': '80', 'DocumentRoot': '/var/www/ks'}, {'CustomLog': 'logs/www.wordpress.com-access_log common', 'ServerName': 'blog.toberoot.com', 'ErrorLog': 'logs/www.wordpress.com-error_log', 'ServerPort': '80', 'DocumentRoot': '/var/www/wordpress'}], 'log': '/etc/httpd/logs/error_log', 'conf': '/etc/httpd/conf/httpd.conf', 'ip': ['172.19.106.62'], 'pid': '25657', 'port': '80'}]
"""