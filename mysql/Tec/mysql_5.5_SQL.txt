# mysql sql


声明列类型{

数据类型总结

数值型
	整型	tinyint,smallint,mediumint,int,bigint
			整型的unsigned-->无符号，zerofill->零填充，M宽度
	浮点型、定点型
			float(M,d) unsigned,M->精度，即总位数，D代表小数位
			decimal比float更精确

字符型
	char(M) 定长，可存储的字符数，M<=255
	varchar(M) 变长，可存储的字符数，M=<65535
	char与varchar的区别
		char(M)，实占M个字符，不够M个，右侧补空格，取出时，去除右侧空格
		varchar(M)，有1-2个字节来标记真实的长度
		
日期时间型
	year 1901-2155，如果输入2位'00-69'+2000,'70-99'+1900
	date YYYY-MM-DD，范围在1000-01-01->9999-12-31
	time HH:MM:SS，范围在-838:59:59->838:59:59
	datetime 'YYYY-MM-DD HH:MM:SS' ，范围在'1000-01-0100:00:00' -> '9999-12-31 23:59:59'.
	
开发中的一个问题——精确到秒的时间表示方式，时间戳 用int型，而不是datetime
}

创库创表{

创建商品表goods

CREATE TABLE `goods` (
  `goods_id` mediumint(8) unsigned NOT NULL AUTO_INCREMENT primary key,
  `cat_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `goods_sn` varchar(60) NOT NULL DEFAULT '',
  `goods_name` varchar(120) NOT NULL DEFAULT '',
  `click_count` int(10) unsigned NOT NULL DEFAULT '0',
  `brand_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  `goods_number` smallint(5) unsigned NOT NULL DEFAULT '0',
  `market_price` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',
  `shop_price` decimal(10,2) unsigned NOT NULL DEFAULT '0.00',
  add_time int unsigned not null default 0) CHARSET=utf8;

创建品牌表brand
 
CREATE TABLE `brand` (
  `brand_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `brand_name` varchar(60) NOT NULL DEFAULT '',
  PRIMARY KEY (`brand_id`)
) CHARSET utf8;

创建商品栏目表category

CREATE TABLE `category` (
  `cat_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(90) NOT NULL DEFAULT '',
  `parent_id` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`cat_id`)
) CHARSET utf8;
}

导入数据{

insert into booboo.goods 
select 
goods_id,cat_id,goods_sn,goods_name,
click_count,brand_id,goods_number,
market_price,shop_price,add_time 
from ecshop.ecs_goods;

insert into booboo.category
select
cat_id,cat_name,parent_id
from ecshop.ecs_category;

insert into booboo.brand
select
brand_id,brand_name
from ecshop.ecs_brand;

查看表信息

MariaDB [booboo]> select * from brand;
+----------+----------------+
| brand_id | brand_name     |
+----------+----------------+
|        1 | 诺基亚         |
|        2 | 摩托罗拉       |
|        3 | 多普达         |
|        4 | 飞利浦         |
|        5 | 夏新           |
|        6 | 三星           |
|        7 | 索爱           |
|        8 | LG             |
|        9 | 联想           |
|       10 | 金立           |
|       11 |   恒基伟业     |
+----------+----------------+
11 rows in set (0.12 sec)

MariaDB [booboo]> select * from category;
+--------+---------------------------+-----------+
| cat_id | cat_name                  | parent_id |
+--------+---------------------------+-----------+
|      1 | 手机类型                  |         0 |
|      2 | CDMA手机                  |         1 |
|      3 | GSM手机                   |         1 |
|      4 | 3G手机                    |         1 |
|      5 | 双模手机                  |         1 |
|      6 | 手机配件                  |         0 |
|      7 | 充电器                    |         6 |
|      8 | 耳机                      |         6 |
|      9 | 电池                      |         6 |
|     11 | 读卡器和内存卡            |         6 |
|     12 | 充值卡                    |         0 |
|     13 | 小灵通/固话充值卡         |        12 |
|     14 | 移动手机充值卡            |        12 |
|     15 | 联通手机充值卡            |        12 |
+--------+---------------------------+-----------+
14 rows in set (0.02 sec)

MariaDB [booboo]> select * from goods limit 5;
+----------+--------+-----------+-----------------------------+-------------+----------+--------------+--------------+------------+------------+
| goods_id | cat_id | goods_sn  | goods_name                  | click_count | brand_id | goods_number | market_price | shop_price | add_time   |
+----------+--------+-----------+-----------------------------+-------------+----------+--------------+--------------+------------+------------+
|        1 |      4 | ECS000000 | KD876                       |           7 |        8 |            1 |      1665.60 |    1388.00 | 1240902890 |
|        3 |      8 | ECS000002 | 诺基亚原装5800耳机          |           3 |        1 |           24 |        81.60 |      68.00 | 1241422082 |
|        4 |      8 | ECS000004 | 诺基亚N85原装充电器         |           0 |        1 |           17 |        69.60 |      58.00 | 1241422402 |
|        5 |     11 | ECS000005 | 索爱原装M2卡读卡器          |           3 |        7 |            8 |        24.00 |      20.00 | 1241422518 |
|        6 |     11 | ECS000006 | 胜创KINGMAX内存卡           |           0 |        0 |           15 |        50.40 |      42.00 | 1241422573 |
+----------+--------+-----------+-----------------------------+-------------+----------+--------------+--------------+------------+------------+

}

