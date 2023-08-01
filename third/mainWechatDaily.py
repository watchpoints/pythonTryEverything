#!/usr/bin/python3
# coding=utf-8
import Iciba


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
    icb = Iciba.iciba(wechat_config)

    '''
    run()方法可以传入openids列表，也可不传参数
    不传参数则对微信公众号的所有用户进行群发
    '''
    icb.run(openids)


if __name__ == '__main__':
    wechat_every_daily()
