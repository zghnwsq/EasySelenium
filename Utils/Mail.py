import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import Settings


def send_mail(subject='Subject:', text=None, attachment=None):
    sender = Settings.SENDER
    code = Settings.SMTP_CODE
    receivers = Settings.RECEIVERS
    try:
        msg = MIMEMultipart()
        # header
        msg['From'] = formataddr([Settings.SENDER_NAME, sender])
        for item in receivers:
            msg['To'] = formataddr([item, item])
        msg['Subject'] = Header(subject, charset='utf-8')
        # 正文
        body = text or ''
        body = MIMEText(body, _subtype='plain', _charset='utf-8')
        # body['From'] = formataddr([Settings.SENDER_NAME, sender])
        # for item in receivers:
        #     body['To'] = formataddr([item, item])
        # body['Subject'] = Header('测试', charset='utf-8')
        msg.attach(body)
        # 附件
        with open(attachment, 'r') as html:
            content = html.read()
        if content:
            print(content)
            file = MIMEText(content, _subtype='html', _charset='utf-8')
            file['Content-Type'] = 'application/octet-stream'
            file["Content-Disposition"] = 'attachment; filename="20190903_225710.html"'
            msg.attach(file)

            server = smtplib.SMTP_SSL('smtp.sina.cn', 465)
            server.login(sender, code)
            server.sendmail(sender, receivers, msg.as_string(),)

            server.quit()
            print('邮件发送成功!')
    except Exception as e:
        print('邮件发送失败!')
        print(e)




