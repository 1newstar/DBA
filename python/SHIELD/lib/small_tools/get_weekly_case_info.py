# -*- coding: UTF-8 -*-

import json
import requests


class ReportAPI:
    def __init__(self):
        self.access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2NsYWltcyI6eyJpbmZvIjp7InVzZXJuYW1lIjoia2VmYXRvbmciLCJkbiI6InVpZD1rZWZhdG9uZyxvdT1ZdW53ZWksb3U9WkhVWVVOLGRjPWppYWdvdXl1bixkYz1jb20iLCJjcmVhdGVfdGltZSI6IjIwMTctMDYtMDkgMTc6MTM6MzkiLCJuYW1lIjpudWxsLCJyb2xlcyI6W10sInBob25lIjpudWxsLCJtYWlsIjoia2VmYXRvbmdAamlhZ291eXVuLmNvbSIsImxhc3Rfc2VlbiI6IjIwMTctMTAtMTkgMTA6MDg6NDkiLCJpZCI6MjM5LCJsb2NhdGlvbiI6bnVsbH19LCJqdGkiOiIyZDA5NTc2NS1hZGNhLTRiZTctYTQwYi0wOWE4ZDdjYTUxOTciLCJleHAiOjE1Mzk5MTQ5MjksImZyZXNoIjpmYWxzZSwiaWF0IjoxNTA4Mzc4OTI5LCJ0eXBlIjoiYWNjZXNzIiwibmJmIjoxNTA4Mzc4OTI5LCJpZGVudGl0eSI6MjM5fQ.22Vh97TLzUvFy-nAuJXa6R96KD-9s5Y2X6-p0lmF80A'
        self.url = 'https://kitchen.cloudcare.cn/#/login'
        self.headers = {
            'Authorization': self.access_token,
            'Content-Type': 'application/json'
        }

    # 查询所有该部门成员
    def get_user(self, email):
        url = self.url + '/api/admin/user/show/by_email?user_email=' + email
        response = requests.get(url, headers=self.headers)
        return response.json()

    # 查询所有部门
    def modify_user(self, user_id, customer_id, user_type):
        url = self.url + '/api/admin/user/modify'
        data = {
            'user_id': user_id,
            'customer_id': customer_id,
            'user_type': user_type
        }

        response = requests.patch(url, data=json.dumps(data), headers=self.headers)
        return response.json()

    def get_customer(self, customer_name):
        url = self.url + '/api/admin/customer/base/show/by_name?customer_name=' + customer_name
        response = requests.get(url, headers=self.headers)
        return response.json()