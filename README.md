# python-elasticsearch
Using elasticsearch in python



### 说明

此脚本是为了工作中提高效率，封装的类。

### 作用

elasticsearch 存储数据，当服务器上没有索引时先创建索引，再插入数据；如果已存在此索引，那么直接插入数据。

### 使用示例

```python
es = ES(data, index_name)
es.router()
```

> data 为**字典**类型**文档**数据
>
> index_name 为**字符串**类型的**索引名**。

### 注意

具体说明可以查看代码中注释部分，可修改 mapping 设置，可以修改 elasticsearch 的主机地址，当然也可以更改文档的 id ，目前已当前处理文档的时间戳作为文档 id。