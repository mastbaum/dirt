import os
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from dirt.resources import Root

here = os.path.dirname(os.path.abspath(__file__))

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')
    settings['db'] = os.path.join(here, 'dirt.db')
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    config.add_static_view('static', 'dirt:static')
    config.add_route('index', '/')
    config.add_route('task_new', '/task_new')
    config.add_route('record_new', '/record_new')
    config.add_route('record', '/record/{record_id}')
    config.add_route('task', '/task/{task_name}')

    config.scan()

    return config.make_wsgi_app()

