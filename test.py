import time
from pydal import DAL as dal
from pydal import Field
import sqlite3

asimp_db = dal("sqlite://storage.db",auto_import=True)
# node_status = asimp_db.define_table('node_status', \
#         Field(fieldname = 'id', unique = True, type = 'string'), 
#         Field(fieldname = 'node_ip', type = 'string'), 
#         Field(fieldname = 'node_name', type = 'string'), 
#         Field(fieldname = 'status', type = 'string'),
#         Field(fieldname = 'master_ip', type = 'string'), 
#         Field(fieldname = 'master_name', type = 'string'),
#         )
print asimp_db.tables()
# from gluon import DAL
# from gluon import Field

# asimp_db = DAL(uri = "mysql://root:root@127.0.0.1/asimp",migrate=True,fake_migrate=True,check_reserved=['mysql'],do_connect=False,lazy_tables = True)
# print asimp_db._dbname
# print asimp_db._uri
# print asimp_db.tables()
# node_status = asimp_db.define_table('dddd13', \
#     Field(fieldname = 'id', unique = True, type = 'string'), 
#     Field(fieldname = 'node_ip', type = 'string'), 
#       
# )
#  
#   
# asimp_db.commit()

# print asimp_db.ccccc.insert(node_ip='1111111111')

# print asimp_db.tables()
# 
# #  
# 
# 
# import MySQLdb
# db = MySQLdb.connect("127.0.0.1","root","root","asimp")
# cursor = db.cursor()
# cursor.execute("show tables;")
# datas = cursor.fetchall()
# print '\n\n',datas[0][0]
# for data in datas:
#     print "Database version : %s " % data
# db.close()