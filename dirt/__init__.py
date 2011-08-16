import os
import couchdb
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from dirt.resources import Root

here = os.path.dirname(os.path.abspath(__file__))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application."""
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    db_server = couchdb.client.Server(settings['couchdb_uri'])
    config.registry.settings['db_server'] = db_server
    config.add_static_view('static', 'dirt:static')

    # html views
    config.add_route('index', '/')
    config.add_route('task_new', '/task_new')
    config.add_route('record_new', '/record_new')
    config.add_route('record', '/record/{record_id}')
    config.add_route('task', '/task/{task_name}')
    config.add_route('couch', '/couch')

    # xmlrpc views
    config.add_route('add_record', '/add_record')
    config.add_route('checkout_task', '/checkout_task')
    config.add_route('checkin_task', '/checkin_task')

    config.scan()

    return config.make_wsgi_app()

