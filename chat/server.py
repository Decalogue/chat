# -*- coding:utf8 -*-
# PEP 8 check with Pylint
"""Create and start NLU TCPServer with socketserver.
创建并启动语义理解服务器。

The socketserver module simplifies the task of writing network servers.
"""
import os
import json
import socketserver
from .config import getConfig
from .qa import Robot
from .mytools import get_current_time
from .ianswer import answer2xml

# 初始化语义服务器
logpath = getConfig("path", "log")
robot = Robot(password=getConfig("neo4j", "password"))


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
            elif "config_content" in json_data.keys():
                answer = robot.configure(info=json_data["config_content"], \
                userid=json_data["userid"])
                info = json_data["config_content"]
            print(answer)
            result = answer2xml(answer)
            print(result)
            # step 3.Send
            try:
                # json 格式接口
                # if json_data['return_type'] == 'json':
                    # self.request.sendall(json.dumps(answer).encode("UTF-8"))
                # xml 格式接口
                # elif json_data['return_type'] == 'xml':
                    # self.request.sendall(answer2xml(answer).encode("UTF-8"))
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
                    file.write("Config: " + " ".join(result) + "\n")
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
    start()
	