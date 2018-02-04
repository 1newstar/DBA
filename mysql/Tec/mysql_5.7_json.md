# MySQL JSON �������͵�ʹ��

[TOC]

## ʲô��json

JSON(JavaScript Object Notation) ��һ�������������ݽ�����ʽ��������ECMAScript��һ���Ӽ��� 

JSON������ȫ���������Ե��ı���ʽ������Ҳʹ����������C���Լ����ϰ�ߣ�����C��C++��C#��Java��JavaScript��Perl��Python�ȣ���

��Щ����ʹJSON��Ϊ��������ݽ������ԡ� �������Ķ��ͱ�д��ͬʱҲ���ڻ�������������(һ�������������紫������)��

### JSON �﷨����

JSON �﷨�� JavaScript �����ʾ�﷨���Ӽ���

* �����ڼ�ֵ����
* �����ɶ��ŷָ�
* �����ű������
* �����ű�������

### JSON ����/ֵ��

JSON ���ݵ���д��ʽ�ǣ�����/ֵ�ԡ�

����/ֵ������е�����д��ǰ�棨��˫�����У���ֵ��д�ں���(ͬ����˫������)���м���ð�Ÿ�����

`"firstName":"John"`

���������⣬�ȼ������� JavaScript ��䣺

`firstName="John"`

### JSON ֵ

JSON ֵ�����ǣ�

* ���֣������򸡵�����
* �ַ�������˫�����У�
* �߼�ֵ��true �� false��
* ���飨�ڷ������У�:������ֵ��value�������򼯺�
* �����ڻ������У�:������һ������ġ�������/ֵ���ԡ�����
* null

### ʵ��

```shell
{
    "name": "BeJson",
    "url": "http://www.bejson.com",
    "page": 88,
    "isNonProfit": true,
    "address": {
        "street": "�Ƽ�԰·.",
        "city": "��������",
        "country": "�й�"
    },
    "links": [
        {
            "name": "Google",
            "url": "http://www.google.com"
        },
        {
            "name": "Baidu",
            "url": "http://www.baidu.com"
        },
        {
            "name": "SoSo",
            "url": "http://www.SoSo.com"
        }
    ]
}
```

### �ŵ�

1. �����ڴ��䣬����������ַ�����Ȼֱ�Ӵ�����������õģ��������ѽ��������⡣�������xml�����ַ����ķ�ʽ����json��������ĺô���google�и��Լ���Э�飬��protobuf������Ȥ���˽�һ�¡�
2. ����ת�����кܶ��json api�ṩ��json�ַ���ת�ɶ��󡢶���ת����json���ķ�����
3. �����Ķ���json��������ýṹ�����Ժ�ֱ�۵��˽�����ʲô���ݡ�


## MySQL 5.7.8 ��ʼ���json

As of MySQL 5.7.8, MySQL supports a native JSON data type that enables efficient access to data inJSON (JavaScript Object Notation) documents. The JSON data type provides these advantages overstoring JSON-format strings in a string column:

�� MySQL 5.7.8 ��ʼ��MySQL֧��ԭ��̬��JSON�������͡���ʹ��MySQL���ݿ���Ը�Ч�ط���JSON �ĵ����͵����ݡ�JSON���������ṩ�������ƣ����е�����Ϊ�ַ������͵�ʱ��ʹ��JSON���͵��ַ������Ƹ���

* Automatic validation of JSON documents stored in JSON columns. Invalid documents produce an error.
* Optimized storage format. JSON documents stored in JSON columns are converted to an internal format that permits quick read access to document elements. When the server later must read a JSON values stored in this binary format, the value need not be parsed from a text representation. The binary format Creating JSON Values is structured to enable the server to look up subobjects or nested values directly by key or array index without reading all values before or after them in the document.