查询5种字句{

where,group,having,order by,limit

比较运算符
	<,<=,>,>=,=,!=,<>,in,between
	#in (va1,va2,va3..vaN)，值等于1->N任意一个都行
	#between va1 and va2，表示在va1和va2之间
	
逻辑运算符
	and,or,not
	&&,||,!
	
模糊查询 
	like 
	% 任意字符
	_ 单个字符{
	goods表中的所有商品{
	select * from goods;
	}
	goods表中goods_id小于12的商品{
	select goods_id,goods_name from goods where goods_id>20;
	}
	goods表中市场价比本店价格超过200的商品的id，名字，价格{
		select goods_id,goods_name,market_price,shop_price from goods where market_price-shop_price > 200;
	}
	本店价格小于3000的商品{
		select goods_id,goods_name,shop_price from goods where shop_price < 3000;
	}
	本店价格小于等于2000的商品{
		select goods_id,goods_name,shop_price from goods where shop_price <= 2000;
	}
	本店价格等于2000的商品{
		select goods_id,goods_name,shop_price from goods where shop_price = 2000;
	}
	本店价格大于3010的商品{
		select goods_id,goods_name,shop_price from goods where shop_price > 3010;
	}
	本店价格大于等于3010的商品{
		select goods_id,goods_name,shop_price from goods where shop_price >= 3010;
	}
	本店价格不等于3010的商品{
		select goods_id,goods_name,shop_price from goods where shop_price != 3010;
	}
	不属于第三号栏目的所有商品{
		select goods_id,cat_id,goods_name from goods where cat_id <> 3;
	}
	属于第三号栏目或者第四号栏目的所有商品{
		select goods_id,cat_id,goods_name from goods where cat_id in (3,4);
	}
	本店价格在2000到3000之间的所有商品{
		select goods_id,goods_name,shop_price from goods where shop_price between 2000 and 3000;
	}
	本店价格在3000到5000之间，或者500到1000的商品{
		select goods_id,goods_name,shop_price from goods where shop_price between 3000 and 5000 or shop_price between 500 and 1000;
	}
	不属于第4和第5栏目的商品{
		select goods_id,goods_name,cat_id from goods where cat_id not in (4,5);
	}
	商品名以诺基亚开头的商品{
		select goods_id,goods_name from goods where goods_name like '诺基亚%';
	}
	商品名以诺基亚开头后面只有三个字符的商品{
		select goods_id,goods_name from goods where goods_name like '诺基亚___';
    }
	}

group 常用于分类统计，求平均等场景，与以下聚合函数配合使用：

	max 最大
	min 最小
	sum 总和
	avg 平均
	count 总行数{	
	最贵的商品价格{
		select max(shop_price) from goods;
	}
	最大的商品编号{
		select max(goods_id) from goods;
	}
	最便宜的商品价格{
		select min(shop_price) from goods;
	}
	最小商品编号{
		select min(goods_id) from goods;
	}
	该店所有商品的库存总量{
		select count(goods_number) from goods;
	}
	查询所有商品的平均价{
		selelct agv(shop_price) from goods;
	}
	该店一共有多少个商品{
		select count(*) from goods;
	}
	查询每个栏目下面最贵商品价格；最低商品价格；商品平均价格；商品库存量；商品种类{
		select max(shop_price),min(shop_price),avg(shop_price),count(*) from goods group by cat_id;
	}	
	}

having和group综合运用查询{
	查询该店的商品比市场价格所节省的价格{
		select goods_id,goods_name,market_price-shop_price as j from goods;
	}
	查询每个商品所积压的货款（提示：库存*单价）{
		select goods_id,goods_name,goods_number*shop_price from goods;
	}
	查询该店积压的总货款{
		select sum(goods_number*shop_price) from goods;
	}
	查询该店每个栏目下面积压的货款{
		select cat_id,sum(goods_num*shop_price) as k from goods group by cat_id;
	}
	查询比市场价省钱200元以上的商品及该商品锁省的钱（where和having分别实现）{
		select goods_id,goods_name,shop_price,market_price,market_price-shop_price as p from goods where market_price-shop_price > 200;
		select goods_id,goods_name,shop_price,market_price,market_price-shop_price as p from goods having p>200;
	}
	查询积压贷款超过2w的栏目，以及栏目积压的货款{
		select cat_id,goods_number*shop_price as k from goods group by cat_id having k > 20000 ;
	}
	}

order by 与 limit 查询{	
	
	按价格由高到底排序{
		select goods_id,goods_name,shop_price from goods order by shop_price desc;
	}
	按发布时间由早到晚排序{
		select goods_id,goods_name,add_time from goods order by add_time ;
	}
	按栏目由低到高排序，栏目内部按价格由高到低排序{
		select goods_id,goods_name,cat_id,shop_price from goods order by cat_id,shop_price desc;
	}
	取出价格最高的前三名商品{
		select goods_id,goods_name,shop_price from goods order by shop_price desc limit 3;
	}
	取出点击量前三名到前五名的商品{
		select goods_id,goods_name,click_count from goods order by click_count desc limit 2,3;
	}
	
	# limit a,b 代表从索引位a开始，一共取b个记录，而索引是从0开始	
	# 如果不写a，则相当于 limit 0,b
	
}

使用误区{

	找出每个栏目下最贵的商品，商品名，商品所在栏目，商品id，商品价格：
	
	这个问题没有办法用一个select完成，需要用到view或子查询
	
	create view a as select cat_id,goods_id,goods_name,shop_price from goods order by cat_id,shop_price desc;
	select * from a group by cat_id;
	
	注意5个字句的顺序，where > group by > having > order by > limit
	group by默认输出行只会选择组中的第一行
	}	
}	

