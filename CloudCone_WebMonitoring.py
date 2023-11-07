# encoding:utf-8
# 风之翼灵
# www.fungj.com
# CloudCone VPS库存监控的脚本，当有货时发送到指定邮箱
import re
import smtplib
import time
import urllib.request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 监控地址
url = 'https://app.cloudcone.com/vps/205/create?token=pre-bf-vps-23-2'

DEFAULT_HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Referer': '{url}',
}


def main():
    # 打开URL并获取页面内容
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    resp = urllib.request.urlopen(req).read().decode('utf-8')
    # 寻找关键字
    pattern = r'This plan is out of stock\. You might find our'
    matches = re.findall(pattern, resp)
    if matches:
        # 无货
        print(str(nowtime) + '无货')
    else:
        # 有货，发邮件通知
        send_mail()
        print(str(nowtime) + '有货')


def send_mail():
    # 发送邮件提醒
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # 添加正文内容
    msg.attach(MIMEText(html_content, 'html'))
    # 连接到QQ邮箱的SMTP服务器
    try:
        server = smtplib.SMTP("smtp.qq.com", 587)  # QQ邮箱SMTP服务器地址和端口号
        server.starttls()  # 使用TLS加密
        server.login(sender_email, password)

        # 发送邮件
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败:", str(e))
    finally:
        server.quit()


# 执行方法

if __name__ == '__main__':
    while True:
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 休眠时间
        time.sleep(185)
        print('---------' + str(nowtime) + ' 程序开始执行------------')
        # 设置发件人邮箱和授权码
        sender_email = "your_email@qq.com"
        password = "your_password"  # 在QQ邮箱中生成的授权码

        # 设置收件人邮箱
        recipient_email = "recipient_email@example.com"
        # 创建邮件内容
        subject = "cloudcone pre-bf-vps-23-2到货通知"
        html_content = """
    <html>
    <head></head>
    <body>
        <h4>cloudcone pre-bf-vps-23-2到货通知</h4>
        <p>库存更新时间：{code}</p>
        <p>购买地址：</p>
        <p><h2><a href="{url}" target="_blank">链接</a></h2></p>
    </body>
    </html>
    """.format(code=str(nowtime), url=url)
        # 执行
        main()