* JSON���д洢��JSON�ĵ��ܹ��Զ���֤����Ч���ļ������һ������
* �Ż��洢���͡�JSON���д洢��JSON�ĵ���ת��Ϊһ���ڲ���ʽ,�ڲ���ʽ������ٵĶ��ͷ����ĵ�Ԫ�ء���������֮������ȡ�洢Ϊ�����Ƹ�ʽ��JSON���ݵ�ֵʱ,�Ͳ���Ҫ���ı���ʾ��ʽ�������ˡ�����JSON����ֵ�Ķ����Ƹ�ʽʹ�����������Ӷ���ֱ��ͨ�����õ���Ƕ��ֵ����������ʱ������Ҫ��ȡ�ĵ�������ֵ��������Щֵ���Ѿ����ĵ��л���֮��ӽ����ġ� 

MySQL 5.7.8��ʼ֧��json�ֶ�����,���ṩ�˲������ú���,ͨ��������,����������ֱ������json�е�����!

Ϊ��˵jsonԭ��֧�ַǳ��ؼ���,���ǿ����Լ��ڿͻ��˴���jsonȻ�󱣴��ַ�����mysql��������?

����һ����ԭ��֧�ֵ�����ʲô����

```shell
create table t (
 id int not null,
 js json not null,
 PRIMARY KEY (id)
)
```

> 1.����ֱ�ӹ��˼�¼

select * from t where js->'$.a'=100

������Ҫ�����м�¼����ȡ�������ڿͻ��˽��й��ˡ�


> 2.����ֱ��update���������ȶ�ȡ

update t set js=json_set(js,'$.a',js->'$.a'+1) where id=1

����ԭ�Ӹ���


update t,t1 set t.js=json_merage(t.js,t1.js) where t.id=t1.id

������


> 3.������һ��SQL����ɶ�����¼���޸ģ�

update t set js=json_set(js,'$.a',123) where id in(1,2)

û��ԭ����֧�֣�����Ǻ���ʵ�ֵġ�


> 4.ͨ��json���ͣ�������ʵ���˱�ṹ�Ķ�̬�仯
> ����һ�������ϵ����ӱ��ֶΣ�������Ƕ����������������

update t set js=json_array_append(js,'$.sonAry',123) where id =1

����һ���ӽڵ㵽sonAry�У������ӱ�


> 5.ͨ��������������json�Ͻ�������

CREATE TABLE j1 (
  id int(11) NOT NULL,
  js json NOT NULL,
  s varchar(45) CHARACTER SET utf8mb4 NOT NULL,
  a int(11) GENERATED ALWAYS AS (json_extract(js,'$.a')) STORED,
  PRIMARY KEY (id),
  KEY i_a (a)
)

ͨ��a���������`(json_extract(js,'$.a'))`�Ͻ�������,��������mysql�����������ٶ�λ��

`json_extract`��������`path`��ͨ����������������������

������������`JSON_CONTAINS/JSON_CONTAINS_PATH`���������������������ϳ��ܶࡣ


### ��MongoDB�Ĳ���

1. **mongodb���Զ�������**��Ҳ���ǿ��Զ�̬���ӱ�,���mysql���Ǳ����ȶ����
2. **�󲿷ֲ�ѯ������²���**,��Ϊmysql json֧��,����û��ʲô���ܲ���ˡ����ǾͲ�ѯ��˵,mysql��SQL�﷨,�ر���json_extract�ļ�дģʽ,�ɶ��Ա�mongodb��Ҫǿ����
3. **mongodbʵ�������������Խ���ϵͳ���Ӷ���ʵ�ָ�����**���ⷽ��,Ҫ���û�ʹ�ó���,����˵���ƻ�������
4. **���ڴ����ݵ�֧��**��mongodb�ڴ�����֧�������ıȽϺ�,�ر������ݷ�Ƭ,�߿����ϻ�������ʵ���ˣ�mysql�ⷽ��Ҳ�ڲ������ƣ��������Ҫ������һ�����ϵ�ѡȡ,��һ���Ե������׷ֲ�����,��ǿһ�������Ӻܶ�.

���ǿ��Լ���,��ϵ���ݿ����֮���������ǿһ����,��ô�ⷽ��,mongodb��nosqlʵ��Ҳ�������κ�����.

