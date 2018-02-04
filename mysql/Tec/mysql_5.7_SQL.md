# SQL语句练习

[TOC]

> 练习sql语句，不经常用就容易忘记哦！

练习环境如下：

| 环境       | 说明           |
| :------- | :----------- |
| OS       | rhel7.2      |
| database | MySQL 5.7.17 |

## 练习环境搭建

```shell
[root@mastera ~]# ls /software
employees_db-full-1.0.6.tar.bz2  mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz  mysql_scripts.zip
[root@mastera ~]# unzip /software/mysql_scripts.zip -d /software
Archive:  /software/mysql_scripts.zip
  inflating: /software/create.sql    
  inflating: /software/populate.sql  
[root@mastera ~]# ls /software
create.sql                       mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz  populate.sql
employees_db-full-1.0.6.tar.bz2  mysql_scripts.zip
[root@mastera ~]# mysql -uroot -p'(Uploo00king)' -e 'create database booboo'
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@mastera ~]# mysql -uroot -p'(Uploo00king)' booboo < /software/create.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
[root@mastera ~]# mysql -uroot -p'(Uploo00king)' booboo < /software/populate.sql 
mysql: [Warning] Using a password on the command line interface can be insecure.
```

## SQL 数据类型

* 所谓建表：就是声明列的过程
* 数据是以文件的形式存放在硬盘（或内存）
* 列：不同的列类型占的空间不一样
* 选列的原则：够用，又不浪费

列的类型分为：数值型、字符型、日期/时间型

```flow
st=>start: 建表
i=>inputoutput: 数据类型
cond1=>condition: 数值
cond2=>condition: 字符串
cond3=>condition: 时间日期
o1=>inputoutput: 整数|浮点数|定点数|bit
o2=>inputoutput: char|set|json
o3=>inputoutput: date|time|year

e=>end
st->i->cond1
cond1(yes)->o1->e
cond1(no)->cond2
cond2(yes)->o2->e
cond2(no)->cond3
cond3(yes)->o3->e


```

### 数值型

数值型分为整数（6）、定点数（2）、浮点数（3）、bit（1）

```flow
st=>start: 数值型
i=>inputoutput: 分类
cond1=>condition: 整数
cond2=>condition: 定点数
cond3=>condition: 浮点数
cond4=>condition: bit
o1=>inputoutput: int
o2=>inputoutput: decimal|numeric
o3=>inputoutput: float|double
o4=>inputoutput: bit
e=>end
st->i->cond1
cond1(yes)->o1->e
cond1(no)->cond2
cond2(yes)->o2->e
cond2(no)->cond3
cond3(yes)->o3->e
cond3(no)->cond4
cond4(yes)->o4->e
```

#### 整数

| 类型        | 字节   | 位    | 无符号        | 有符号            |
| --------- | ---- | ---- | ---------- | -------------- |
| tinyint   | 1    | 8    | 0 ~ 2^8-1  | -2^7 ~ 2^7-1   |
| smallint  | 2    | 16   | 0 ~ 2^16-1 | -2^15 ~ 2^15-1 |
| mediumint | 3    | 24   | 0 ~ 2^24-1 | -2^23 ~ 2^23-1 |
| int       | 4    | 32   | 0 ~ 2^32-1 | -2^31 ~ 2^31-1 |
| bigint    | 8    | 64   | 0 ~ 2^64-1 | -2^63 ~ 2^63-1 |

**数学推算**

> tinyint 微小的列类型，1字节，由开发人员规定的字节数

```shell
[0][0][0][0][0][0][0][0]-->[1][1][1][1][1][1][1][1]
```

如果表示正数

```shell
2^0 + 2^1 + 2^3 + ... + 2^7 = 2^8 - 1 = 255	0 ~ 255
```

如果表示负数，可以用最高位来标识符号位，1代表-，0代表+

```shell
2^0 + 2^1 + 2^3 + ... + 2^6 = 2^7 - 1 =127 	-128 ~ 127（只有后7位表示绝对值，最高位表示的是符号。其中+0和-0是一样的，所以可以用来表示-128）
```

1. `unsigned`属性决定，有该属性则表示无符号位，无则表示有符号位
2. `zerofill`属性决定，是否补0，并自动为该列添加UNSIGNED属性
3. `M`属性决定，存在补0时，补0的位数
4. `default`属性，声明默认值
5. `not null`属性，不为空

#### 浮点型

| 类型                    | 字节   | 位    | 无符号  | 有符号  |
| --------------------- | ---- | ---- | ---- | ---- |
| float(M,D)            | 4    | 32   |      |      |
| real(M,D)             |      |      |      |      |
| Double precision(M,D) | 8    | 64   |      |      |



