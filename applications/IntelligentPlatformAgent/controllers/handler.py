#unicode=utf8

import sys,os
 
masterpath = os.path.join(os.getcwd(),r'applications\IntelligentPlatformMaster\controllers')
sys.path.append(masterpath)
 
from common import *

def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)
    

@service.jsonrpc2
def run_command(commandList):
    ret = execute_command(commandList)    
    return  ret
    
def call():
    return service()