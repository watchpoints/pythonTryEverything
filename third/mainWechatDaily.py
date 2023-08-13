#!/usr/bin/python3
# coding=utf-8
import json
import ssl
import sys
import os

import requests

#sys.path.append("../kernel")
#from kernel import interface_db


class iciba:
    # 初始化
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid'].strip()
        self.appsecret = wechat_config['appsecret'].strip()
        self.template_id = wechat_config['template_id'].strip()
        self.access_token = ''

    # 错误代码
    @staticmethod
    def get_error_info(errcode):
        return {
            40013: '不合法的 AppID ，请开发者检查 AppID 的正确性，避免异常字符，注意大小写',
            40125: '无效的appsecret',
            41001: '缺少 access_token 参数',
            40003: '不合法的 OpenID ，请开发者确认 OpenID （该用户）是否已关注公众号，或是否是其他公众号的 OpenID',
            40037: '无效的模板ID',
        }.get(errcode, 'unknown error')

    # 打印日志
    def print_log(self, data, openid=''):
        errcode = data['errcode']
        errmsg = data['errmsg']
        if errcode == 0:
            print(' [INFO] send to %s is success' % openid)
        else:
            print(' [ERROR] (%s) %s - %s' % (errcode, errmsg, self.get_error_info(errcode)))
            if len(openid) > 0:
                print(' [ERROR] send to %s is error' % openid)
            sys.exit(1)

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            appid, appsecret)
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            self.access_token = data['access_token']

    # 获取用户列表
    def get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % self.access_token
        r = requests.get(url)
        data = json.loads(r.text)
        if 'errcode' in data:
            self.print_log(data)
        else:
            openids = data['data']['openid']
            return openids

    # 发送消息
    def send_msg(self, openid, template_id, iciba_everyday):
        #getup = interface_db.get_up_everyday()
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': iciba_everyday['fenxiang_img'],
            'data': {
                'content': {
                    'value': iciba_everyday['content'],
                    'color': '#0000CD'
                    },
                'note': {
                    'value': iciba_everyday['note'],
                },
                'translation': {
                    'value': iciba_everyday['translation'],
                }
            }
        }
        json_data = json.dumps(msg)
        print("json_data=" + json_data)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % self.access_token
        r = requests.post(url, json_data)
        print("send is ok")
        return json.loads(r.text)

    # 获取爱词霸每日一句
    @staticmethod
    def get_iciba_everyday():
        url = 'http://open.iciba.com/dsapi/'
        r = requests.get(url)
        print(url)
        return json.loads(r.text)

    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        everyday_words = self.get_iciba_everyday()
        print(everyday_words)
        for openid in openids:
            openid = openid.strip()
            result = self.send_msg(openid, self.template_id, everyday_words)
            self.print_log(result, openid)

    # 执行
    def run(self, openids=[]):
        print("run....")
        if not openids:
            # 如果openids为空，则遍历用户列表
            openids = self.get_user_list()
        # 根据openids对用户进行群发
        self.send_everyday_words(openids)


# https://mp.weixin.qq.com/debug/cgi-bin/sandboxinfo?action=showinfo&t=sandbox/index

def wechat_every_daily():
    # 微信配置
    wechat_config = {
        'appid': 'wxb547e7b33f80bb5a',  # (No.1)此处填写公众号的appid
        'appsecret': '4ff76e73733313eb2f2a88789cc6c4db',  # (No.2)此处填写公众号的appsecret
        'template_id': '18upwZQ0jMHVbAcWHR8VyTtYse73ku2SKLMEnyJHgFA'  # (No.3)此处填写公众号的模板消息ID
    }

    # 用户列表
    openids = [
        'o28Ze5kirj4l5QW_DGLImkth_9JY',  # (No.4)此处填写你的微信号（微信公众平台上的微信号）
        'o28Ze5p3AXcHZBLYxZv77klCVWnk',  # 如果有多个用户也可以
        # 'xxxxx',
    ]

    # 执行
    icb = iciba(wechat_config)

    '''
    run()方法可以传入openids列表，也可不传参数
    不传参数则对微信公众号的所有用户进行群发
    '''
    icb.run(openids)


if __name__ == '__main__':
    wechat_every_daily()
