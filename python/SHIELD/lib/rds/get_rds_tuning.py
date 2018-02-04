# -*- coding:utf-8 -*-


import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancePerformanceRequest
from aliyunsdkrds.request.v20140815 import CreateDiagnosticReportRequest
from aliyunsdkrds.request.v20140815 import DescribeDiagnosticReportListRequest

"""
RDS的用于故障排查的基础信息，不需要登陆到客户RDS后台直接获取即可。
1. 数据库实例的监控信息
2. 数据库实例的检测报告
3. 数据库实例的慢查询日志
"""

class RDS:
    def __init__(self, access_key, access_secret, region):
        self.client = AcsClient(access_key, access_secret, region)

    def get_TotalPages(self, action_name):
        Total = 0
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        request.set_PageSize('10')
        result = json.loads(self.client.do_action_with_exception(request))
        TotalCount = float(result['TotalRecordCount'])
        PageSize = float(result['PageRecordCount'])

        if TotalCount > PageSize:
            try:
                # TotalCount = float(result['TotalCount'])
                # PageSize = float(result['PageSize'])
                return int(round(TotalCount / PageSize))
            except Exception as e:
                print e.message
                return Total
        else:
            return 1

    def get_DescribeDBInstances(self):
        Total = self.get_TotalPages('DescribeInstances')
        for page in xrange(1, Total + 1):
            request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
            request.set_accept_format('json')
            request.set_PageSize('10')
            request.set_PageNumber(page)
            result = json.loads(self.client.do_action_with_exception(request))
            yield result['Items']['DBInstance'] if result['Items'] else []

    def get_DescribeRegions(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        result = json.loads(self.client.do_action_with_exception(request))
        return result['Regions']['RDSRegion']

    def get_DescribeDBInstancePerformance(self, DBInstanceId, key, StartTime, EndTime):
        """
        获取RDS监控数据
        key包含以下项目：
            MySQL_NetworkTraffic	    MySQL实例平均每秒钟的输入流量，MySQL实例平均每秒钟的输出流量。单位为KB。
            MySQL_QPSTPS	            平均每秒SQL语句执行次数，平均每秒事务数
            MySQL_Sessions	            当前活跃连接数，当前总连接数
            MySQL_InnoDBBufferRatio	    InnoDB缓冲池的读命中率，InnoDB缓冲池的利用率，InnoDB缓冲池脏块的百分率
            MySQL_InnoDBDataReadWriten	InnoDB平均每秒钟读取的数据量，InnoDB平均每秒钟写入的数据量。单位为KB
            MySQL_InnoDBLogRequests	    平均每秒向InnoDB缓冲池的读次数，平均每秒向InnoDB缓冲池的写次数
            MySQL_InnoDBLogWrites	    平均每秒日志写请求数，平均每秒向日志文件的物理写次数，平均每秒向日志文件完成的fsync()写数量
            MySQL_TempDiskTableCreates	MySQL执行语句时在硬盘上自动创建的临时表的数量
            MySQL_MyISAMKeyBufferRatio	MyISAM平均每秒Key Buffer利用率，MyISAM平均每秒Key Buffer读命中率，MyISAM平均每秒Key Buffer写命中率
            MySQL_MyISAMKeyReadWrites	MyISAM平均每秒钟从缓冲池中的读取次数，MyISAM平均每秒钟从缓冲池中的写入次数，MyISAM平均每秒钟从硬盘上读取的次数，MyISAM平均每秒钟从硬盘上写入的次数
            MySQL_COMDML	            平均每秒Delete语句执行次数，平均每秒Insert语句执行次数， 平均每秒Insert_Select语句执行次数，平均每秒Replace语句执行次数，平均每秒Replace_Select语句执行次数，平均每秒Select语句执行次数，平均每秒Update语句执行次数
            MySQL_RowDML	            平均每秒从InnoDB表读取的行数，平均每秒从InnoDB表更新的行数，平均每秒从InnoDB表删除的行数，平均每秒从InnoDB表插入的行数，平均每秒向日志文件的物理写次数
            MySQL_MemCpuUsage	        MySQL实例CPU使用率(占操作系统总数)，MySQL实例内存使用率(占操作系统总数)
            MySQL_IOPS	                MySQL实例的IOPS（每秒IO请求次数）
            MySQL_DetailedSpaceUsage	MySQL实例空间占用详情：ins_size实例总空间使用量;data_size数据空间;log_size日志空间;tmp_size临时空间;other_size系统空间
            slavestat	                只读实例延迟
        """
        request = DescribeDBInstancePerformanceRequest.DescribeDBInstancePerformanceRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(DBInstanceId)
        request.set_Key(key)
        request.set_StartTime(StartTime)
        request.set_EndTime(EndTime)
        result = json.loads(self.client.do_action_with_exception(request))
        return result

    def create_DiagnosticReport(self, DBInstanceId, StartTime, EndTime):
        """
        创建诊断报告
        """
        request = CreateDiagnosticReportRequest.CreateDiagnosticReportRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(DBInstanceId)
        request.set_StartTime(StartTime)
        request.set_EndTime(EndTime)
        result = json.loads(self.client.do_action_with_exception(request))
        return result

    def get_DiagnosticReport(self,DBInstanceId):
        """
        获取诊断报告
        :return:
        """
        request = DescribeDiagnosticReportListRequest.DescribeDiagnosticReportListRequest()
        request.set_accept_format('json')
        request.set_DBInstanceId(DBInstanceId)
        result = json.loads(self.client.do_action_with_exception(request))
        return result

if __name__ == '__main__':
    # 测试RAM账号
    api = RDS('', '', '' )
    # xxRAM子账号
    api = RDS('Eh5qex1rw', 'dQ5V2mQjA1cwjDT1DcXIlDITn6ypag', 'cn-shanghai')

    # 获取所有的数据库实例
    #for items in api.get_DescribeDBInstances():
    #    print json.dumps(items)
    # for items in api.get_DescribeDBInstances():
    #    print items

    # 获取数据库实例的所有区域
    # for r in api.get_DescribeRegions():
    #    print r['RegionId']

    # 获取数据库监控信息
    print api.get_DescribeDBInstancePerformance('rm-bp158s78ovw33r1zf','MySQL_QPSTPS,MySQL_COMDML','2018-01-02T15:00Z','2018-01-03T15:00Z')

    # 获取数据库检测报告
    # 通过ram子账号测试
    #print api.get_DiagnosticReport('rr-bp1ks23k451zxjf7r','2018-01-03T10:00Z','2018-01-04T10:00Z')
    # 发通账号测试
    #print api.create_DiagnosticReport('rm-uf649bq2e05ee43ib', '2018-01-11T10:00Z', '2018-01-11T18:00Z')
    print api.get_DiagnosticReport('rm-uf649bq2e05ee43ib')

"""
检测报告返回结果如下：
{u'ReportId': u'10026104', u'RequestId': u'BE48EDD4-A1DF-4225-BD84-177BC57CDF9C-9213'}
{u'ReportList': [{u'DownloadURL': u'', u'EndTime': u'', u'DiagnosticTime': u'2018-01-11T10:50:25Z', u'StartTime': u'', u'Score': 100}, {u'DownloadURL': u'http://rdsreport-shanghai-v2.oss-cn-shanghai.aliyuncs.com/custins5059547/apsaradba_report_1515667455768.pdf?OSSAccessKeyId=LTAITfQ7krsrEwRn&Expires=1515667885&Signature=NsrSNM%2BDch4sWPz8R8h%2Bh1FcYig%3D', u'EndTime': u'2018-01-11T10:00:00Z', u'DiagnosticTime': u'2018-01-11T10:44:15Z', u'StartTime': u'2018-01-10T10:00:00Z', u'Score': 97}], u'RequestId': u'FB1A3AE9-F022-4B1C-AAD5-7E64AA53B973'}
"""