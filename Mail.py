from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr




import smtplib
class Mail(object):
	def __init__(self, target = ""):
		self.frommail = '2822743310@qq.com'		#发件箱
		self.frompass = 'ibozzvgziyisdgia'		#邮箱密码
		self.target = target
		self.smtp_server = 'smtp.qq.com'		#邮箱smtp地址
		
	def format_addr(self, s):
		name,	addr = parseaddr(s)
		return formataddr((Header(name, 'utf-8').encode(), addr))
		
	def sendMail(self, conent):		#send mail, and inspert the content into the mod
		msg = MIMEText('<html><body><h1>Haka机器人情报通告</h1>' + conent + '</body></html>', 'html', 'utf-8')
		msg['From'] = self.format_addr('HakaRb <%s>' % self.frommail)
		msg['To'] = self.format_addr('Haka <%s>' % self.target)
		msg['Subject'] = Header('学术活动通知', 'utf-8').encode()

		server = smtplib.SMTP(self.smtp_server, 25)
		server.set_debuglevel(1)
		server.login(self.frommail, self.frompass)
		server.sendmail(self.frommail, [self.target], msg.as_string())
		server.quit()
		return

if __name__ == '__main__':
	mail = Mail('282271296@qq.com')
	mail.sendMail('this is test')
	
	