��δ����������,

ǿһ���Է���,��ͳ��ϵ���ݿ�ʼ����Ψһ���ѡ��,����ͨ��֧��json,����ǰNosql��һЩ����Ҳ�������뵽�Լ���ϵ��.

���ڹ̶����ֶ�,��Ȼ��ͳ�ı���ʽ���ܸ���,�����ڶ�̬�ֶη��ö�����json�ֶ���,Ҳ���Ժܺõ���Ӧ��������.

��һ���Է���,NoSQL���ó�һЩ,��ͳ��ϵ���ݿ��������Ӧ�ò���ͨ����ʵ�����ݿ�ķֲ���ʽ��ʵ��(������һ�����������������).

���ڴ�ֲ�ʽ��������һ���Է���,��ͳ��ϵ���ݿ�ȱ��ֱ��֧��,�����ǿ���ͨ��Ӧ�ò���ʵ��,���ܶ�NoSQLҲ�ڲ��������ⷽ��Ĺ���.

�����ڴ�һ��������ϵ���ݿ�,ÿ��ʵ���ṩǿһ���Ե�����,���õ�SQL,���Զ�̬���������ܺõ�֧��.

����ʵ��֮����һ���ֲ�ʽ�Ĳ�,���Ծۺϴ������ݿ�ʵ��,��Э���û�ʵ������һ����,

�����ͱȽ�������.


## ���ʹ��json��������

### ����json���͵���

```shell
create table t(id int,js json,PRIMARY KEY (`id`))
```

### ��������

```shell
insert into t values(1,'{"a":1,"s":"abc"}')
insert into t values(2,'[1,2,{"a":123}]')
insert into t values(3,'"str"')
insert into t values(4,'123')

# ֱ���ṩ�ַ������ɡ���������JSON_Array��JSON_Object����������
insert into t values(5,JSON_Object('key1',v1,'key2',v2))
insert into t values(4,JSON_Array(v1,v2,v3))
```

* `JSON_OBJECT([key, val[, key, val] ...])`
* `JSON_ARRAY([val[, val] ...])`
* `JSON_SET(json_doc, path, val[, path, val] ...)`

### �޸�����

```shell
update t set js=json_set('{"a":1,"s":"abc"}','$.a',456,'$.b','bbb') where id=1
```

���`js={"a":456,"s":"abc","b":"bbb"}`

path��`$`�ʹ�������`doc`,Ȼ�������`JavaScript`�ķ�ʽָ���������Ի��������±��.ִ��Ч��������json���﷨

```shell
$.a=456
$.b="bbb"
```

���ھ��޸�,�����ھ�����.

```shell
$.c.c=123
```

�����`javascript`�л������Ϊ`.c`Ϊ`null`��
������`json_set('{}','$.c.c',123)`�У������ڵ�·����ֱ�ӱ����ԡ�

����Ķ������飬���Ŀ��`doc`����������ᱻת����`[doc]`��Ȼ����ִ��`set`��
���`set`���±곬�����鳤�ȣ�ֻ����ӵ������β��

```shell
select json_set('{"a":456}','$[1]',123)

# ���[{"a":456},123]��Ŀ���ֱ�ת����[{"a":456}],Ȼ��Ӧ��$[1]=123��

select json_set('"abc"','$[999]',123)

# ���["abc",123]��
```

�پټ�������

```shell
select json_set('[1,2,3]','$[0]',456,'$[3]','bbb')
# ���[456,2,3,'bbb']
```

ע��:
����`javascript`��
`var a=[1,2,3]`
`a.a='abc'`
�ǺϷ���,����һ��`a`ת��`json`�ַ���,`a.a`�Ͷ�ʧ�ˡ�

����`mysql`�У���������·�������ڣ����
`select json_set('[1,2,3]','$.a',456)`
�������`[1,2,3]`


Ȼ�������������汾
`JSON_INSERT(json_doc, path, val[, path, val] ...)`
��������ڶ�Ӧ���������,�������κα䶯

