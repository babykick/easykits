#coding=utf-8
#refer:http://forum.ubuntu.org.cn/viewtopic.php?t=289471


"""
A SMTP mail agent tool for mail.
Automation of mail sending  with  mobile short message notification provided by mail box. 
"""

import smtplib, mimetypes
import sys
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 
from email.mime.image import MIMEImage  
import poplib
from email import parser 
import cStringIO
import base64
import re

# reload(sys)
# sys.setdefaultencoding('utf-8')
#  
 
class Mail:
    """
     Represent email object.
     Included information is encoded.
    """
    def __init__(self):pass
    
    def fill(self, fromAddr, toAddr, title, content, attachFile=None):
        msg = MIMEMultipart()  
        msg['From'] = fromAddr
        msg['to'] = toAddr  #to_adress="139SMSserver<" + receiverNumber + "@" + get_mail_postfix + ">"
        msg['Subject'] = title
        
        if isinstance(content , basestring):
           msg.attach(MIMEText(content, _charset='utf-8'))
        else:
           msg.attach(content)
           
        if attachFile is not None:
            if isinstance(attachFile, basestring):
               self._attachFile(attachFile, msg)
            else:
               msg.attach(attachFile)
                
        self.msg = msg
    
    def fromMsg(self,msg):
        self.msg = msg
    
    def asString(self):
        return self.msg.as_string()
    
    
    def _attachFile(self, fileName, msg):
        ctype, encoding = mimetypes.guess_type(fileName)   
        if ctype is None or encoding is not None:   
            ctype = 'application/octet-stream'  
        maintype, subtype = ctype.split('/', 1)   
        att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)   
        att1.add_header('Content-Disposition', 'attachment', filename = fileName)   
        msg.attach(att1)
        
    def _decode(self, code, encoding="utf-8"):
        try:
           return base64.decodestring(code)   #.encode(encoding)
        except:
           return code
    
    def _decodeHeader(self,code):
        return email.Header.decode_header(code)[0][0]
    
    def _extractEmail(self, str):
        s = re.search(r"<(.*)>", str)
        if s:
            return s.group(1)
        else:
            return str
        
        
    def getSenderAddress(self):
        return self._extractEmail(self.msg["from"])
    
    def getReceiverAddress(self):
        return self._extractEmail(self.msg["to"])
        
    def getSubject(self):
        return self._decodeHeader(self.msg['subject'])
 
         
    def getText(self):
        for part in self.msg.walk():
            contenttype = part.get_content_type()
            if contenttype == 'text/plain':
                # get content  
                text = self._decode(part.get_payload())  # encoded
   
    def getAttachFileString(self):
        for part in self.msg.walk():
            contenttype = part.get_content_type()
            filename = part.get_filename()
            if filename and contenttype == 'application/octet-stream':   
                return self._decode(part.get_payload()) # encoded
    
    
class PostAgent:
    """
       One MailBox may have several post agents to manage different email account 
    """
    def __init__(self, name, username, password, smtp=None, pop=None):
        self.name = name # the agent name for identify
        self.username = username  # username on email server
        self.password = password  # password on email server
        self.smtp = smtp  # smtp 
        self.pop = pop   # pop
    
    @property    
    def postfix(self):
        return self.smtp.split(".")[-1]
    
    @property
    def domain(self):
        return '.'.join(self.smtp.split('.')[-2:])
        
    @property
    def smtpHost(self):return self.smtp
    
    @property
    def popHost(self):return self.pop

    def addSMTP(self, smtp):
        self.smtp = smtp
        
    def addPOP(self, pop):
        self.pop = pop
    
    def sendMail(self, mail):
        try:
            stp = smtplib.SMTP()
            stp.connect(self.smtp)
            stp.login(self.username, self.password)
            stp.sendmail(mail.getSenderAddress(),mail.getReceiverAddress(), mail.asString())
            stp.quit()
            stp.close()
            return True
        except Exception, e:
            print str(e)
            return False
    
    def _connectPop(self, username, password):    
        pop_conn = poplib.POP3_SSL(self.pop) 
        pop_conn.user(username) 
        pop_conn.pass_(password)
        return pop_conn
     
    def receiveAll(self, username, password): 
        conn = self._connectPop(username, password)
        
        #Get messages from server: 
        messages = [conn.retr(i) for i in range(1, len(conn.list()[1]) + 1)]
        
        # Concat message pieces: 
        messages = ["\n".join(mssg[1]) for mssg in messages]
        
        #Parse message into an email object:
        ps = parser.Parser()
        messages = [ps.parsestr(mssg) for mssg in messages]
        conn.quit()
        return messages
    
    @property  
    def mails(self):
        return _MailIterator(self._connectPop(self.username, self.password))
    

class _MailIterator:
        def __init__(self, popconn):
            self.popconn = popconn
            self.index = 1
            
        def __iter__(self):
            return self
        
        def next(self):
            print "%s/" % self.index, len(self.popconn.list()[1])
            total = len(self.popconn.list()[1])
            if self.index < total +1:
                msg = self.popconn.retr(total - self.index + 1 ) #Result is in form (response, ['line', ...], octets).
                msgObj = email.message_from_string("\n".join(msg[1]))
                mail = Mail()
                mail.fromMsg(msgObj)
                self.index += 1
                return mail    
            else:
                raise StopIteration
                
       
class Mailbox:
    """
      To send email, each person should have a mail box first, people write their mails,
      save in the mail box, the agents will send them out by their address
    """
    def __init__(self, name, username=None, password=None, smtp=None, pop=None, **kargs):
        agents = {}
        self.postAgent = PostAgent(name, username=username, password=password
                                 , smtp=smtp, pop=pop)
        # Initial agent is default
        self.defaultAgent = self.postAgent or None
        agents[self.postAgent.domain] = self.postAgent
        
        
    def addAgent(self, username, password, smtp, pop):
        newAgent = postAgent(username, password, smtp, pop)
        agents[newAgent.domain] = newAgent
        if self.defaultAgent is None:
            self.defaultAgent = newAgent
    
    def switchAgent(domain):
        """
           Switch defalut agent to by mail server domain,eg:
           
        """
        agent = self.agents.get(domain)
        if agent is None:
            raise KeyError("No this agent for your give domain %s" % domain)
        
   
    def sendMail(self, to, subject, content, attachFile=None):
        mail = Mail()
        fromAddr = self.defaultAgent.username + "@" + self.defaultAgent.domain
        print "Send by agent '%s'" % self.defaultAgent.name
        mail.fill(fromAddr, to, subject, content, attachFile)
        self.defaultAgent.sendMail(mail)
    
    @property 
    def mails(self):
        return self.defaultAgent.mails
      
  