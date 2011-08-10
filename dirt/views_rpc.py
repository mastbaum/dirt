import os
import sqlite3
from pyramid.view import view_config
from pyramid_xmlrpc import xmlrpc_view

here = os.path.dirname(os.path.abspath(__file__))
settings = {}
settings['db'] = os.path.join(here, 'dirt.db')

@view_config(name='login')
def login(hostname, password):
    db = sqlite3.connect(settings['db'])
    rs = db.execute("select id, hostname, password, enabled from slave where hostname = ? and password = ?", (hostname, password))
    slaves = [dict(id=row[0], hostname=row[1], password=row[2], enabled=row[3]) for row in rs.fetchall()]
    db.close()
    if len(slaves) == 0:
        return [0, 'dude', 'sweet', 'True'] # slaves[0]
    else:
        return None #None # throw exception

@view_config(route_name='add_record')
@xmlrpc_view
def add_record(context, hostname, password, record_id, description, tasknames):
    slave = login(hostname, password)
    db = sqlite3.connect(settings['db'])
    if not slave:
        return 'no' #False # throw exception

    db.execute('insert into record (number, description, uuid) values (?, ?, ?)',
                       [record_id, description, record_id])

    rs = db.execute('select max(id) from record')
    record_id = rs.fetchall()[0][0]
    db.commit()
    db.close()
    return record_id

@view_config(name='checkout_task')
@xmlrpc_view
def checkout_task(context, hostname, password, task_type, platform):
    slave = login(hostname, password)

@view_config(name='checkin_task')
@xmlrpc_view
def checkin_task(context, hostname, password, revnumber, taskname, success, results):
    slave = login(hostname, password)

@view_config(name='testt')
@xmlrpc_view
def testt(context, name):
    db = sqlite3.connect(settings['db'])
    return name
    db.close()

