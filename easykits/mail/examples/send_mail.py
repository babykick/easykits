#coding=utf-8
from mykits import MailBox
    
      
if __name__ == '__main__':
    # mb = Mailbox('139', YOUR_USERNAME, YOUR_PASSWORD, "smtp.139.com", "pop.139.com")
    mb = Mailbox('139', 'babykick', 'hacker', "smtp.139.com", "pop.139.com")
    success = mb.sendMail(to="babykick@139.com",
                          subject="test".decode('utf-8') ,
                          content="content")
   
    for mail in mb.mails:
        print 'from', mail.getSenderAddress()
        print 'subject:', mail.getSubject(),"\n"
        
          
    
    # 
    # set_account('13907309206','hacker')
    # mailNumber = "13907309206"
    # title = "[robot]测试短信"
    # text="==============\n本条信息由机器人程序自动发送"
    # if send_mail("陈路".decode('utf-8'),mailNumber.decode('utf-8'),title.decode('utf-8') , text.decode('utf-8') , attachFile="maillib139.py"):
    #     print mailNumber,"发送成功".decode('utf-8')
    # else:
    #     print mailNumber,'发送失败'.decode('utf-8')
    # 
    # 