* M 精度（总位数，不包含小数点） 取值范围为0~255。FLOAT只保证6位有效数字的准确性，所以FLOAT(M,D)中，M<=6时，数字通常是准确的。如果M和D都有范围后的处理同decimal。
* D  标度（小数位）取值范围为0~30，同时必须<=M。double只保证16位有效数字的准确性，所以DOUBLE(M,D)中，M<=16时，数字通常是准确有明确定义，其超出范围后的处理同decimal。

#### 定点型

**numeric(M,D)  decimal(M,D)**

其中M表示十进制数字总的个数，D表示小数点后面数字的位数

例如 `decimal(5,2)`的取值范围为999.99 ~ 999.99。

* 如果存储时，整数部分超出了范围（如上面的例子中，添加数值为1000.01），MySql就会报错,不允许存这样的值。
* 如果存储时，小数点部分若超出范围，就分以下情况：
 1. 若四舍五入后，整数部分没有超出范围，则只警告，但能成功操作并四舍五入删除多余的小数位后保存。如999.994实际被保存若四舍五入后，整数部分超出范围，则MySql报错，并拒绝处理。如999.995和999.995都会报错。
 2. M的默认取值为10，D默认取值为0。如果创建表时，某字段定义为decimal类型不带任何参数，等同于decimal(10,0)。带一个参数时M的取值范围为1~65，取0时会被设为默认值，超出范围会报错。
 3. D的取值范围为0~30，而且必须<=M，超出范围会报错。

所以，很显然，当M=65，D=0时，可以取得最大和最小值。

**浮点和定点字节是固定的，一般是4个或者8个字节**

#### BIT

* BIT数据类型可用来保存位字段值。BIT(M)类型允许存储M位值。M范围为1~64，默认为1。
* BIT其实就是存入二进制的值，类似010110。

1. 如果存入一个BIT类型的值，位数少于M值，则左补0.
2. 如果存入一个BIT类型的值，位数多于M值，MySQL的操作取决于此时有效的SQL模式：
3. 如果模式未设置，MySQL将值裁剪到范围的相应端点，并保存裁减好的值。
4. 如果模式设置为traditional(“严格模式”)，超出范围的值将被拒绝并提示错误，并且根据SQL标准插入会失败。


### 字符型

>  **字符**

* 1个英文字符 = 1位 = 8 字节
* 1个中文字符 = 2位 = 18字节 (utf8)

#### 字符串

| 类型      | 宽度   | 可存字符 | 实存字符 | 实占空间              | 利用率                        |
| ------- | ---- | ---- | ---- | ----------------- | -------------------------- |
| char    | M    | M    | i    | M                 | i/M<=100%                  |
| varchar | M    | M    | i    | i 字符 + ( 1~2 ) 字节 | i/i 字符 + ( 1~2 ) 字节 < 100% |



**区别**：

1. char：定长，char(M)，M代表宽度，即可容纳的字符数 M ~ [ 0 , 255] 约2W~6W个字符，受字符集影响

2. varchar：变长，varchar(M)，M代表宽度，即可容纳的字符数

3. 定长速度比变长快

4. 变长能够保留末尾空格，而定长会忽略

   **选择原则**

   1. *空间效率*—— 例如：四字成语 char(4)；个人微博140字 varchar(140)
   2. *速度* ——例如：用户名 char(n)

   ​

#### 二进制字符

BINARY和VARBINARY类型类似于CHAR和VARCHAR类型，但是不同的是，它们存储的不是字符字符串，而是二进制串。**所以它们没排序和比较基于列值字节的数值值。**

当保存BINARY值时，在它们右边填充0x00(零字节)值以达到指定长度。取值时不删除尾部的字节。比较时所有字节很重要（因为空的，0x00<空格），包括ORDER BY和DISTINCT操作。比如插入'a '会变成'a \0'。

对于VARBINARY，插入时不填充字符，选择时不裁剪字节。比较时所有字节很重要。

当类型为BINARY的字段为主键时，应考虑上面介绍的存储方式。



#### 文本

> 字符文本——tinytext|mediumtext|text|longtext
> 二进制文本——tinyblob|mediumblob|blob|longblob

BLOB列被视为二进制字符串。TEXT列被视为字符字符串，类似CHAR和BINARY。
在TEXT或BLOB列的存储或检索过程中，不存在大小写转换。

BLOB和TEXT在以下几个方面不同于VARBINARY和VARCHAR：