`JSON_REPLACE(json_doc, path, val[, path, val] ...)`
����������滻,�������κα䶯

��������������û��javascriptֱ�Ӷ�Ӧ�Ĳ���
`select json_insert('{"a":1,"s":"abc"}','$.a',456,'$.b','bbb')`
���`{"a":1,"s":"abc","b":"bbb"}`

`select json_replace('{"a":1,"s":"abc"}','$.a',456,'$.b','bbb')`
���`{"a":456,"s":"abc"}`

����ɾ���ڵ�
`JSON_REMOVE(json_doc, path[, path] ...)`
���������ɾ����Ӧ����,�������κα䶯
`select json_replace('{"a":1,"s":"abc"}','$.a','$.b')`
���`{"s":"abc"}`

�漰����ʱ������������`json_set`����һ��
`select json_insert('{"a":1}','$[0]',456)`
������䣬��Ϊ`0`Ԫ���Ѿ������ˣ�ע������������`[{"a":1}]`

`select json_insert('{"a":1}','$[999]',456)`
���׷�ӵ������β`[{"a":1}��456]`


`select json_replace('{"a":1}','$[0]',456)`
���`456`������`[456]`

`select json_replace('{"a":1}','$[1]',456)`
������䡣

��ʵ����`json_insert`��`json_replace`��˵һ�����û��Ҫ�������ʹ�á�



`select json_remove('{"a":1}','$[0]')`
������䣡

`select json_remove('[{"a":1}]','$[0]')`
���`[]`

��֮�漰�����ʱ��ҪС�ġ�


`JSON_MERGE(json_doc, json_doc[, json_doc] ...)`
�����doc�ϲ�

`select json_merge('[1,2,3]','[4,5]')`
���`[1,2,3,4,5]`��

### �������չ

`select json_merge('{"a":1}','{"b":2}')`
���`{"a":1,"b":2}`����������ֱ���ںϡ�

����Ļ���������
`select json_merge('123','45')`
���`[123,45]`�����������������

`select json_merge('{"a":1}','[1��2]')`
���`[{"a":1},1,2]`��Ŀ���������飬��ת����`[doc]`

`select json_merge('[1,2]','{"a":1}')`
���`[1,2,{"a":1}]`�������鶼׷�ӵ�������档


`JSON_ARRAY_APPEND(json_doc, path, val[, path, val] ...)`
��ָ���Ľڵ㣬���Ԫ�أ�����ڵ㲻�����飬����ת����`[doc]`

`select json_Array_append('[1,2]','$','456')`
���`[1,2,456]`

`select json_Array_append('[1,2]','$[0]','456')`
���`[[1,456],2]`��ָ������`$[0]`����ڵ㣬����ڵ�����飬���Ե�ЧΪ
`select json_Array_append('[[1],2]','$[0]','456')`


`JSON_ARRAY_INSERT(json_doc, path, val[, path, val] ...)`
�������ָ���±괦����Ԫ��

`SELECT JSON_ARRAY_INSERT('[1,2,3]','$[1]',4)`
���`[1,4,2,3]`����`$`������±�1������

`SELECT JSON_ARRAY_INSERT('[1,[1,2,3],3]','$[1][1]',4)`
���`[1,[1,4,2,3],3]`����`$[1]`������±�1������

`SELECT JSON_ARRAY_INSERT('[1,2,3]','$[0]',4,'$[1]',5)`
���`[4,5,1,2,3]`��ע�������������ǰ���������ϵģ�����`[4,1,5,2,3]`


��ȡ`json`��Ϣ�ĺ���
`JSON_KEYS(json_doc[, path])`
����ָ��`path`��`key`

`select json_keys('{"a":1,"b":2}')`
���`["a","b"]`

`select json_keys('{"a":1,"b":[1,2,3]}','$.b')`
���`null`������û��`key`


`JSON_CONTAINS(json_doc, val[, path])`
�Ƿ�������ĵ�

