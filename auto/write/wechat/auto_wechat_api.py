import os
from urllib import parse, request
import requests
import time
import json
from datetime import datetime
from werobot import WeRoBot


def NewClient():
    robot = WeRoBot()
    robot.config["APP_ID"] = os.getenv('WECHAT_APP_ID')
    robot.config["APP_SECRET"] = os.getenv('WECHAT_APP_SECRET')
    my_client = robot.client
    return my_client


def get_image_list():
    client = NewClient()
    try:
        media_json = client.get_media_list("image", 0, 20)  ##永久素材
        print(media_json)
    except Exception as e:
        print("upload image error: {}".format(e))


# 此函数用于获取
def get_access_token():
    """
        get_access_token
    """
    try:
        appid = "wx94e03776e64ee600"
        appsecret = "9affd2c7c49adefb92660a8095cbbf7c"
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            appid, appsecret)
        r = requests.get(url)
        data = json.loads(r.text)
        print("get_access_token:{}".format(data))
        if 'errcode' in data:
            return False, False
        else:
            access_token = data['access_token']
            print('access_token:', (access_token, time.time()))
            return access_token, time.time()

    except Exception as e:
        print(e)
        return False, False


class Caogao(object):

    def __init__(self, name, data, access_token, getTokenTime):
        self.name = name
        self.data = data
        self.access_token = access_token
        self.getTokenTime = getTokenTime

    # 先判断是否有token，如果没有，获取token，同时记录时间，获取后开始干活儿，
    # 如果有，判断是否失效，失效则重新获取，
    # 判断token是否过期
    def which_token_abate(self):
        # 获取token时间戳
        # global getTokenTime
        # 获取当前时间戳
        nowtime_stamp = time.time()
        # 用当前时间戳减去getTokenTime，大于两个小时就判定失效
        hour2 = 2 * 60 * 60 * 1000
        if nowtime_stamp - self.getTokenTime > hour2:
            return True
        return False

    # 判断是否有token
    def have_token(self):
        if self.access_token != '':
            return True
        return False

    # 发送数据，data为要发的内容
    def send_requests(self):
        # 2.导入requests包,发送post
        try:
            header_dict = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
                'Content-Type': 'application/json; charset=utf-8'
            }
            response_post = requests.post(
                url='https://api.weixin.qq.com/cgi-bin/draft/add?',
                params={
                    'access_token': self.access_token},
                headers=header_dict,
                data=bytes(json.dumps(self.data, ensure_ascii=False).encode('utf-8'))
                # data=self.data,
            )
            resp = json.loads(response_post.text)
            print(resp)
            media_id = resp['media_id']
            print(media_id)
            return media_id
        except Exception as e:
            print(e)
        return ''


class FreePublish(object):
    def __init__(self, name, media_id, access_token):
        self.name = name
        self.media_id = media_id
        self.access_token = access_token

    # 发送数据，data为要发的内容
    # https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html
    def send_requests(self):
        # 2.导入requests包,发送post
        errcode = -1
        try:
            media_id = {
                'media_id': self.media_id
            }

            postUrl = "https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=%s" % self.access_token
            r = requests.post(postUrl, data=bytes(json.dumps(media_id, ensure_ascii=False).encode('utf-8')))

            resp = json.loads(r.text)
            print(resp)
            publish_id = resp['publish_id']

        except Exception as e:
            print(e)
        return publish_id


# 发布状态轮询接口
class FreePublishGet(object):
    def __init__(self, name, access_token, publish_id):
        self.name = name
        self.access_token = access_token
        self.publish_id = publish_id

    # 发送数据，data为要发的内容
    # https://developers.weixin.qq.com/doc/offiaccount/Publish/Get_status.html
    def send_requests(self):
        # 2.导入requests包,发送post
        publish_status = -1
        try:
            publish_id = {
                'publish_id': self.publish_id
            }

            postUrl = "https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token=%s" % self.access_token
            r = requests.post(postUrl, data=bytes(json.dumps(publish_id, ensure_ascii=False).encode('utf-8')))

            resp = json.loads(r.text)
            print(resp)
            publish_status = resp['publish_status']

        except Exception as e:
            print(e)
        return publish_status


def markdown_to_wechat(msg):
    """
     获取token
    """
    my_token, my_time = get_access_token()

    if not my_token:
        print("get_access_token failed")
        return

    # 2.新建草稿
    # https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html
    # interval_days = (datetime.now() - datetime(2023, 9, 27)).days
    # title = "挑战早睡早起100天：第" + str(interval_days) + "天"
    # msg = get_life_task()
    my_articles = {
        "articles": [
            {
                "title": "Ai俱乐部同步更新",
                "author": "小王同学",
                "content": msg,
                # 图文消息的封面图片素材id（必须是永久MediaID）
                "thumb_media_id": "ibkaqGK8sJHhDErJXsz_6EHBJ9Pz90Imfwz3ariI2DZaheJilHR_SY8EgBLp8Ahf",
                "need_open_comment": 1

            }
        ]
        # 若新增的是多图文素材，则此处应有几段articles结构，最多8段
    }
    print(my_articles)

    # 创建草稿实例
    caogao = Caogao('Caogao', my_articles, my_token, my_time)
    media_id = caogao.send_requests()
    if len(media_id) == 0:
        print("caogao failed")
        return False
    time.sleep(5)
    # 发布接口
    freePublish = FreePublish('FreePublish', media_id, my_token)
    publish_id = freePublish.send_requests()
    if publish_id < 0:
        print("FreePublish failed")
    time.sleep(10)
    # 发布状态轮询接口
    time.sleep(5)
    freePublishGet = FreePublishGet('FreePublishGet', my_token, publish_id)
    publish_status = freePublishGet.send_requests()
    print(publish_status)


if __name__ == '__main__':
    markdown_to_wechat("test")

  
