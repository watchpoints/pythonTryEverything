import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import sleep
from threading import Thread
from flask import Flask, request, jsonify
from queue import Queue

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
import signal

from wechat import push_get_up
from putdonwphone import mykuaishou

# import wechat.push_get_up

q = Queue(100)  # 创建一个先进先出的队列


# 定义消费者线程
class Consumer(Thread):

    def run(self):
        global q
        while True:
            logging.info('消费者线程开始消费线程了')
            msg = q.get()  # 默认阻塞
            logging.info('消费线程得到了数据：{}'.format(msg))
            sleep.send_msg_to_blog(msg)


LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
#  https://github.com/zhayujie/bot-on-anything
# https://github.com/zhayujie/chatgpt-on-wechat

# set token or get from environments 三个参数是可以的
TOKEN = os.getenv("WECHAT_TOKEN", "testtest")
AES_KEY = os.getenv("WECHAT_AES_KEY", "Quk4OepZpDVkhWnevUNnOXfoynwT1gg83cYdBpaZXYP")
APPID = os.getenv("WECHAT_APPID", "wx94e03776e64ee600")

app = Flask(__name__)


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == "text":
            content = " 加油，小王同学，我相信你一定能做到 \n"
            content = content + msg.content
            logging.info(content)
            global q
            q.put(content)
            reply = create_reply(content, msg)
        else:
            reply = create_reply("Sorry, can not handle this for now", msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == "text":
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply("Sorry, can not handle this for now", msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/json', methods=['POST'])
def example():
    if request.method == 'POST':
        # 从 POST 请求的 JSON 数据中获取参数
        data = request.json
        name = data.get('name')
        age = data.get('age')

        # 在服务端进行一些处理
        # ...

        # 返回 JSON 格式的响应
        response = {'message': 'Hello, {}, you are {} years old.'.format(name, age)}
        return jsonify(response)


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException("Function execution timed out.")


def markdown_to_wechat():
    # 微信公共号文章发布
    push_get_up.markdown_to_wechat()


def EeasyHabitSleep():
    # 设置超时时间
    signal.alarm(3600)
    try:
        sleep.show_sleep()
        mykuaishou.interface_auo_upload_kuaishou()
    finally:
        # 取消超时设置
        signal.alarm(0)


def StartForTest():
    # 设置超时时间
    signal.alarm(3600)
    try:
        sleep.show_sleepForTest()
    finally:
        # 取消超时设置
        signal.alarm(0)


if __name__ == "__main__":
    # 设置超时时间为20分钟
    signal.signal(signal.SIGALRM, timeout_handler)

    # not  execute logging  fucntion before  here
    logging.basicConfig(level=logging.DEBUG,
                        format=LOG_FORMAT,
                        datefmt=DATE_FORMAT,
                        filename="./pythonTryEverything.log"
                        )

    logging.info("""
        ┌──────────────────────────────────────────────────────────────────────┐
        │                                                                      │    
        │                      •  Start Beemove  •                             │
        │                                                                      │
        └──────────────────────────────────────────────────────────────────────┘
    """)

    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    StartForTest()
    backsched = BackgroundScheduler(job_defaults=job_defaults, timezone='Asia/Shanghai')
    backsched.add_job(EeasyHabitSleep, CronTrigger.from_crontab("30 6 * * *"), id="do_show_sleep_job")
    backsched.add_job(markdown_to_wechat, CronTrigger.from_crontab("10 6 * * *"), id="markdown_to_wechat")
    # backsched.add_job(sleep.show_sleep, CronTrigger.from_crontab("0 6 * * *"), id="do_show_sleep_job")
    backsched.start()

    t2 = Consumer()
    t2.start()
    # server_address = ("", 8089)
    # httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    # httpd.serve_forever()
    # host: 绑定的ip(域名)
    # port: 监听的端口号
    # debug: 是否开启调试模式
    app.run(host="0.0.0.0", port=80, debug=True, use_reloader=False)
    # export FLASK_APP=xx.py  # 指定flask应用所在的文件路径
    # export FLASK_ENV=development  # 设置项目的环境, 默认是生产环境
    # flask run -h 0.0.0.0 -p 8000  # 启动测试服务器并接受请求
    # http://127.0.0.1:8000/
