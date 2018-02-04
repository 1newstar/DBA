# coding:utf8

import sys
from collections import OrderedDict

'''
实现一个员工增删改查功能

1. 用户在终端新增用户时输入  姓名，英文名， 年龄， 工号（全局唯一）， 生日，工龄，入职时间、电话号码
2. 工龄时间有python自动计算
3. 用户在终端可以查询用户信息， 通过 姓名、英文名、工号、电话号码， 支持模糊查询最好
4. 删除用户通过工号
5. 支持修改功能， 通过工号修改用户全部信息 （工号排除）， 
6. 程序终止后再次启动任然可以查询之前录入的用户数据


内存中以list存放所有员工信息，每个员工信息用有序dict存放
emp = [ OrderedDict{},OrderedDict{},OrderedDict{}]

存放日志时以字符串存入

'''

class Emp_IDUS():
    def __init__(self,info):
        self.emp = []

        if info == 'I':
            print self.insert_emp()
        elif info == 'D':
            print self.delete_emp()
        elif info == 'U':
            print self.update_emp()
        else:
            emp=self.select_emp()
            print emp
#            for k,v in i.iteritems():
#                print k+':'+v


    def insert_emp(self):
        name = raw_input('姓名:')
        ename = raw_input('英文名:')
        age = raw_input('年龄:')
        eid =raw_input('工号（全局唯一）:')
        birthday=raw_input('生日:')
        hiredate =raw_input('入职时间:')
        hireage = '10'
        tel = raw_input('电话号码:')
        line_list = [name,ename,age,eid,birthday,hiredate,hireage,tel]

        return "ok"


    def delete_emp(self):
        emp = self.load_r()
        info = raw_input('请输入要删除员工id:')
        for i in emp:
            if i['eid'] == info:
                print i
                emp.remove(i)

        for line in emp :
            line_str = ','.join(line.values())
            self.load_w(line_str)

        return "ok"

    def update_emp(self):
        emp = self.load_r()
        info = raw_input('请输入要更新的员工id:')
        for i in emp:
            if i['eid'] == info:
                old_info = i
                emp.remove(i)
        for line in emp :
            line_str = ','.join(line.values())
            self.load_w(line_str)

        an = raw_input('姓名是否需要修改；Y/N ')
        if an == 'Y':
            name = raw_input('姓名:')
        else:
            name = old_info['name']

        an = raw_input('英姓名是否需要修改；Y/N ')
        if an == 'Y':
            ename = raw_input('英姓名:')
        else:
            ename = old_info['ename']

        an = raw_input('年龄是否需要修改；Y/N ')
        if an == 'Y':
            age = raw_input('年龄:')
        else:
            age = old_info['age']

        eid = old_info['eid']

        an = raw_input('生日是否需要修改；Y/N ')
        if an == 'Y':
            birthday = raw_input('生日:')
        else:
            birthday = old_info['birthday']

        an = raw_input('入职时间是否需要修改；Y/N ')
        if an == 'Y':
            hiredate = raw_input('入职时间:')
        else:
            hiredate = old_info['hiredate']

        hireage = '10'

        an = raw_input('电话号码是否需要修改；Y/N ')
        if an == 'Y':
            tel = raw_input('电话号码:')
        else:
            tel = old_info['tel']

        line_list = [name, ename, age, eid, birthday, hiredate, hireage, tel]
        line_str = ','.join(line_list)
        self.load_a(line_str)
        return "ok"

    def select_emp(self):
        emp = self.load_r()
        result = []
        info = raw_input('请输入姓名、英文名、工号、电话号码:')
        for i in emp:
            for k in i.keys():
                if info in i[k]:
                    result.append(i)
        return result






    def save(self,emp):
        with open('emp_file','w') as emp_file:
            emp_file.write(emp+'\n')
        return 1

    def load(self):
        emp = []
        emp_index = ['name','ename','age','eid','birthday','hiredate','hireage','tel']
        emp_file = open('emp_file','r')
        for line_str in  emp_file.readlines():
            emp_dict = OrderedDict()
            j = 0
            for i in line_str.strip().split(','):
                emp_dict[emp_index[j]] = i
                j = j+1
            emp.append(emp_dict)
        return emp






if __name__ == "__main__":
    input_str = '''
            员工增删改查系统
            添加员工信息 I
            删除员工信息 D
            更改员工信息 U
            查看员工信息 S
            正常退出程序 q 
            请输入：
            '''
    while True:
        info = raw_input(input_str)
        if info == 'q':
            sys.exit(0)
        else:
            e = Emp_IDUS(info)


