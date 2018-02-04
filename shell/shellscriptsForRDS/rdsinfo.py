# -*- coding:utf-8 -*-

import requests
import json
import time
import datetime

from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815 import DescribeDBInstanceAttributeRequest, DescribeBackupPolicyRequest, \
    DescribeBackupsRequest, DescribeBackupsRequest, DescribeResourceUsageRequest, DescribeDBInstancesRequest, \
    DescribeRegionsRequest, DescribeDBInstancePerformanceRequest, DescribeDBInstanceIPArrayListRequest, \
    DescribeDBInstanceAttributeRequest


data = {
    'Engine': '',   #数据库类型
    'private': '',  #内网地址
    'public': '',   #外网地址
    'DBInstanceId': '',   #主机名
    'CPU': '',
    'MEM': '',
    'RegionId': '',   #地域ID
    'ZoneId': '',     #可用区ID
    'Port': '',
}



class RdsAPI:
    def __init__(self, access_id, access_secret, region):
        self.clt = client.AcsClient(str(access_id), str(access_secret), str(region))

    def get_DescribeRegions(self):
        '获取所有region'
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeRegions')
        return self.clt.do_action(request)

    def get_DescribeDBInstances(self):
        '获取某地域所有RDS'
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeDBInstances')
        return self.clt.do_action_with_exception(request)

    def get_DescribeDBInstanceAttribute(self, DBInstanceId):
        '获取RDS基本属性'
        request = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeDBInstanceAttribute')
        request.set_DBInstanceId(str(DBInstanceId))
        return self.clt.do_action_with_exception(request)



def get_instances(data):
    instances = data['Items']['DBInstance'] if data['Items'].has_key('DBInstance') else []
    DBInstance = [ins['DBInstanceId'] for ins in instances]
    return DBInstance


def get_instance_info(data, project):
    instance = data['Items']['DBInstanceAttribute'] if data['Items'].has_key('DBInstanceAttribute') else []
    #print json.dumps(instance)
    #print instances
    DBInstance = [{
        'Project': project,
        'Engine': ins['Engine'],  # 数据库类型
        'Private': ins['ConnectionString'] if ins['DBInstanceNetType'] == 'Intranet' else '',  # 内网地址
        'Public': ins['ConnectionString'] if ins['DBInstanceNetType'] == 'Internet' else '',  # 外网地址
        'DBInstanceId': ins['DBInstanceId'],  # 主机名
        'CPU': '',
        'MEM': ins['DBInstanceMemory'],
        'DISK': ins['DBInstanceStorage'],
        'DBInstanceClass': ins['DBInstanceClass'],
        'RegionId': ins['RegionId'],  # 地域ID
        'ZoneId': ins['ZoneId'],  # 可用区ID
        'Port': ins['Port'],
    } for ins in instance]

    return DBInstance



d = []

if __name__ == '__main__':

    with open('rds.txt') as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.split(',')
            #print line[0]
            api = RdsAPI(line[2], line[3].strip('\n'), line[1])
            instances = get_instances(json.loads(api.get_DescribeDBInstances()))
            #print api.get_DescribeDBInstanceAttribute('rdsmuyzbenvzfib')
            for instance in instances:
                d.append(get_instance_info(json.loads(api.get_DescribeDBInstanceAttribute(instance)), line[0]))


print '项目名称, 数据库类, 内存, CPU, 磁盘, 地域, 实例ID, 公网地址, 内网地址, 连接端口, 规格'
for x in d:

    for z in x:
        #print z
        print '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}'.format(z['Project'], z['Engine'], z['MEM'] / 1024, z['CPU'], z['DISK'], z['RegionId'], z['DBInstanceId'], z['Public'], z['Private'], z['Port'], z['DBInstanceClass'])