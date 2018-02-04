# coding:utf8

from flask import Flask, request, render_template,jsonify
from get_os_info import *
from get_mysql_tuning import *
from time import strftime,gmtime


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/linux', methods=['GET'])
def linux_form():
    name = 'linux'
    return render_template('linux_form.html',name=name)


@app.route('/linux', methods=['POST'])
def linux():
    hostname = request.form['hostname']
    port = request.form['port']
    username = request.form['username']
    password = request.form['password']
    s = Get_os_info(hostname, int(port), username, password)
    a = s.get_os_hardware_infos()
    return render_template('linux.html', a=a, hostname=hostname)


@app.route('/linuxmoniter', methods=['GET'])
def linuxmoniter_form():
    name = 'linuxmoniter'
    return render_template('linux_form.html',name=name)


@app.route('/linuxmoniter', methods=['POST'])
def linuxmoniter():
    hostname = request.form['hostname']
    port = request.form['port']
    username = request.form['username']
    password = request.form['password']
    s = Get_os_info(hostname, int(port), username, password)
    a = s.get_os_old_resource_utilization()
    return render_template('linuxmoniter.html', a=a, hostname=hostname)

@app.route('/linuxcurrent', methods=['GET'])
def linuxcurrent_form():
    name = 'linuxcurrent'
    return render_template('linux_form.html',name=name)


@app.route('/linuxcurrent', methods=['POST'])
def linuxcurrent():
    hostname = request.form['hostname']
    port = request.form['port']
    username = request.form['username']
    password = request.form['password']
    s = Get_os_info(hostname, int(port), username, password)
    a = s.get_os_current_resource_utilization()
    return render_template('linuxcurrent.html', a=a, hostname=hostname)




@app.route('/mysqlcheck', methods=['GET'])
def mysqlcheck_index():
    return render_template('index_mysqlcheck.html')


@app.route('/mysqlcheck',methods=['POST'])
def mysqlcheck_data():
    dbhostname = request.form['dbhostname']
    dbport = request.form['dbport']
    dbusername = request.form['dbusername']
    dbpassword = request.form['dbpassword']
    dbname = request.form['dbname']
    now_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    s = Get_mysql_tuning(dbhostname, int(dbport), dbusername, dbpassword,dbname)
    a = s.get_mysql_tuning()
    s.close()
    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return render_template('data_check.html', a=a, dbhostname=dbhostname,now_time=now_time,current_time=current_time)




if __name__ == '__main__':
    app.run(debug=True)

