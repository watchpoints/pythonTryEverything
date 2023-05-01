import logging
import signal

import weibo
import toutiao
import maimai
import douyu
import myblog
import mycsdn
import dedao
import zhishi


# easy sleep
def show_sleep():
    try:
        myblog.KillChromebeta()
        logging.info("22点打卡，关机睡觉，手机一定要放客厅")
        # weibo.post_sleep_weibo()
        # 微博定时提醒
        myblog.KillChromebeta()
        toutiao.post_sleep_toutiao()  # easy sleep

        # 斗鱼时提醒
        myblog.KillChromebeta()
        douyu.post_sleep_douyu()
        # 脉脉定时提醒
        myblog.KillChromebeta()
        maimai.post_sleep_maimai()

        # 脉脉定时提醒
        myblog.KillChromebeta()
        mycsdn.send_msg_to_csdn(myblog.query_sleep_content())

        # 得到定时提醒
        myblog.KillChromebeta()
        dedao.send_msg_to_dedao(myblog.query_sleep_content())

        # 知识星球定时提醒
        myblog.KillChromebeta()
        zhishi.send_msg_to_zhishi(myblog.query_sleep_content())
    finally:
        print("end")


def send_msg_to_blog(wechat_txt: str):
    try:
        logging.debug("send_msg_to_blog:" + wechat_txt)
        myblog.KillChromebeta()
        # if not weibo.send_msg_to_weibo(wechat_txt):
        #     print("post weibo failed")
        #     logging.error("post weibo failed")

        print("post send_msg_to_toutiao")
        myblog.KillChromebeta()
        if not toutiao.send_msg_to_toutiao(wechat_txt):
            logging.error("post toutiao failed")
        print("post send_msg_to_douyu")
        myblog.KillChromebeta()
        if not douyu.send_msg_to_douyu(wechat_txt):
            logging.error("post douyu failed")
        print("post send_msg_to_maimai")
        myblog.KillChromebeta()
        if not maimai.send_msg_to_maimai(wechat_txt):
            logging.error("post maimai failed")

        myblog.KillChromebeta()
        if not mycsdn.send_msg_to_csdn(wechat_txt):
            logging.error("post mycsdn failed")

        myblog.KillChromebeta()
        if not dedao.send_msg_to_dedao(wechat_txt):
            logging.error("post dedao failed")

        myblog.KillChromebeta()
        if not zhishi.send_msg_to_zhishi(wechat_txt):
            logging.error("post send_msg_to_zhishi failed")

    finally:
        signal.alarm(0)  # 成功完成任务，取消超时信号
        print("end")


if __name__ == '__main__':
    # send_msg_to_blog("this is a test")
    myblog.KillChromebeta()
    if not zhishi.send_msg_to_zhishi("testtest"):
        logging.error("post send_msg_to_zhishi failed")
