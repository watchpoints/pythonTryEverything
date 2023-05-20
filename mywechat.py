import itchat

def wechat_send(msg):
    # 登录微信
    itchat.auto_login(hotReload=True)
    # 发送消息
    #itchat.send('Hello, World!', toUserName='小王同学')
    # 获取好友列表
    friends = itchat.get_friends()

    # 获取文件传输助手的username
    for friend in friends:
        print(friend)
        if friend['RemarkName'] == '文件传输助手':
            filehelper_username = friend['UserName']
            break


    itchat.logout()

if __name__ == '__main__':
    wechat_send("")