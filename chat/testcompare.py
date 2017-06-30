# 连接数据库
graph = Graph("http://localhost:7474/db/data", password="train")
# 选择器初始化
selector = NodeSelector(graph)
# 查询测试标准节点
ts_node = selector.select("TestStandard", question="你的标准问题")
# ts_node就是一整条记录，包含question, content, context, behavior, parameter, url这六项。
# 比如你问“你好”，把从我那里得到的答案和ts_node内容比较就可以了。具体怎么比较要看你的思路。