import elasticsearch
import time

# es 相关操作
class ES(object):
    def __init__(self, data, index_name):
        """
        实例化 es 对象
        :param data: 字典类型
        """
        self.es = elasticsearch.Elasticsearch(hosts="your hosts", http_auth=("account", "password"))
        self.data = data
        self.index = index_name

    def buildmapping(self):
        """
        创建 mapping 并返回状态信息
        :return: 无返回结果
        """
        # 构造 mapping
        mapping = {
            "settings": {
                "index": {
                # 刷新间隔
                    "refresh_interval": "3s"
                },
                # 副本数
                "number_of_replicas": "0",
                # 切片（分布在每个节点上的切片）
                "number_of_shards": "1"
            },
            "mappings": {
                "_doc": {
                    "dynamic_templates": [
                        {
                            "string_fields": {
                                "match": "*",
                                "match_mapping_type": "string",
                                "mapping": {
                                    "type": "keyword",
                                    "norms": "false"
                                }
                            }
                        }
                    ]
                }
            }
        }

        # 创建索引
        R = self.es.indices.create(index=self.index, body=mapping)
        print(R)

    def insertdata(self):
        """
        1.id暂定为当前时间戳
        2.插入文档到 es 中
        :return: 无法返回结果
        """
        id = str(time.time())
        self.es.create(index=self.index, body=self.data, id=id)

    def router(self):
        """
        1.查询 es 中是否存在此索引
        2.存在的话直接存储数据
        3.不存在的话先创建索引再存储数据
        :return: 无返回
        """
        try:
            response = self.es.search(index=self.index)
            if response:
                print("此索引已经存在，开始存储数据...")
                try:
                    self.insertdata()
                    print("存储完成")
                except Exception as e:
                    print(e)

        except elasticsearch.exceptions.NotFoundError:
            print("查无此索引，正在创建...")
            self.buildmapping()
            print("索引创建完成，开始存储数据...")
            self.insertdata()
            print("存储完成")
