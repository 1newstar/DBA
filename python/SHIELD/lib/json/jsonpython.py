# -*- coding:utf8 -*-

import random

class json_analyze():
    def __init__(self,links):
        self.links = links
        self.node_dict = {}
        self.link_dict = {}

    def f(self,n):
        """
        获取json中所有节点的信息（hostname,ip,type）以字典的类型存放，key的值为hostname
        :param n: json list
        :return: json list
        """
        for ops in n:
            if ops['link']:
                self.f(ops['link'])
            else:
                k = ops['hostname']
                v = {'hostname':ops['hostname'],'ip':ops['ip'],'type':ops['type']}
                self.node_dict[k]=v
                n.remove(ops)
        while len(n) != 0:
            self.f(n)
        return self.node_dict


    # 获取节点关系
    def r(self,n):
        for ops in n:
            if ops['link']:
                source = ops['hostname']
                for ops_c in ops['link']:
                    destination = ops_c['hostname']
                    k = random.random()
                    self.link_dict[k] = {'source':source,'destination':destination}

                self.r(ops['link'])
        return self.link_dict


if __name__ == "__main__":
    links = [
        {
            'hostname': 'client',
            'ip': '',
            'type': 'internat',
            'link': [
                {
                    'hostname': 'slb01',
                    'ip': '106.1.2.1',
                    'type': 'SLB',
                    'link': [
                        {
                            'hostname': 'web01',
                            'ip': '192.168.1.1',
                            'type': 'ECS',
                            'link': [
                                {
                                    'hostname': 'db01',
                                    'ip': '192.168.2.1',
                                    'type': 'RDS',
                                    'link': None
                                }
                            ]

                        },
                        {
                            'hostname': 'web02',
                            'ip': '192.168.1.2',
                            'type': 'ECS',
                            'link': [
                                {
                                    'hostname': 'db01',
                                    'ip': '192.168.2.1',
                                    'type': 'RDS',
                                    'link': None
                                }
                            ]
                        },
                        {
                            'hostname': 'web03',
                            'ip': '192.168.1.3',
                            'type': 'ECS',
                            'link': [
                                {
                                    'hostname': 'db01',
                                    'ip': '192.168.2.1',
                                    'type': 'RDS',
                                    'link': None
                                }
                            ]
                        }
                    ]
                },
                {
                    'hostname': 'slb02',
                    'ip': '106.1.2.2',
                    'type': 'SLB',
                    'link': [
                        {
                            'hostname': 'app01',
                            'ip': '192.168.1.4',
                            'type': 'ECS',
                            'link': [
                                {
                                    'hostname': 'db02',
                                    'ip': '192.168.2.2',
                                    'type': 'RDS',
                                    'link': None
                                }
                            ]

                        },
                        {
                            'hostname': 'app02',
                            'ip': '192.168.1.5',
                            'type': 'ECS',
                            'link': [
                                {
                                    'hostname': 'db02',
                                    'ip': '192.168.2.2',
                                    'type': 'RDS',
                                    'link': None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    j = json_analyze(links)
    relationship = j.r(links)
    nodes = j.f(links)
    print "所有节点的信息"
    print nodes.values()
    print "所有节点的映射关系"
    print relationship.values()
