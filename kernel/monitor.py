import smtplib
from email.mime.text import MIMEText
import urllib.parse
import sys
from email.utils import encode_rfc2231

# 第三方 SMTP 服务
mail_host = "smtp.163.com"      # SMTP服务器
mail_user = "@163.com"        # 用户名 邮件地址
mail_pass = "CQOVOIJPBSCYVOBQ" # 授权密码，非登录密码
 
sender ="@163.com"   # 发件人邮箱(最好写全, 不然会失败)
receivers = ['@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


title = 'tell'  # 邮件主题 中文怎么处理
 
def sendEmail(content):
 
    message = MIMEText(urllib.parse.quote(content), 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = urllib.parse.quote(title)
 
    try:
        # https://docs.python.org/3/library/smtplib.html
        smtpObj = smtplib.SMTP_SSL(mail_host)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user,mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

if __name__ == '__main__':
    # 打印语言默认编码
    print(f"defaultencoding--{sys.getdefaultencoding()}")
    # 打印系统配置的编码
    print(f"filesystemencoding--{sys.getfilesystemencoding()}")

    # 最后尝试打印中文
    sendEmail("this is text")