1. 当保存或检索BLOB和TEXT列的值时不删除尾部空格。(这与VARBINARY和VARCHAR列相同）。
2. 比较时将用空格对TEXT进行扩充以适合比较的对象，正如CHAR和VARCHAR。
3. 对于BLOB和TEXT列的索引，必须指定索引前缀的长度。对于CHAR和VARCHAR，前缀长度是可选的。
4. BLOB和TEXT列不能有默认值。

MySQL Connector/ODBC将BLOB值定义为LONGVARBINARY，将TEXT值定义为LONGVARCHAR。

BLOB或TEXT对象的最大大小由其类型确定，但在客户端和服务器之间实际可以传递的最大值由可用内存数量和通信缓存区大小确更改max_allowed_packet变量的值更改消息缓存区的大小，但必须同时修改服务器和客户端程序。

每个BLOB或TEXT值分别由内部分配的对象表示。

| 类型        | 字节   | 位    | 长度         |
| --------- | ---- | ---- | ---------- |
| tiny      | 1    | 8    | 0 ~ 2^8-1  |
| blob/text | 2    | 16   | 0 ~ 2^16-1 |
| medium    | 3    | 24   | 0 ~ 2^24-1 |
| log       | 4    | 32   | 0 ~ 2^32-1 |


#### ENUM

MySQL中的ENUM是一个字符串对象，其值来自表创建时在列规定中显式枚举的一列值。

可以插入空字符串""和NULL：
* 如果你将一个非法值插入ENUM(也就是说，允许的值列之外的字符串)，将插入空字符串以作为特殊错误值。该字符串与“普通”空字符串有数值值0。
  *如果将ENUM列声明为允许NULL，NULL值则为该列的一个有效值，并且默认值为NULL。如果ENUM列被声明为NOT NULL，其默的第1个元素。

**值的索引规则如下：**

* 来自列规定的允许的值列中的值从1开始编号。
* 空字符串错误值的索引值是0。所以，可以使用下面的SELECT语句来找出分配了非法ENUM值的行：`mysql> SELECT * FROM tbl_enum_col=0;`
* NULL值的索引是NULL。

NUM最多可以有65,535(2^16-1)个元素。当创建表时，ENUM成员值的尾部空格将自动被删除。

#### SET

SET是一个字符串对象，可以有零或多个值，其值来自表创建时规定的允许的一列值。指定包括多个SET成员的SET列值时各成员之开。例如，指定为`SET('one', 'two') NOT NULL`的列可以有下面的任何值：
* ''
* 'one'
* 'two'
* 'one,two'

*SET最多可以设置64个值。创建表时，SET成员值的尾部空格将自动被删除。检索时，保存在SET列的值使用列定义中所使用的大小*
*MySQL用数字保存SET值，所保存值的低阶位对应第1个SET成员。如果在数值上下文中检索一个SET值，检索的值的位设置对应组员。*

| set  | 二进制  | 十进制  |
| ---- | ---- | ---- |
| 'a'  | 0001 | 1    |
| 'b'  | 0010 | 2    |
| 'c'  | 0100 | 4    |
| 'd'  | 1000 | 8    |

**实际应用场景：可以作为权限管理**

#### JSON











## SQL DDL 练习

1. 创建库db1
2. 修改db1的字符编码为utf8
3. 删除库db1
4. 创建库uplooking
5. 创建表student，有id_student （主键）和name列
6. 创建表teachers，有id_teacher （主键）和name列
7. 创建表t1，有id（主键，自增）和values列
8. 重命名表student为students
9. 给student表新增id_teacher列
10. 给teachers表新增age列
11. 给teachers表删除age列
12. 给students表添加外键id_teacher列
13. 删除t1表
14. 创建库db1
15. 删除库db1

```shell
mysql> create database db1;
mysql> alter database db1 character set utf8;
mysql> show create database db1;
+----------+--------------------------------------------------------------+
| Database | Create Database                                              |
+----------+--------------------------------------------------------------+
| db1      | CREATE DATABASE `db1` /*!40100 DEFAULT CHARACTER SET utf8 */ |
+----------+--------------------------------------------------------------+
mysql> drop database db1;
mysql> create database uplooking;
mysql> use uplooking
mysql> create table uplooking.student (id_student int primary key ,name varchar(20) );
mysql> create table uplooking.teachers (id_teacher int primary key ,name varchar(20));
mysql> create table t1 (id int primary key auto_increment,name varchar(10));
mysql> rename table student to students;
mysql> alter table students add id_teacher int;
mysql> alter table teachers add age int;
mysql> alter table teachers drop column age;
mysql> alter table students add constraint fy_students_teachers foreign key (id_teacher) references teachers (id_teacher);
mysql> drop table t1;
mysql> create database db1;
mysql> drop database db1;
```

## SQL DML 练习

1. 插入以下数据到teachers表中

   | id_teacher | name   |
   | ---------- | ------ |
   | 1          | Booboo |
   | 2          | Kevin  |
   | 3          | Mark   |

2. 插入以下数据到students表中：

   | id_student | name        | id_teacher |
   | ---------- | ----------- | ---------- |
   | 1          | superman    | 1          |
   | 2          | batman      | 1          |
   | 3          | wonderwoman | 1          |


​     

3. 修改teachers表中id_teacher列为3的name列的值为John
4. 修改students表中name列为batman并且id_teacher为1的行，将name改为leo
5. 修改students表中id_teacher=1或者id_teacher=2的行，将id_teacher改为3
6. 删除students表中id_student=3的行
7. 删除students表和teachers表中所有的行