子查询3种{
	
	where 型{
		
		# 把内层查询的结果作为外层查询的比较条件
		# 查询最大、最贵商品
		
		查询最新的商品（以id最大为最新，不用order by）:{
			select goods_id,goods_name from goods where goods_id = (select max(goods_id) from goods);
		}
		每个栏目下最新的商品：{
			select cat_id,goods_id,goods_name from goods where goods_id in (select max(goods_id) from goods group by cat_id);	
		}
		每个栏目下最贵的商品：{
			select cat_id,goods_id,goods_name,shop_price from goods where shop_price in (select max(shop_price) from goods group by cat_id);
		}	
		
	}
	
	from 型{
		
		# 把内层查询的结果作为外层查询的临时表
		# 查询每个栏目下最新、最贵商品
		
		每个栏目下最新的商品：{
			select * from (select cat_id,goods_id,goods_name from goods order by cat_id,goods_id desc) as a group by cat_id;
		}
		
	}
	
	exits 型{
		
		# 把外层的查询结果，拿到内层，看内存查询是否成立
		# 查询有商品的栏目
		
		查有商品的栏目{
			select cat_id,cat_name from category where cat_id in (select cat_id from goods where cat_id in (select cat_id from category) group by cat_id);
			select cat_id,cat_name from category where exists (select * from goods where goods.cat_id = category.cat_id);
		}
	}
	
	拓展题{

	设有成绩表stu，如下：
	+--------+--------+-------+
	| name   | class  | score |
	+--------+--------+-------+
	| 张三   | 数学   |    90 |
	| 张三   | 语文   |    50 |
	| 张三   | 地理   |    40 |
	| 李四   | 语文   |    55 |
	| 李四   | 政治   |    45 |
	| 王五   | 政治   |    30 |
	+--------+--------+-------+
	试查询两门及两门以上不及格的学生的平均分{
		select name,avg(score) from stu where name in (select name from stu where score < 60 group by name having count(*)>=2) group by name;
		select name,avg(score) from stu where name in (select name from stu group by name having sum(score<60) >= 2) group by name;
	}

	
	

}	

}

合并查询{
	
	union 联合{
		
		# 作用：把2个查询连接在一起
		# 要求：两次查询的列数一直
		# 推荐：查询的每一个列，相对应的列类型也一样
		# 可以来自多张表，例如ecshop中的留言板
		查询ecshop中用户ecshop的评论和投诉{
			select user_name,content from ecs_comment where user_name = 'ecshop' union select user_name,msg_content from ecs_feedback where user_name = 'ecshop';
		}
		# 如果不同的语句中有完全相同的行，则会合并为一行，即去重
		# 如果不想自动去重复，则需要使用all参数，union all
		获取a表和b表中的id和num，如果id相同，则获取num之和{
			MariaDB [booboo]> select * from a;
			+------+------+
			| id   | num  |
			+------+------+
			| a    |    5 |
			| b    |   10 |
			| c    |   15 |
			| d    |   10 |
			+------+------+

			MariaDB [booboo]> select * from b;
			+------+------+
			| id   | num  |
			+------+------+
			| b    |    5 |
			| c    |   15 |
			| d    |   20 |
			| e    |   99 |
			+------+------+
	
			select id,sum(num) from (select * from a union all select * from b) as tmp group by id;
		}
		# 如果包含order by或limit子句，需要加小括号
		# 尽量不要在子句中单独用，而是整体使用，对最终结果来排序
		取第四栏目的商品，价格降序偏排列，还想去第五栏的商品，价格也降序，最终按价格降序，union连接{
			(select shop_price,goods_id,goods_name,cat_id from goods where cat_id = 4 ) union (select shop_price,goods_id,goods_name,cat_id from goods where cat_id = 5 ) order by shop_price desc;
			}
		取第三个栏目价格前3高的商品和第四个栏目价格前两高的商品，用union实现{
		(select goods_id,cat_id,goods_name,shop_price from goods where cat_id = 3 order by shop_price desc limit 3) union (select goods_id,cat_id,goods_name,shop_price from goods where cat_id = 4 order by shop_price desc limit 2);
		}
	
	
	}
		
		
		
}
	
