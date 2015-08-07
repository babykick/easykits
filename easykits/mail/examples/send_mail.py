#coding=utf-8

import sys
sys.path.append(r"F:\programing\python\app\mypackages\easykits")
from easykits import Mailbox


YOUR_USERNAME = ""
YOUR_PASSWORD = ""

if __name__ == '__main__':
    mb = Mailbox('139', YOUR_USERNAME, YOUR_PASSWORD, "smtp.139.com", "pop.139.com")
     
    success = mb.sendMail(to="someone@gmail.com",
                          subject="test".decode('utf-8') ,
                          content="content")
   
    for mail in mb.mails:
        print 'from', mail.getSenderAddress()
        print 'subject:', mail.getSubject(),"\n"
       

