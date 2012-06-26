# -*- coding: utf-8 -*-
'''
Created on 21.06.2012

@author: D_Unusov
'''
#from google.appengine.ext.db import djangoforms
from wtforms.ext.appengine.db import Form, model_form
from wtforms import *
from models import *

class RegionForm(Form):
    
    name    = TextField(u'Full Name', [validators.required(), validators.length(max=20)])
    _type_list = [] 
    for type in Town.all(): 
        _type_list.append((type.key().id(),type.name)) 
    city = SelectField(u'Type of entry', choices =_type_list, coerce=int) 
    
TownForm = model_form(Town)
    