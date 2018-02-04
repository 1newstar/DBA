# -*- coding:utf-8 -*-

"""
1. 安装firefox
2. 安装geckodriver解压后放在firefox的安装目录下 https://github.com/mozilla/geckodriver/releases
3. 安装gselenium模块
"""

from selenium import webdriver


class Client:
    def __init__(self):
        self.driver = webdriver.Firefox()

    def login_confluence(self, user, password):
        self.driver.get('https://confluence.jiagouyun.com/login.action?os_destination=%2F')
        self.driver.maximize_window()
        self.driver.find_element_by_name('os_username').send_keys(user)
        self.driver.find_element_by_name('os_password').send_keys(password)
        self.driver.find_element_by_name('login').click()

    def login_kitchen(self,user,password):
        self.driver.get('https://kitchen.cloudcare.cn/#/login')
        self.driver.maximize_window()
        self.driver.find_element_by_name('name').send_keys(user)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_class_name('login-btn').click()

    def login_csos(self,ops,user,password):
        self.driver.get('https://csos.cloudcare.cn/console.html#/login')
        self.driver.maximize_window()
        self.driver.find_element_by_xpath('//input[@type="text"]').send_keys(ops)
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(user)
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//button').click()

    def login_rattic(self,user,password):
        self.driver.get('https://rattic.jiagouyun.com')
        self.driver.maximize_window()
        self.driver.find_element_by_name('auth-username').send_keys(user)
        self.driver.find_element_by_name('auth-password').send_keys(password)
        self.driver.find_element_by_class_name('btn').click()

    def login_git(self,user,password):
        self.driver.get('http://git.jiagouyun.com/users/sign_in')
        self.driver.maximize_window()
        self.driver.find_element_by_name('username').send_keys(user)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_name('button').click()

    def login_bj_moniter(self,user,password):
        self.driver.get('http://bj-monitor.jiagouyun.com/index.php')
        self.driver.maximize_window()
        self.driver.find_element_by_name('name').send_keys(user)
        self.driver.find_element_by_name('password').send_keys(password)
        self.driver.find_element_by_name('enter').click()

if __name__ == '__main__':
    ldapuser = 'weiyaping'
    ldappassword = ''
    login1 = Client()
    login1.login_confluence(ldapuser, ldappassword)
    login2 = Client()
    login2.login_csos('','','')
    login3 = Client()
    login3.login_kitchen('','')
    login4 = Client()
    login4.login_rattic(ldapuser, ldappassword)
    login5 = Client()
    login5.login_git(ldapuser, ldappassword)
    login6 = Client()
    login6.login_bj_moniter(ldapuser, ldappassword)

