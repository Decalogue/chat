# -*- coding:utf8 -*-
"""Create and start NLU TCPServer with socketserver.
创建并启动语义理解服务器。

The socketserver module simplifies the task of writing network servers.
"""
import os
import json
import socketserver
from .config import getConfig
from .mytools import Walk, get_current_time
from .graph import Database
# from .sql import Database
# from .qa_sql import Robot
from .ianswer import answer2xml
from .qa import Robot


kb = Database()

class WalkUserData(Walk):
    def handle_file(self, filepath, pattern=None):
        kb.handle_excel(filepath)

def add_qa(path=None, names=None):
    """Add subgraph from excel data.
    """
    walker = WalkUserData()
    print(path)
    fnamelist = walker.dir_process(1, path, style="fnamelist")
    print("知识库更新内容:", fnamelist)

# 开机从U盘自动导入知识库
add_qa(path=getConfig("path", "usbkb"))

# 初始化日志路径
logpath = getConfig("path", "log")

# 初始化语义服务器
# 从 qa 初始化
robot = Robot(password=getConfig("neo4j", "password"))
# 从 qa_sql 初始化
# robot = Robot(path=getConfig("path", "db"), password=None)


class MyTCPHandler(socketserver.BaseRequestHandler):
    """The request handler class for nlu server.
    语义理解服务器。

    It is instantiated once per connection to the server, and must override
    the 'handle' method to implement communication to the client.
    """
    def handle(self):
        while True:
			# self.request is the TCP socket connected to the client
            self.data = self.request.recv(2048)
            if not self.data:
                break
            print("\n{} wrote:".format(self.client_address[0]))
            self.data = self.data.decode("UTF-8")
            print("Data:\n", self.data)
            # step 1.Bytes to json obj and extract question
            json_data = json.loads(self.data)
            # step 2.Get answer
            if "ask_content" in json_data.keys():
                answer = robot.search(question=json_data["ask_content"], \
                userid=json_data["userid"])
                info = json_data["ask_content"]
                # 其中 result['picurl'] 为 xml 格式
                result = answer2xml(answer)
            elif "config_content" in json_data.keys():
                answer = robot.configure(info=json_data["config_content"], \
                userid=json_data["userid"])
                info = json_data["config_content"]
                result = answer
            print(answer)
            print(result)
            # step 3.Send
            try:
                self.request.sendall(json.dumps(result).encode("UTF-8"))
            except:
                with open(logpath, "a", encoding="UTF-8") as file:
                    file.write(get_current_time("%Y-%m-%d %H:%M:%S") + "\n" \
                    + "发送失败\n")
            # 追加日志
            with open(logpath, "a", encoding="UTF-8") as file:
                # 写入接收数据中的内容字段
                file.write(get_current_time("%Y-%m-%d %H:%M:%S") + "\n" \
                    + info + "\n")
                # 写入正常问答
                if "ask_content" in json_data.keys():
                    for key in ["question", "content", "behavior", "url", "context", "parameter", "picurl"]:
                        file.write(key + ": " + str(result[key]) + "\n")
                # 写入配置信息
                elif "config_content" in json_data.keys():
                    file.write("Config: " + json.dumps(result) + "\n")
                file.write("\n")


def start(host="localhost", port=7000):
    """Start NLU server.

    Create the server, binding to host and port. Then activate the server.
    This will keep running until you interrupt the program with Ctrl-C.

    Args:
        host: Server IP address. 服务器IP地址设置。
            Defaults to "localhost".
        port: server port. 服务器端口设置。
            Defaults to 7000.
    """
    # 多线程处理并发请求
    sock = socketserver.ThreadingTCPServer((host, port), MyTCPHandler)
    sock.serve_forever()

if __name__ == "__main__":
    # host = getConfig("nluserver", "host")
    # port = getConfig("nluserver", "port")
    # start(host, port)
    start()
	