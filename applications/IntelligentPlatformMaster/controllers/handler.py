#unicode=utf8
import os ,sys
import copy
import traceback
import socket
 
masterpath = os.path.join(os.getcwd(),r'applications\IntelligentPlatformMaster\controllers')
sys.path.append(masterpath)
from common import *
import log as logging

LOG = logging.getLogger(__name__)

def index():
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))

def user():
    return dict(form=auth())

@cache.action()
def download():
    return response.download(request, db)
    
@service.jsonrpc2
def app_operate_interface(action,app,version,ip):
    finalUrl="/IntelligentPlatformAgent/handler/call/jsonrpc2"  
    port = '80'
    method = 'run_command'
    params = {'commandList':'puppet agent  --server %s --test --tags %s_%s_%s'%(socket.gethostname(),app,version,action)}
    ret = call_jsonrpc(ip,port,finalUrl,method,params)
    
    if 'call_jsonrpc failed' in str(ret):
        return  'call_jsonrpc failed\n'+str(ret)
        
    if 'Notice: Finished catalog' not in str(ret):
        raise CmdException('Notice: Finished catalog\n'+str(ret))
        
    if action == 'install':
        db.relationshipinfo.insert(
        host_name=ip,
        app_name=app,
        action_status='installing',
        current_version=version,
        next_relation_ip='')
 
    elif action == 'uninstall':
        query = (db.relationshipinfo.host_name==ip) & (db.relationshipinfo.app_name==app)
        james = db(query).select(db.relationshipinfo.ALL)[0]
        james.delete_record()
        
    elif action == 'upgrade':
        query = (db.relationshipinfo.host_name==ip) & (db.relationshipinfo.app_name==app)
        james = db(query).select(db.relationshipinfo.ALL)[0]
        james.update_record(current_version=version)
 
    elif action == 'rollback':
        query = (db.relationshipinfo.host_name==ip) & (db.relationshipinfo.app_name==app)
        james = db(query).select(db.relationshipinfo.ALL)[0]
        james.update_record(current_version=version)
 
    return True
    
@service.jsonrpc2
def get_relation_host(ip,app):
    signature = 'hly'
    finalUrl="/IntelligentPlatformAgent/handler/call/jsonrpc2"  
    port = '80'
    method = 'run_command'
    params = {'commandList':'puppet agent  --server %s --test --tags %s_get'%(socket.gethostname(),app)}
    ret = call_jsonrpc(ip,port,finalUrl,method,params)
    if 'call_jsonrpc failed' in str(ret):
        return  ret
    for line in ret[0].split('\n'):
        if signature in line and 'Notice:' in line  and  '/Stage' not in line and ':' in line :
            ip_list = line.split(':')[2].strip()
            ip_list = ip_list.split(',')
            return  [ip.split(chr(0x1b))[0] for ip in ip_list if len(ip.strip()) > 0]
            
    return  []
    
@service.jsonrpc2
def get_hostlist():
    try:
        hostlist = []
        hostdicts = {'hostname':'', 'ipaddr':''}
        dirs=os.listdir('/var/lib/puppet/ssl/ca/signed')

        for dir in dirs:
            dirname=dir.split('.')[0]
            hostname=socket.gethostname()
            host=hostname.lower()
            hostdicts['hostname'] = dirname
            hostdicts['ipaddr'] = get_ip_by_hostname(dirname)
            if cmp(dirname,host):
                tmp = copy.deepcopy(hostdicts)
                hostlist.append(tmp)
        return hostlist       
    except Exception,e:
        exstr = traceback.format_exc()
        LOG.error('get host list failed: %s' % exstr)  
        raise CmdException('get host list failed:  %s' % exstr)

@service.jsonrpc2
def get_app_list():
    try:
        app_info = {'appname':'app1','version':[],'lastversion':''}
        app_list = []
        try:
            dirs=os.listdir('/etc/puppet/modules')   
            if len(dirs):
                for dir in dirs:
                    version_file = r'/etc/puppet/modules/%s/version.md'%dir
                    if os.path.exists(version_file):
                        fileHandler = open(version_file, 'r')
                        version_stream = fileHandler.readlines()
                        for tmp in version_stream:
                            if '\n' in version_stream:
                                version_stream.remove('\n')
                        if len(version_stream):
                            version_list = []
                            for str in version_stream:
                                if str != '\n':
                                    version_list.append(str.strip())
                            app_info['version'] = version_list
                            app_info['lastversion']= version_stream[-1].strip()
                            app_info['appname'] = dir
                            
                            tmp = copy.deepcopy(app_info)
                            app_list.append(tmp)
            return app_list
        except Exception,e:
            exstr = traceback.format_exc()
            LOG.error('get app version failed: %s' % exstr)  
            raise ParasTypeException('get app version failed:  %s' % exstr)
            
    except Exception,e:
        exstr = traceback.format_exc()
        LOG.error('get host list failed: %s' % exstr)  
        raise CmdException('get host list failed:  %s' % exstr)

@service.jsonrpc2
def get_host_installed_apps(ip):
    try:
        app_list = []
        app_dicts = {'app_name':'', 'app_version':''}
        signature = 'hly'
        finalUrl="/IntelligentPlatformAgent/handler/call/jsonrpc2"  
        port = '80'
        method = 'run_command'
        params = {'commandList':'puppet agent  --server %s --test --tags version'%(socket.gethostname())}
        ret = call_jsonrpc(ip,port,finalUrl,method,params)
        if 'call_jsonrpc failed' in str(ret):
            return  ret
        for line in ret[0].split('\n'):
            if signature in line and 'Notice:' in line  and  '/Stage' not in line and ':' in line :
                app_name = line.split(':')[1].strip()
                app_version = line.split(':')[3].strip()
                app_dicts['app_name'] = app_name
                app_dicts['app_version'] = app_version.split(chr(0x1b))[0]
                tmp =  copy.deepcopy(app_dicts)
                app_list.append(tmp)
        return  app_list
    except Exception,e:
        exstr = traceback.format_exc()
        LOG.error('get host installed app failed: %s' % exstr)  
        raise ParasTypeException('get host installed app failed:  %s' % exstr)
def call():
    return service()
 