连接查询{
	
	关系型数据库的数学模型为集合set
	1） set的特性：无序，唯一
	2）一张表就是一个集合，一行记录就是一个元素——理论上不可能出现完全相同的行
	3）表中有一个隐藏列row_id是不同的
	集合的运算
	1）在数学中，两个集合X和Y的笛卡尓乘积（Cartesian product），又称直积，表示为X × Y，
	2）第一个对象是X的成员而第二个对象是Y的所有可能有序对的其中一个成员。
	3）假设集合A={a,b}，集合B={0,1,2}，则两个集合的笛卡尔积为{(a,0), (a,1), (a,2), (b,0), (b,1), (b, 2)}。
	
	table a 7 行，table b 8 行 ，这两表相乘一共 7*8=56行
	
	取出商品的商品名，商品所在栏目名{
		select goods_name,cat_name,goods.cat_id,category.cat_id from goods join category on goods.cat_id = category.cat_id limit 4;
		select goods_name,cat_name,goods.cat_id,category.cat_id from goods,category where goods.cat_id = category.cat_id limit 4;
	}
	
	
	python 代码实现笛卡尔积{
	for i in A:
		for j in B:
			print '{}{}'.format(i,j)
	print 'A*B的元素个数为{}'.format(len(A)*len*(B))
	}
	
	python 代码实现左连接{
		test=0	
		for i,j in A.items():
			for m,n in B.items():
				if i==m:
					print '{} {} {} {}'.format(i,j,m,n)
				else:
					test=test+1
			if test==len(B):
			print '{} {} NULL NULL '.format(i,j)
	}
	
	python 代码实现右连接{
		test=0	
		for a,b in B.items():
			for i,j in A.items():
				if a==i:
					print '{} {} {} {}'.format(i,j,a,b)
				else:
					test=test+1
			if test==len(A):
			print 'NULL NULL {} {}'.format(a,b)
	}
	
	
	左连接{
		# select col1,col2,colN from A left join B ON A.col = B.col
		# 左连接以左表为准，去右表匹配，找不到匹配用NULL补齐
		
	}
	
	右连接{
		# select col1,col2,colN from A right join B ON A.col = B.col
		# 右连接以右表为准，去左表匹配，找不到匹配用NULL补齐
		
	}
	
	内连接{
		# 内连接，查询左右表都有的数据，即：不要左、右中NULL的部分
		# 左右连接的交集
		# 左右连接目前没有并集，可以用union连接	
	}
	
	查goods_id,cat_id,cat_name,brand_id,brand_name,goods_name{
			select goods_id,goods.cat_id,cat_name,goods.brand_id,brand_name from goods left join (category,brand) on (goods.cat_id=category.cat_id and goods.brand_id=brand.brand_id);
		}
	

}			
	
列的增删改{
	
	alter table 表名 add 列声明 [after col_name | first]
	
}

视图view{
	
	1）视图定义：视图是由查询结果形成的一张虚拟表
	2）视图的创建语法：create view 视图名 as select 语句;
	3）为什么要视图：简化查询；权限控制，关闭表的权限，打开视图权限；大数据分表时可以用到；
		比如表的行数超过200万行时，就会变慢，可以把一张表拆分成4张表来存放
			news表
			newsid 1,2,3,4
			news1，news2，news3，news4
			把一张表的数据分散到4张表中，分散的方法很多，
			最常用的是用id取模来计算
				id%4+1=[1,2,3,4]
			比如id=17 ，17%4+1=2，news2	
	4）视图与表的关系
			视图是表的查询结果，如果表数据发生变化，则视图也会有影响
			视图增删改也会影响表，但是增删改有时不可以对视图执行，比如不是一一对应关系
			对于视图的插入动作，视图必须包含所有表中没有默认值的列	
	
	视图的创建{
	CREATE
    [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]
	/*	undifiend  	未定义，自动，让系统帮你选
		temptable  	当引用视图时，根据视图的创建语句建立一个临时表
		merge	 	当引用视图时，引用视图的语句与定义视图的语句合并 */
    [SQL SECURITY { DEFINER | INVOKER }]
    VIEW view_name [(column_list)]
    AS select_statement
    [WITH [CASCADED | LOCAL] CHECK OPTION]
	}

	视图的修改{
	ALTER [ALGORITHM = {UNDEFINED | MERGE | TEMPTABLE}]
    VIEW view_name [(column_list)]
    AS select_statement
    [WITH [CASCADED | LOCAL] CHECK OPTION]
	该语句用于更改已有视图的定义。其语法与CREATE VIEW类似。
	}
	
	查询每个栏目下最贵的商品{
	
	create algorithm=temptable view test1 as select goods_id,goods_name,shop_price,cat_id from goods order by cat_id,shop_price desc;
	create algorithm=merge view test as select goods_id,goods_name,shop_price,cat_id from goods order by cat_id,shop_price desc;
	
	MariaDB [booboo]> select * from test group by cat_id;
	+----------+--------------------------------+------------+--------+
	| goods_id | goods_name                     | shop_price | cat_id |
	+----------+--------------------------------+------------+--------+
	|       16 | 恒基伟业G101                   |     823.33 |      2 |
	|        8 | 飞利浦9@9v                     |     399.00 |      3 |
	|        1 | KD876                          |    1388.00 |      4 |
	|       23 | 诺基亚N96                      |    3700.00 |      5 |
	|        3 | 诺基亚原装5800耳机             |      68.00 |      8 |
	|        5 | 索爱原装M2卡读卡器             |      20.00 |     11 |
	|       25 | 小灵通/固话50元充值卡          |      48.00 |     13 |
	|       29 | 移动100元充值卡                |      90.00 |     14 |
	|       27 | 联通100元充值卡                |      95.00 |     15 |
	+----------+--------------------------------+------------+--------+
	9 rows in set (0.00 sec)
	
	MariaDB [booboo]> select * from test1 group by cat_id;
	+----------+----------------------------------------+------------+--------+
	| goods_id | goods_name                             | shop_price | cat_id |
	+----------+----------------------------------------+------------+--------+
	|       16 | 恒基伟业G101                           |     823.33 |      2 |
	|       22 | 多普达Touch HD                         |    5999.00 |      3 |
	|       18 | 夏新T5                                 |    2878.00 |      4 |
	|       23 | 诺基亚N96                              |    3700.00 |      5 |
	|        7 | 诺基亚N85原装立体声耳机HS-82           |     100.00 |      8 |
	|        6 | 胜创KINGMAX内存卡                      |      42.00 |     11 |
	|       25 | 小灵通/固话50元充值卡                  |      48.00 |     13 |
	|       29 | 移动100元充值卡                        |      90.00 |     14 |
	|       27 | 联通100元充值卡                        |      95.00 |     15 |
	+----------+----------------------------------------+------------+--------+
	9 rows in set (0.00 sec)
	}
	
	
}

