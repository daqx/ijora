# -*- coding: utf-8 -*-
'''
Created on 21.06.2012

@author: D_Unusov
'''
#from google.appengine.ext.db import djangoforms
from wtforms.ext.appengine.db import model_form
from models import *

RegionForm = model_form(Region)
    