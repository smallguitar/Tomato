# import yaml
# class PuppetReport(yaml.YAMLObject):
#     
#     yaml_tag = u'!ruby/object:Puppet::Transaction::Report'
#     
#     def __init__(self, data):
#         
# 
#      
#         self.host = data['host']
#         
#         print self.host
#         self.logs = PuppetLog(data["logs"])
#         self.metrics = PuppetMetrics(data["metrics"])
#         self.time = data["time"]
#         self.external_times = ruby_sym(data["external_times"])
#         self.resource_statuses = PuppetResourceStatus(data["resource_statuses"])
#     def __repr__(self):
#         return "(host=%r, logs=%r, metrics=%r, time=%r)" % (self.host,self.logs, self.metrics, self.time)
# class ruby_sym(yaml.YAMLObject):
#     yaml_tag = u'!ruby/sym'
#     def __init__(self):
#         self.attr = attr
#         def __repr__(self):
#             return "(attr=%r)" % (self.attr)
# class PuppetLog(yaml.YAMLObject):
#     yaml_tag = u'!ruby/object:Puppet::Util::Log'
#     def __init__(self, log):
#         self.source = log["source"]
#         self.message = log["message"]
#         self.tags = log["tags"]
#         self.time = log["time"]
#     def __repr__(self):
#         return "(source=%r, message=%r, tags=%r, time=%r)" % (self.source,
#                                                               self.message, self.tags, self.time)
# 
# class PuppetMetrics(yaml.YAMLObject):
#     def __init__(self, metric):
#         self.time = submetric(metric["time"])
#         self.resources = submetric(metric["resource"])
#         self.changes = submetric(metric["changes"])
#         self.events = submetric(metric["events"])
#     def __repr__(self):
#         
#         return "(time=%r, resource=%r, changes=%r, events=%r)" % (self.time, self.resource, self.changes, self.events)
# 
# class submetric(yaml.YAMLObject):
#     yaml_tag = u'!ruby/object:Puppet::Util::Metric'
#     def __init__(self, submetric):
#         self.label = submetric["label"]
#         self.name = submetric["name"]
#         self.values = submetric["values"]
#     def __repr__(self):
#         return "(label=%r, name=%r, values=%r)" % (self.label, self.name,
#                                                    self.values)
# class PuppetResourceStatus(yaml.YAMLObject):
#     yaml_tag = u'!ruby/object:Puppet::Resource::Status'
#     def __init__(self, resource_status):
#         self.evaluation_time = resource_status["evaluation_time"]
#         self.events = resource_status["events"]
#         self.file = resource_status["file"]
#         self.line = resource_status["line"]
#         self.resource = resource_status["resource"]
#         self.source_description = resource_status["source_description"]
#         self.tags = resource_status["tags"]
#         self.time = resource_status["time"]
#         self.version = resource_status["version"]
#     def __repr__(self):
#         return "(evaluation=%r, events=%r, file=%r, line=%r, resource=%r,source_description=%r, tags=%r, time=%r, version=%r)" %(self.evaluation, self.events, self.file, self.line, self.resource,self.source_description, self.tags, self.time, self.version)

#unicode=utf8
'''
Created on Feb 25, 2016

@author: root
'''
import yaml
import init_db as initdb
from pydal import DAL as dal
import MySQLdb


def construct_ruby_object(loader, suffix, node):
    return loader.construct_yaml_map(node)

def construct_ruby_sym(loader, node):
    return loader.construct_yaml_str(node)

@service.jsonrpc
def parase_yaml():

    yaml.add_multi_constructor(u"!ruby/object:", construct_ruby_object)
    yaml.add_constructor(u"!ruby/sym", construct_ruby_sym)
    
    stream = file('/home/201602250326.yaml','r')
    mydata = yaml.load(stream)

    return mydata
  
@service.jsonrpc
def insert_data():
    tables = []
    db = MySQLdb.connect("127.0.0.1","root","root","asimp")
    cursor = db.cursor()
    cursor.execute("show tables;")
    datas = cursor.fetchall()
    for data in list(datas):
        tables.append(list(data))
    return tables



def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