字符集{
	
	mysql的字符集设置非常灵活，可以设置
		1）服务器默认字符集
		2）数据库默认字符集
		3）表默认字符集 create table 表名（列声明）charset utf8;
		4）列默认字符集
		如果某一个级别没有指定字符集，则继承上一级
		
	以表声明utf8为例：
		存储的数据在表中，最终是utf8
			
	字符集转换器工作原理：
		1）告诉服务器，我给你发的数据是什么编码的？ character_set_client
		2）告诉转换器，需要转换成什么编码？			character_set_connection
		3）告诉服务器，查询的结果用什么编码？		character_set_results
		
		如果三者都为utf8 ，则可以简写为 			set names utf8
		
	插入“中国”，并查询{
		/*查看当前字符集设置*/
		MariaDB [(none)]> show variables like 'character%';
		+--------------------------+----------------------------+
		| Variable_name            | Value                      |
		+--------------------------+----------------------------+
		| character_set_client     | utf8                       |/*客户端使用utf8*/
		| character_set_connection | utf8                       |/*转换器将客户端编码转为utf8*/
		| character_set_database   | latin1                     |/*数据库默认使用latin1*/
		| character_set_filesystem | binary                     |/*文件系统默认使用二进制*/
		| character_set_results    | utf8                       |/*服务器返回客户端的结果使用utf8*/
		| character_set_server     | latin1                     |
		| character_set_system     | utf8                       |
		| character_sets_dir       | /usr/share/mysql/charsets/ |
		+--------------------------+----------------------------+
		8 rows in set (0.08 sec)
		/**/
		/*服务器上创建表t10，使用utf8编码*/
		MariaDB [(none)]> create table test.t10 (name varchar(10)) charset utf8;
		Query OK, 0 rows affected (0.06 sec)
		/*客户端插入“中国utf8”--->转换器将“中国utf8”转为“中国utf8”--->服务器上使用utf8编码保存*/
		MariaDB [(none)]> insert into test.t10 values ('中国');
		Query OK, 1 row affected (0.03 sec)
		/*服务器返回查询结果使用utf8*/
		MariaDB [(none)]> select * from test.t10;
		+--------+
		| name   |
		+--------+
		| 中国   |
		+--------+
		1 row in set (0.00 sec)
		/*设置服务器返回查询结果使用gbk*/
		MariaDB [(none)]> set character_set_results=gbk;
		Query OK, 0 rows affected (0.00 sec)
		/*服务器返回查询结果使用gbk*/
		MariaDB [(none)]> select * from test.t10;
		+------+
		| name |
		+------+
		| א¹򞞠|
		+------+
		1 row in set (0.01 sec)
	}	
		
}

校对集{
	校对集就是排序规则
		1）一种字符集可以有一个或多个排序规则
		2）以UTF8为例，我们默认使用utf8_general_ci规则[a,B,c,D]，也可以按照二进制来排,utf8_bin[B,D,a,c]
	
	如何声明校对集呢？
		create table () charset utf8 collation utf8_bin;
		

	排序例题{
	MariaDB [test]> create table test.t2 (id varchar(10)) charset utf8 collate utf8_bin;
	Query OK, 0 rows affected (0.04 sec)

	MariaDB [test]> insert into test.t2 values ('a'),('B'),('c'),('D');
	Query OK, 4 rows affected (0.03 sec)
	Records: 4  Duplicates: 0  Warnings: 0

	MariaDB [test]> select * from test.t2 order by id;
	+------+
	| id   |
	+------+
	| B    |
	| D    |
	| a    |
	| c    |
	+------+
	4 rows in set (0.04 sec)
	}
}

