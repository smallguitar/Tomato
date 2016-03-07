# db.define_table('company',Field('name'),Field('info'))
# db.define_table('employee',Field('employer',db.company),Field('name'),Field('info'))
# db.define_table('employee3',Field('employer'),Field('name'),Field('info'))
# db.define_table('softwarestatus', Field('id'), Field('software_name'))
 
db.define_table('hostinfo', 
    Field( 'id',unique = True), 
    Field( 'host_ip' ), 
    Field( 'host_name' ), 
    Field( 'host_group_name' ),
    Field( 'total_memory' ), 
    Field( 'used_memory' ), 
    Field( 'cpu' ),
)

db.define_table('appinfo', 
    Field( 'id',unique = True), 
    Field( 'app_name' ),
    Field( 'app_group_name' ),
    Field( 'latest_version' ), 
    Field( 'history_version' ), 
)

db.define_table('relationshipinfo', 
    Field( 'id',unique = True), 
    Field( 'host_name' ),
    Field( 'app_name' ), 
    Field( 'action_status' ), 
    Field( 'current_version' ), 
    Field( 'next_relation_ip' ), 
)

db.define_table('loginfo', 
    Field( 'id',unique = True), 
    Field( 'host_name' ),
    Field( 'action_name' ), 
)