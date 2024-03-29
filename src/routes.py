# -*- coding: utf-8 -*-
from webapp2_extras.routes import RedirectRoute
from handlers import *
import handlers

#from web.handlers import LoginHandler
#from web.handlers import LogoutHandler
#from web.handlers import SecureRequestHandler
#from web.handlers import CreateUserHandler

# Using redirect route instead of simple routes since it supports strict_slash
# Simple route: http://webapp-improved.appspot.com/guide/routing.html#simple-routes
# RedirectRoute: http://webapp-improved.appspot.com/api/webapp2_extras/routes.html#webapp2_extras.routes.RedirectRoute

_routes = [
    RedirectRoute('/', MainPage),    
    RedirectRoute('/sign', Guestbook),
    RedirectRoute('/admin/regions', RegionList),
    RedirectRoute('/admin/regions/add', handlers.RegionForm),    
    RedirectRoute('/admin/regions/edit/<region_id>', handlers.EditRegion),
    RedirectRoute('/admin/regions/edit/<region_id>/<act>', handlers.EditRegion),
    RedirectRoute('/admin/towns', TownList),
    RedirectRoute('/admin/towns/add', handlers.TownForm),
    RedirectRoute('/admin/towns/edit/<town_id>', handlers.EditTown),
    RedirectRoute('/admin/towns/edit/<town_id>/<act>', handlers.EditTown),
    
    #RedirectRoute('/admin/towns/edit/(\d+)/delete', handlers.EditTown),
    
    #RedirectRoute('/login/', LoginHandler, name='login', strict_slash=True),
    #RedirectRoute('/logout/', LogoutHandler, name='logout', strict_slash=True),
    #RedirectRoute('/secure/', SecureRequestHandler, name='secure', strict_slash=True),
    #RedirectRoute('/', CreateUserHandler, name='create-user', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    for r in _routes:
        app.router.add(r)