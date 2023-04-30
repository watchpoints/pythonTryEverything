import logging
import weibo
import os
import toutiao
import maimai
import douyu
import time

# easy sleep
def show_sleep():
    os.system("ps -ef | grep google-chrome  | grep -v grep | awk '{print $2}' | xargs kill")
    logging.info("22点打卡，关机睡觉，手机一定要放客厅")
    weibo.post_sleep_weibo()
    weibo.post_sleep_weibo()

    toutiao.post_sleep_toutiao()  # easy sleep
    toutiao.post_sleep_toutiao()  # easy sleep

    # 斗鱼
    douyu.post_sleep_douyu()
    douyu.post_sleep_douyu()
    maimai.post_sleep_maimai()
    maimai.post_sleep_maimai()
    
    
def send_msg_to_blog(wechat_txt:str):
    logging.debug("send_msg_to_blog:" +wechat_txt)
    if weibo.send_msg_to_weibo(wechat_txt) == False:
        print("post weibo failed")
        logging.error("post weibo failed")
        
    print("post send_msg_to_toutiao")
    if toutiao.send_msg_to_toutiao(wechat_txt) ==False:
       logging.error("post toutiao failed")
    print("post send_msg_to_douyu")
    if douyu.send_msg_to_douyu(wechat_txt) == False:
        logging.error("post douyu failed")
    print("post send_msg_to_maimai")
    if maimai.send_msg_to_maimai(wechat_txt) == False:
        logging.error("post maimai failed")
  
if __name__ == '__main__':
    send_msg_to_blog("this is a test")  
    
    