触发器{
	trigger,触发，一触即发
		1）作用：监视某种情况并触发某种操作
		2）监视对象：表
		3）监视事件：增删改
		4）触发时间：after、before
		5）触发事件：增删改
	
	创建触发器的语法{
		create trigger TGNAME
		after/before insert/update/delete on TBNAME
		For each row //mysql只能使用行触发器
		begin
		sql 语句
		end
	}
	
	删除触发器的语法{
		drop trigger tgname;
	}
	
	old&new{
		1）new 是修改前的数据
		2）old 是修改前的数据
	}
	
	after&before{
				
		after	监视事件发生后触发
		before	监控事件发生前出发
		
	}
	
	观察以下场景：电子商城{
	商品表g
	商品主键	商品名 库存
	1			电脑	28
	2			自行车	12
	
	订单表o
	订单主键	商品外键	购买量
		1		2			3
		2		1			5
		
	完成订单与减少库存的逻辑
		insert into o(gid,num) values (2,3);//插入语句
		update g set goods_num = goods_num - 3 where id=2;//更新过程
	}
	
	触发器例题{
	MariaDB [test]> create table g (gid tinyint primary key auto_increment,goods_name varchar(10) not null,goods_num int not null default 0) charset utf8;
	Query OK, 0 rows affected (0.11 sec)

	MariaDB [test]> create table o (oid tinyint primary key auto_increment,gid tinyint,order_num int not null default 0) charset utf8;
	Query OK, 0 rows affected (0.03 sec)

	MariaDB [test]> insert into g (goods_name,goods_num) values ('小猪',80),('小羊',60),('小鸡',280);
	Query OK, 3 rows affected (0.03 sec)
	Records: 3  Duplicates: 0  Warnings: 0

	MariaDB [test]> insert into o (gid,order_num) values (2,10),(1,20);
	Query OK, 2 rows affected (0.04 sec)
	Records: 2  Duplicates: 0  Warnings: 0

	MariaDB [test]> select * from g;
	+-----+------------+-----------+
	| gid | goods_name | goods_num |
	+-----+------------+-----------+
	|   1 | 小猪       |        80 |
	|   2 | 小羊       |        60 |
	|   3 | 小鸡       |       280 |
	+-----+------------+-----------+
	3 rows in set (0.13 sec)

	MariaDB [test]> select * from o;
	+-----+------+-----------+
	| oid | gid  | order_num |
	+-----+------+-----------+
	|   1 |    2 |        10 |
	|   2 |    1 |        20 |
	+-----+------+-----------+
	2 rows in set (0.00 sec)
	
	//监控对象：表o
	//监控操作：insert
	//触发时间：after
	//触发事件：update
	
	# 添加订单库存减少
	dilimiter //
	create trigger tg1
	after insert on o
	begin
	update g set goods_num = goods_num - new.order_num where gid=new.gid;
	end//
	
	# 删除订单库存增加
	delimiter //
	create trigger tg2
	after delete on o
	for each row
	begin
	update g set goods_num = goods_num + old.order_num where gid=old.gid;
	end//
	
	# 修改订单的数量改变库存
	delimiter//
	create trigger tg3
	after update on o
	for each row
	begin
	update g set goods_num = goods_num + old.order_num - new.order_num where gid=new.gid;
	end//
	
	# 订单数量不能查过库存量，如果超过则改为最大库存
	delimiter//
	create trigger tg4
	before insert on o
	for each row
	begin
	if new.order_num > (select goods_num from g where gid=new.oid)
	then
		set new.order_num = (select goods_num from g where gid=new.oid);
	end if;
	update g set goods_num = goods_num - new.order_num where gid=new.oid;
	end//
	
	}

}

存储过程{
	
	
}

索引与优化{
	
	索引预览{
	设有N条记录，不用索引，平均查找N/2次		1万条记录 查5000次
	btree 二叉树索引	log2N					1万条记录	查14次
	hash  哈希索引		1			
	}
	
	索引的优点和缺点：{
		优点：加快查询速度
		缺点：降低了增删改的速度，增大了表的文件大小，索引文件甚至比数据文件还大
	
	导入数据可以先去掉索引，数据导入后再添加索引	
	}
	
	索引的使用原则{
		1）不过度使用索引
		2）索引条件列where后面最频繁的条件比较适宜索引
		3）索引散列值，过于集中的值不要索引，例如给性别加索引，意义不大
	}

	索引类型{
								唯一性	NULL		个数	
		1）普通索引 index：		可重复	null		多个		加快查询速度
		2）唯一索引 unique：	唯一	not null	多个		不仅能加快查询速度，行上的值不能重复
		3）主键索引 primary：	唯一	not null	一个		关于数据的数据，即元数据，不能重复，不能为空
		4）全文索引 fulltext：	fulltext index

	}
	
	查看索引{
		show index from tablename;
	}	
	
	建立索引{
	alter table add {index|key} [index_name] [index_type] (index_col_name,...) [index_option] ...
		1)index_name:
		2)index_type:btree\hash
		3)index_option:key_block_size = ; index_tyep with parser parser_name comment 'string'
	# 创建主键索引
		alter table add primary key (id);
	# 创建普通索引
		alter table add index index_num (num);
	# 创建唯一索引
		alter table add unique index index_num (num);
	# 创建全文索引
		alter table add fulltext index index_name (name);
	# 创建空间索引
		alter table add spatial index index_num (num);
		mysql的空间索引是建立在空间数据类型（如point和genomtry等)列上的索引。
		在mysql中MyISAM, InnoDB都支持空间列（存储空间数据类型的列）

		空间索引有以下特性：

			只有myisam和innodb（mysql5.7.5以上版本）的表支持空间索引。
			被索引的列必须非NULL
			在mysql5.7中，列的前缀长度属性被禁用。空间索引直接索引完整宽度的列
			由于空间数据类型我们很少用到，所以空间索引我们接触的更少。这里不做深入阐述了
	# 创建外键索引
		alter table add foreign key index_foregin_key (t1.num,t2.num) reference_definition'
		
		
	# 全文索引的用法
		select * from tbname where match (全文索引名) against ('keyword');
		强烈注意：MySql自带的全文索引只能用于数据库引擎为MYISAM的数据表，如果是其他数据引擎，则全文索引不会生效。此外，MySql自带的全文索引只能对英文进行全文检索，目前无法对中文进行全文检索。如果需要对包含中文在内的文本数据进行全文检索，我们需要采用Sphinx（斯芬克斯）/Coreseek技术来处理中文。
	}
 

	注：目前，使用MySql自带的全文索引时，如果查询字符串的长度过短将无法得到期望的搜索结果。MySql全文索引所能找到的词默认最小长度为4个字符。另外，如果查询的字符串包含停止词，那么该停止词将会被忽略。	
}

