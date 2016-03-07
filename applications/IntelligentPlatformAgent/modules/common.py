# -*- coding: utf-8 -*-
from __future__ import division
import os 
import re
import sys 
import subprocess
import socket
from platform import system
import time
import json
import uuid
import httplib 
import types
import log as logging
import traceback

LOG = logging.getLogger(__name__)

class CmdException(Exception):
    def __init__(self, message=None, **kwargs):
        if message == None:
            message = "Execution of some command failed, check the log please."
        super(CmdException, self).__init__(message)
 
class ParasTypeException(Exception):
    code = -32001
    def __init__(self, message=None, **kwargs):
        if message == None:
            message = "Failed in parsing parameter. Parameter passed must be incorrect."
        super(ParasTypeException, self).__init__(message)
        
def get_ip_by_hostname(hostname):
    pattern = r'\d+\.\d+\.\d+\.\d+'
    
    with open('/etc/hosts') as f:
        lines = f.readlines()
        f.close()
        
    for line in lines:
        ipList = re.findall(pattern, line)
        if  ipList:
            dest_string = line.replace(ipList[0],'').strip().lower()
            if dest_string == hostname.lower():
                return ipList[0]
    return None
    
def execute_command(commandList):
    
    try:
        if system()=='Windows':
            if isinstance(commandList,list):
                command = commandList
            else:
                command = [commandList]
            process_name = uuid.uuid1().__str__()+'.bat'
            f = open(process_name, "w")
            try:
                f.write('%s\n\n'%('\n'.join(command))) 
            finally:
                f.close()
            cmd = process_name
        else:
            if isinstance(commandList,list):
                command = [ '#!/bin/bash',]+commandList
            else:
                command = [ '#!/bin/bash',commandList]
            process_name = '/tmp/'+uuid.uuid1().__str__()+'.sh'
            # open(process_name, 'w').write('%s\n\n'%('\n'.join(command))) 
            f = open(process_name, "w")
            try:
                f.write('%s\n\n'%('\n'.join(command))) 
            finally:
                f.close()
                
            cmd = '/usr/bin/bash '+process_name
        process_shell=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        #Popen.communicate(input=None), return a tuple (stdoutdata, stderrdata) 
        msg = process_shell.communicate()
        print msg[0]
        print msg[1]
        if os.path.exists(process_name):
            os.remove(process_name)
        return msg
    except Exception,e:
        if os.path.exists(process_name):
            os.remove(process_name)
        return str(e)
 
def call_jsonrpc(ip,port,finalUrl,method,params):
    raiseException=True
    rpcPort = port
    headers = {'Content-Type':'application/json'}
    timeout = 10
    def _getRpcBody_(function, parameters):
        body = {}
        body['jsonrpc'] = "2.0"
        body['method'] = function
        body['params'] = parameters
        body['id'] = uuid.uuid1().__str__()
        return json.dumps(body)

    # Send request and receive response
    try:
        socket.setdefaulttimeout(timeout)
        httpclient = httplib.HTTPConnection(ip, rpcPort, timeout)
        param = _getRpcBody_(method, params)
        httpclient.request('POST', finalUrl, param, headers)
        response = httpclient.getresponse()
        resBody = response.read()
        httpclient.close()
    except Exception,e:
        exstr = traceback.format_exc()
        LOG.error('call_jsonrpc failed: %s' % exstr)  
        raise ParasTypeException('call_jsonrpc failed:  %s' % exstr)

    # Convert json string into python object
    resDict = json.loads(resBody)
    if resDict.has_key('result'):
        return resDict['result']
    else:
        if raiseException:
            errormsg = resDict['error']['message']
            raise Exception(errormsg)
        else:
            return
 