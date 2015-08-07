#coding=utf-8
#refer:http://forum.ubuntu.org.cn/viewtopic.php?t=289471


'''
A SMTP mail agent tool for 139 mail.
Useful for automation of mail sending  with  mobile short message notification provided by 139 mail box. 
'''

import smtplib, mimetypes
import sys
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage  
import time

reload(sys)
sys.setdefaultencoding('utf-8')
 
#mail configeration
send_mail_host = "smtp.139.com"  #sender smtp server
sender_mail_postfix = "139.com"  #sender domain
get_main_host = "pop.139.com"    #receiver pop server
get_mail_postfix = "139.com"     #receiver domain

sender_user_number = ''
sender_mail_pswd = ''


 
    

def set_account(name,pwd):
    '''Set the User account
    name: user name of mail account
    pwd:  user password of mail account
    '''
    
    global sender_user_number,sender_mail_pswd
    sender_user_number=name
    sender_mail_pswd=pwd
    
    
def send_mail(appearName,receiverNumber,subject,content, attachFile=None):
    '''
    appearName:  displayed sender's name in mail
    receiverNumber: mobile number of receiver as mail address
    subject:  subject of mail
    content:  content of mail
    '''
    
    sender_mail_address = appearName.encode('gb2312') + "<" + sender_user_number + "@" + sender_mail_postfix + ">"
   
 
    msg = MIMEMultipart()  
    msg['Subject'] = subject
    msg['From'] = sender_mail_address
    msg['to'] = to_adress="139SMSserver<" + receiverNumber + "@" + get_mail_postfix + ">"
    msg.attach(MIMEText(content, _charset='utf-8'))
    if attachFile:
        _attach_file(attachFile, msg)
         
    try:
        stp = smtplib.SMTP()
        stp.connect(send_mail_host)
        stp.login(sender_user_number, sender_mail_pswd)
        stp.sendmail(sender_mail_address, to_adress, msg.as_string())
        stp.quit()
        stp.close()
        return True
    except Exception, e:
        print str(e)
        return False



def _attach_file(fileName, msg):
    ctype, encoding = mimetypes.guess_type(fileName)   
    if ctype is None or encoding is not None:   
        ctype = 'application/octet-stream'  
    maintype, subtype = ctype.split('/', 1)   
    att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)   
    att1.add_header('Content-Disposition', 'attachment', filename = fileName)   
    msg.attach(att1)
    
    
 
if __name__ == '__main__':
    set_account('13907309206','hacker')
    mailNumber = "13907309206"
    title = "[robot]测试短信"
    text="==============\n本条信息由机器人程序自动发送"
    if send_mail("陈路".decode('utf-8'),mailNumber.decode('utf-8'),title.decode('utf-8') , text.decode('utf-8') , attachFile="maillib139.py"):
        print mailNumber,"发送成功".decode('utf-8')
    else:
        print mailNumber,'发送失败'.decode('utf-8')
 