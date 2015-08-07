import urllib2
from contextlib import contextmanager

@contextmanager
def proxy(*proxyServers):
    proxyServerDict = dict(server.split("://") for server in proxyServers)
    try:
        setProxy(proxyServerDict)
        yield
    finally:
        setProxy(None)
            
                
def setProxy(proxyServerDict):
    """ for example
       proxyServerDict = {'http': '127.0.0.1:8087,
                          'https': '127.0.0.1:8087' 
                          }
    """
    if proxyServerDict == None:
         null_proxy_handler = urllib2.ProxyHandler({})
         opener = urllib2.build_opener(null_proxy_handler)
    else:
        if isinstance(proxyServerDict, dict):
             proxy_handler = urllib2.ProxyHandler(proxyServerDict)
             opener = urllib2.build_opener(proxy_handler)
        else:
             raise TypeError("Should be given in dict format:\n%s" % setProxy.__doc__)
    
    urllib2.install_opener(opener)