```shell
select json_contains('{"a":1,"b":4}','{"a":1}')
���1

select json_contains('{"a":2,"b":1}','{"a":1}')
���0

select json_contains('{"a":[1,2,3],"b":1}','[1,2]','$.a')
���1�������������Ҫ����Ԫ�ض����ڡ�

select json_contains('{"a":[1,2,3],"b":1}','1','$.a')
���1��Ԫ�ش�������Ԫ���С�
```

`JSON_CONTAINS_PATH(json_doc, one_or_all, path[, path] ...)`
���·���Ƿ����

```shell
select JSON_CONTAINS_PATH('{"a":1,"b":1}', 'one','$.a','$.c')
���1��ֻҪ����һ��

select JSON_CONTAINS_PATH('{"a":1,"b":1}', 'all','$.a','$.c')
���0������ȫ�����ڡ�


select JSON_CONTAINS_PATH('{"a":1,"b":{"c":{"d":1}}}', 'one','$.b.c.d')
���1��

select JSON_CONTAINS_PATH('{"a":1,"b":{"c":{"d":1}}}', 'one','$.a.c.d')
���0��
```

`JSON_EXTRACT(json_doc, path[, path] ...)`
���doc��ĳ�������ڵ��ֵ��

```shell
select json_extract('{"a":1,"b":2}','$.a')
���1

select json_extract('{"a":[1,2,3],"b":2}','$.a[1]')
���2


select json_extract('{"a":{"a":1,"b":2,"c":3},"b":2}','$.a.*')
���[1,2,3]��a.*ͨ��a�������Ե�ֵ���س����顣


select json_extract('{"a":{"a":1,"b":2,"c":3},"b":4}','$**.b')
���[2,4]��ͨ��$�����в���µ�����b��ֵ���س����顣
```

mysql5.7.9��ʼ������һ�ּ�д��ʽ��column->path

```shell
select id,js->'$.id' from t where js->'$.a'=1 order by js->'$.b'
# �ȼ���
select id,json_extract(js,'$.id') 
from t where json_extract(js,'$.a')=1
order by json_extract(js,'$.b')
```


`JSON_SEARCH(json_doc, one_or_all, search_str[, escape_char[, path] ...])`
ǿ��Ĳ�ѯ������������doc�з��ط��������Ľڵ㣬select�����ڱ��з��ط���Ҫ��ļ�¼��

`select json_search('{"a":"abc","b":{"c":"dad"}}','one','%a%')`

���`$.a`����`like`һ��������`%`��`_`ƥ�䣬�����нڵ��ֵ��ƥ�䣬oneֻ����һ����

```shell
select json_search('{"a":"abc","b":{"c":"dad"}}','all','%a%')
# ���["$.a","$.b.c"]


select json_search('{"a":"abc","b":{"c":"dad"}}','all','%a%',null,'$.b')
# ���["$.b.c"]�����Ʋ��ҷ�Χ��

select json_search('{"a":"abc","b":{"c":"dad"},"c":{"b":"aaa"}}','all','%a%',null,'$**.b')
# ���["$.b.c","$.c.b"]�����ҷ�Χ����ʹ��ͨ�������ÿ��ƥ��ڵ�����²��ҡ�
```

ע�⣬ֻ��json_extract��json_search�е�path��֧��ͨ�䣬����json_set,json_insert�ȶ���֧�֡�


`JSON_LENGTH(json_doc[, path])`
��������ĳ��ȣ������object�������Ը�����������Ϊ`1`

```shell
select json_length('[1,2,3]')
���3

select json_length('123')
���1

select json_length('{"a":1,"b":2}')
���2

���ٸ�path����
select json_length('{"a":1,"b":[1,2,3]}','$.b')
���3
```

`JSON_DEPTH(json_doc)`
����`doc`���

```shell
select json_depth('{}')��json_depth('[]'),json_depth('123')
���1,1,1

select json_depth('[1,2,3,4,5,6]')
���2

select json_depth('{"a":{"b":{"c":1}}}')
���4
```

