# coding: utf8

import paramiko


class Get_os_info():
    '''
    获取远程服务器的操作系统信息,（OS为Linux）
    '''
    def __init__(self,hostname,port,username,password):
        self.hostname,self.port,self.username,self.password = hostname,port,username,password
        #创建SSH连接日志文件（只保留前一次连接的详细日志，以前的日志会自动被覆盖）  
        #paramiko.util.log_to_file(‘paramiko.log’)  
        self.s = paramiko.SSHClient()  
        #允许连接不在know_hosts文件中的主机
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
        #建立SSH连接  
        self.s.connect(hostname,port,username,password)  
    
    
    def get_os_info(self,cmd):
        stdin,stdout,stderr = self.s.exec_command(cmd)
        return stdout.read()


    def get_os_hardware_infos(self):
        '''
        硬件规格信息:cpu mem disk
        系统发行版本和内核信息:release kernel
        '''
        cmd=['cat /etc/redhat-release','uname -a','lscpu','free','df -h']
        info = ['release','kernel','cpu','mem','disk']
        result=[]
        for i in cmd:
            result.append(self.get_os_info(i))
        os_info_dict = dict(zip(info,result))
        return os_info_dict

    def get_os_old_resource_utilization(self):
        '''
        历史系统资源使用情况
        sar -u 报告CPU的利用率
        sar -q 报告CPU运行队列和交换队列的平均长度
        sar -r 报告内存没有使用的内存页面和硬盘块
        sar -b 报告IOPS的使用情况
        sar -d 报告磁盘的使用情况
        '''
        cmd = ['sar -u','sar -q','sar -r','sar -b','sar -d']
        info = ['cpu_usage_rate','cpu_average_load','mem_usage_rate','iops_usage_rate','disk_usage_rate']
        result = []
        for i in cmd:
            result.append(self.get_os_info(i))
        os_info_dict = dict(zip(info, result))
        return os_info_dict

    def get_os_current_resource_utilization(self):
        '''
        实时系统资源使用情况
        观察系统的进程状态、内存使用、虚拟内存使用、磁盘的IO、中断、上下文切换、CPU使用等
        vmstat 1 5
        监控系统磁盘的IO性能情况
        iostat -dkx 1 5
        统计当前所有的连接数情况
        netstat -nat| awk '{print $6}'| sort | uniq -c
        查出哪个ip地址连接最多
        netstat -na|grep ESTABLISHED|awk '{print $5}'|awk -F: '{print $1}'|sort|uniq -c
        查看占用CPU最大的5个进程
        ps -aux 2> /dev/null |sort -k3nr|head -n 5|awk 'BEGIN{print "%CPU\tPID\tCOMMAD"}{print $4,'\t',$2,'\t',$11}'
        查看占用内存最多的5个进程
        ps -aux 2> /dev/null | sort -k4nr |head -n 5 | awk 'BEGIN{print "%MEM\tPID\tCOMMAD"}{print $4,'\t',$2,'\t',$11}'
        '''
        cmd = ['vmstat 1 5',
               'iostat -dkx 1 5',
               "netstat -nat| awk '{print $6}'| sort | uniq -c",
               "netstat -na|grep ESTABLISHED|awk '{print $5}'|awk -F: '{print $1}'|sort|uniq -c",
               '''ps -aux |sort -k3nr|head -n 5''',
               "ps -aux | sort -k4nr |head -n 5"
        ]
        info = ['a','b','c','d','e','f']
        result = []
        for i in cmd:
            result.append(self.get_os_info(i))
        os_info_dict = dict(zip(info, result))
        return os_info_dict



    def get_os_info_close(self):
        self.s.close()


if __name__ == '__main__':
    get = Get_os_info("106.14.139.35",6622,'root','Uploo00king')
    print get.get_os_hardware_infos()
    print get.get_os_current_resource_utilization()
    print get.get_os_old_resource_utilization()

