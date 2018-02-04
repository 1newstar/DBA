#/usr/local/env python
#coding:utf8
import sys
import os
import mysqlbala
import psutil
import datetime
import time

def print_info(title,content,filename):
	print '\033[1;34;47m'
        print "\n============={0}=====================".format(title)
        print '\033[0m'
        print "{0}信息保存至{1}文件中".format(content,filename)

def print_in_table(infoq,filename):
        with open('info_dir/{0}'.format(filename),'w') as f:
                for i in infoq:
			for j in i:
                        	f.write(str(j)+' | ')
			f.write('\n')
def print_in_kv(infoq,filename):
	with open('info_dir/{0}'.format(filename),'w') as f:
                for i in infoq:
                        line_str = '%-30s%-30s'%(i+':',infoq[i])+'\n'
                        f.write(line_str)
def print_in_knv(infoq,filename):
        with open('info_dir/{0}'.format(filename),'w') as f:
                for i in infoq:
                        line_str = '{0}={1}\n'.format(i[0],i[1])
                        f.write(line_str)

def print_in_v(infoq,filename):
        with open('info_dir/{0}'.format(filename),'w') as f:
                for i in infoq:
                        line_str = '{0}\n'.format(infoq[i])
                        f.write(line_str)
def print_out(filename):
	for i in open('info_dir/'+filename,'r').readlines():
		sys.stdout.write(i)
	print


def info_hardware():
	'''
	硬件规格信息:cpu mem disk
	系统发行版本和内核信息:release kernel
	'''
	hw_info_dict = {}
	cpu = psutil.cpu_count(logical=True)
	mem = psutil.virtual_memory()
	disk = psutil.disk_usage('/')
	release=os.popen('cat /etc/redhat-release').read().strip()
	kernel=os.popen('uname -r').read().strip()

	hw_info_dict['cpu']=cpu
	hw_info_dict['mem']='%.2f'%(mem.total/1024/1024/1024.0)+'G'
	hw_info_dict['disk']='%.2f'%(disk[0]/1024/1024/1024.0)+'G'
	hw_info_dict['rele']=release
	hw_info_dict['kernel']=kernel

	print_in_kv(hw_info_dict,'hardware.info')
	


def info_sysres():
	'''
	系统资源使用信息：cpu mem disk io net process
	'''
	sr_info_dict = {}
	cpu = os.popen('uptime').read().strip()
	mem = psutil.virtual_memory().percent
	disk = psutil.disk_usage('/').percent
	io = os.popen('iostat -kx 1 -c 3').read()
	net = psutil.net_io_counters()
	cputop5 = os.popen("ps aux | sort -k3rn | head -5 | awk '{print $11}'").read()
	memtop5 = os.popen("ps aux | sort -k4rn | head -5 | awk '{print $11}'").read()
	

	sr_info_dict[cpu] = '\033[1;34;47mcpu使用情况:\033[0m\n' + cpu
	sr_info_dict[mem] = '\033[1;34;47mmem使用情况:\033[0m\t\t\t\t' + str(mem) + '%'
	sr_info_dict[disk] = '\033[1;34;47mdisk使用情况:\033[0m\t\t\t\t' + str(disk) + '%'
	sr_info_dict[io] = '\033[1;34;47mio使用情况:\033[0m\n' + io
	sr_info_dict[net] = '\033[1;34;47mnet使用情况:\033[0m\n' + str(net) 
	sr_info_dict[cputop5] = '\033[1;34;47m占用CPU最高的5个进程:\033[0m\n' + cputop5
	sr_info_dict[memtop5] = '\033[1;34;47m占用mem最高的5个进程:\033[0m\n' + memtop5

	psinfo={}
	for i in psutil.pids():
    		p=psutil.Process(i)
    		if p.name() == 'mysqld':
        		psinfo['MySQL进程名'] = p.name()
        		psinfo['进程bin路径'] = p.exe()
        		psinfo['进程状态'] = p.status()
        		psinfo['进程创建时间'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(p.create_time()))
        		psinfo['进程uid信息'] = p.uids()
        		psinfo['进程gid信息'] = p.gids()
        		psinfo['进程CPU时间信息'] = p.cpu_affinity()
        		psinfo['进程内存利用率'] = p.memory_percent()
        		psinfo['进程内存信息'] = p.memory_info()
        		psinfo['进程IO信息'] = p.io_counters()
        		psinfo['进程socket列表'] = p.connections()
        		psinfo['进程开启线程数'] = p.num_threads()	
	print_in_v(sr_info_dict,'sysres.info')	
	print_in_kv(psinfo,'mysqlps.info')

def info_mysql_all(host,user,password,dbname):
	'''
	Mysqld变量的详细信息保存至mysqlvariables.info文件中
	数据库运行状态保存至info.mysqlstatus
	连接情况info.mysqlconn
	'''
	p = mysqlbala.mysqlhelper(host,user,password,dbname)
	my = p.queryAll('show variables')	
        myi = p.queryAll('show engine innodb status')
	mys = p.queryAll('show status;')
	myc = p.queryAll('show full processlist;')
        p.close()
	print_in_knv(my,'mysqlvariables.info')
	print_in_knv(mys,'mysqlstatus.info')	
	print_in_table(myi,'mysqlinnodb.info')
	print_in_table(myc,'mysqlconn.info')

def info_logs():
	'''
	系统和服务的日志信息{
		/*复制一份至info_dir/*/
		/var/log/messages
		error-log
		bin-log
		slow-log
	'''
	os.popen('cp /var/log/messages info_dir')
	os.popen('cp /etc/my.cnf info_dir')
	
	




host='localhost'
user='root'
password='(Uploo00king)'
dbname='uplooking'

if __name__ == "__main__": 
	os.popen('rm -rf info_dir;mkdir info_dir')
	info_hardware()
	info_logs()
	info_sysres()
	info_mysql_all(host,user,password,dbname)
	file_name=os.popen('ls info_dir').readlines()
	print_info('硬件规格信息:cpu mem disk','硬件规格信息','hardware.info')
	print_out('hardware.info')
	print_info('系统和服务日志信息','日志信息','info_dir')
	print_info('系统资源使用信息:cpu mem disk io net process','系统资源使用信息','sysres.info')
	print_out('sysres.info')
	print_info('Mysqld进程的详细信息','mysql进程信息','mysqlps.info')
	print_out('mysqlps.info')
	print_info('MySQL变量的详细信息','变量信息','mysqlvariables.info')
#	print_out('mysqlvariables.info')
	print_info('MySQL整体状态的详细信息','整体状态信息','mysqlstatus.info')
#	print_out('mysqlstatus.info')
	print_info('MySQL_InnoDB状态的详细信息','InnoDB状态','mysqlinnodb.info')
#	print_out('mysqlinnodb.info')
	print_info('MySQL当前所有连接的详细信息','连接信息','mysqlconn.info')
	print_out('mysqlconn.info')

	
		
	