存储过程{
	类似于函数，就是将一段代码封装起来，通过call来调用
	可以用流程控制语句 if/else ,case , while 
	
	查询存储过程{
		show create procedure dbname.pdname;
	}
	
	创建存储过程{
	delimiter //
	create procedure proc1 (out s int) 
	begin
	select count(*) into s from user;
	end//
	dilimiter ;
	}
	
	参数{
		MySQL存储过程的参数用在存储过程的定义，共有三种参数类型,IN,OUT,INOUT,形式如：
			CREATE PROCEDURE([[IN |OUT |INOUT ] 参数名 数据类形...])
		1)IN 输入参数:表示该参数的值必须在调用存储过程时指定，在存储过程中修改该参数的值不能被返回，为默认值
		2)OUT 输出参数:该值可在存储过程内部被改变，并可返回
		3)INOUT 输入输出参数:调用时指定，并且可被改变和返回
	
	
		IN参数实例{
				delimiter //
				create procedure demo_in (IN p_in int)
				begin
				select p_in;
				set p_in=2;
				select p_in;
				end//
				delimiter ;
				
				set @p_in=1;
				call demo_in(@p_in);
				select @p_in;
		}
		
		OUT参数实例{
				delimiter //
				create procedure demo_out (out p_out int)
				begin
				select p_out;
				set p_out=2;
				select p_out;
				end//
				delimiter ;
				
				set @p_out=1;
				call demo_out(@p_out);
				select @p_out;
		}
	
		INOUT参数实例{
				delimiter //
				create procedure demo_inout (inout p_inout int)
				begin
				select p_inout;
				set p_inout=2;
				select p_inout;
				end//
				delimiter ;
				
				set @p_inout=1;
				call demo_inout(@p_inout);
				select @p_inout;		
			
		}
	}
	
	变量{
	
		Ⅰ. 变量定义
			DECLARE variable_name [,variable_name...] datatype [DEFAULT value];
			其中，datatype为MySQL的数据类型，如:int, float, date, varchar(length)
			例如:
			1. DECLARE l_int int unsigned default 4000000;
			2. DECLARE l_numeric number(8,2) DEFAULT 9.95;
			3. DECLARE l_date date DEFAULT '1999-12-31';
			4. DECLARE l_datetime datetime DEFAULT '1999-12-31 23:59:59';
			5. DECLARE l_varchar varchar(255) DEFAULT 'This will not be padded';
		
		Ⅱ. 变量赋值
			SET 变量名 = 表达式值 [,variable_name = expression ...]
		
		Ⅲ. 用户变量
			ⅰ. 在MySQL客户端使用用户变量
				select 'hello' into @x;
				set @x='hello';
			ⅱ. 在存储过程中使用用户变量
				delimiter //
				create procedure pr1 ()
				begin
				select @x;
				set @x=2;
				select @x;
				end//
				dilimiter ;
				
		①用户变量名一般以@开头
		②滥用用户变量会导致程序难以理解及管理		
				
	}
	
	注释{
		MySQL存储过程可使用两种风格的注释
			1）双模杠：该风格一般用于单行注释 	--name
			2）c风格：一般用于多行注释			/* yes */
	}
	
	流程控制{
		
		if条件判断{
			if a > 1 
			then cmd1;
			else cmd2;
			enf if;
		}
		
		while循环{
			while a > 1
			do cmd1;cmd2;
			end while;
		}
		
		until循环{
			// 它在执行操作后检查结果，而while则是执行前进行检查。
			repeat cmd1; cmd2;
			until a > 1
			end repeat;
		}
		
		loop循环{
			/* loop循环不需要初始条件，这点和while 循环相似，同时和repeat循环一样不需要结束条件,
			leave语句的意义是离开循环。*/
			loop_table：loop cmd1;cmd2;
			if a > 1 
			then leave loop_table;
			end if;
			end loop;
		}
		
	基本函数{

			字符串类型{
				CHARSET(str) //返回字串字符集
				CONCAT (string2 [,... ]) //连接字串
				INSTR (string ,substring ) //返回substring首次在string中出现的位置,不存在返回0
				LCASE (string2 ) //转换成小写
				LEFT (string2 ,length ) //从string2中的左边起取length个字符
				LENGTH (string ) //string长度
				LOAD_FILE (file_name ) //从文件读取内容
				LOCATE (substring , string [,start_position ] ) 同INSTR,但可指定开始位置
				LPAD (string2 ,length ,pad ) //重复用pad加在string开头,直到字串长度为length
				LTRIM (string2 ) //去除前端空格
				REPEAT (string2 ,count ) //重复count次
				REPLACE (str ,search_str ,replace_str ) //在str中用replace_str替换search_str
				RPAD (string2 ,length ,pad) //在str后用pad补充,直到长度为length
				RTRIM (string2 ) //去除后端空格
				STRCMP (string1 ,string2 ) //逐字符比较两字串大小,
				SUBSTRING (str , position [,length ]) //从str的position开始,取length个字符,
				// 注：mysql中处理字符串时，默认第一个字符下标为1，即参数position必须大于等于1
				TRIM([[BOTH|LEADING|TRAILING] [padding] FROM]string2) //去除指定位置的指定字符
				UCASE (string2 ) //转换成大写
				RIGHT(string2,length) //取string2最后length个字符
				SPACE(count) //生成count个空格
			}
			
			数字类型{
				ABS (number2 ) //绝对值
				BIN (decimal_number ) //十进制转二进制
				CEILING (number2 ) //向上取整
				CONV(number2,from_base,to_base) //进制转换
				FLOOR (number2 ) //向下取整
				FORMAT (number,decimal_places ) //保留小数位数
				HEX (DecimalNumber ) //转十六进制
				// 注：HEX()中可传入字符串，则返回其ASC11码，如HEX('DEF')返回4142143 也可以传入十进制整数，返回其十六进制编码，如HEX(25)返回19	
				LEAST (number , number2 [,..]) //求最小值
				MOD (numerator ,denominator ) //求余
				POWER (number ,power ) //求指数
				RAND([seed]) //随机数
				ROUND (number [,decimals ]) //四舍五入,decimals为小数位数]
			}
			
			日期时间类{
				ADDTIME (date2 ,time_interval ) //将time_interval加到date2
				CONVERT_TZ (datetime2 ,fromTZ ,toTZ ) //转换时区
				CURRENT_DATE ( ) //当前日期
				CURRENT_TIME ( ) //当前时间
				CURRENT_TIMESTAMP ( ) //当前时间戳
				DATE (datetime ) //返回datetime的日期部分
				DATE_ADD (date2 , INTERVAL d_value d_type ) //在date2中加上日期或时间
				DATE_FORMAT (datetime ,FormatCodes ) //使用formatcodes格式显示datetime
				DATE_SUB (date2 , INTERVAL d_value d_type ) //在date2上减去一个时间
				DATEDIFF (date1 ,date2 ) //两个日期差
				DAY (date ) //返回日期的天
				DAYNAME (date ) //英文星期
				DAYOFWEEK (date ) //星期(17),1为星期天
				DAYOFYEAR (date ) //一年中的第几天
				EXTRACT (interval_name FROM date ) //从date中提取日期的指定部分
				MAKEDATE (year ,day ) //给出年及年中的第几天,生成日期串
				MAKETIME (hour ,minute ,second ) //生成时间串
				MONTHNAME (date ) //英文月份名
				NOW ( ) //当前时间
				SEC_TO_TIME (seconds ) //秒数转成时间
				STR_TO_DATE (string ,format ) //字串转成时间,以format格式显示
				TIMEDIFF (datetime1 ,datetime2 ) //两个时间差
				TIME_TO_SEC (time ) //时间转秒数]
				WEEK (date_time [,start_of_week ]) //第几周
				YEAR (datetime ) //年份
				DAYOFMONTH(datetime) //月的第几天
				HOUR(datetime) //小时
				LAST_DAY(date) //date的月的最后日期
				MICROSECOND(datetime) //微秒
			}
	
}

SQL执行计划explain{
	
	EXPLAIN 语句主要是用于解析SQL执行计划，通过分析执行计划采取适当的优化方式提高SQL运行的效率。
	EXPLAIN 语句输出通常包括id列，select_type，table，type，possible_keys，key等等列信息
	MySQL 5.6.3后支持SELECT, DELETE, INSERT,REPLACE, and UPDATE.
	EXPLAIN EXTENDED支持一些额外的执行计划相关的信息
	EXPLAIN PARTITIONS支持基于分区表查询执行计划的相关信息
	
	执行顺序id：{
		1)包含一组数字，表示查询中执行select子句或操作表的顺序
		2)id如果相同，可以认为是一组，从上往下顺序执行；在所有组中，id值越大，优先级越高，越先执行
	}
	
	table：{
		1)从哪个表(表名)上输出行记录，
	}
	
	连接类型type：{
		1)system 表只有一行
		2)const 表最多只有一行匹配，通用用于主键或者唯一索引比较时
		3)eq_ref 每次与之前的表合并行都只在该表读取一行，这是除了system，const之外最好的一种，特点是使用=，而且索引的所有部分都参与join且索引是主键或非空唯一键的索引
		4)ref 如果每次只匹配少数行，那就是比较好的一种，使用=或<=>，可以是左覆盖索引或非主键或非唯一键
		5)fulltext 全文搜索
		6)ref_or_null 与ref类似，但包括NULL
		7)index_merge 表示出现了索引合并优化(包括交集，并集以及交集之间的并集)，但不包括跨表和全文索引。这个比较复杂，目前的理解是合并单表的范围索引扫描（如果成本估算比普通的range要更优的话）
		8)unique_subquery 在in子查询中，就是value in (select...)把形如“select unique_key_column”的子查询替换。PS：所以不一定in子句中使用子查询就是低效的！
		9)index_subquery 同上，但把形如”select non_unique_key_column“的子查询替换
		10)range 常数值的范围
		11)index 
				a.当查询是索引覆盖的，即所有数据均可从索引树获取的时候（Extra中有Using Index）；
				b.以索引顺序从索引中查找数据行的全表扫描（无 Using Index）；
				c.如果Extra中Using Index与Using Where同时出现的话，则是利用索引查找键值的意思；
				d.如单独出现，则是用读索引来代替读行，但不用于查找
		12)all 全表扫描
	}
	
	可能使用的索引possible_keys：{
		1)指出MySQL能使用哪个索引在表中找到行。
		2)查询涉及到的字段上若存在索引则该索引将被列出，但不一定被查询使用。
		3)如果改列为NULL，说明该查询不会使用到当前表上的相关索引，考虑是否有必要添加索引
	}
	
	实际使用的索引key：{
		1)显示MySQL在查询中实际使用的索引，若没有使用索引，显示为NULL
		2)也可能存在key不等于possible_keys的情形，即possible_keys不适合提取所需的行
		3)而查询所选择的列在使用其他索引时更高效
		TIPS：查询中若使用了覆盖索引，则该索引仅出现在key列表中
	}

	索引字节数key_len：{
		1)表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度
	}
	
	ref：{
		1)表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
	}
	
	rows：{
		1)表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数
		2)对于InnoDB，该值为预估，不一定精确
	}
	
	Extra:{
		1)包含不适合在其他列中显示但十分重要的额外信息
	}
}




