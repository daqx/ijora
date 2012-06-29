# -*- coding: utf-8 -*-
import cgi
import datetime
import urllib
import webapp2
from google.appengine.ext import db

class Greeting(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)


class Region(db.Model):
    name = db.StringProperty()
    city = db.ReferenceProperty()
    
    def __repr__(self):
        return unicode(self.name)
    

class Town(db.Model):
    name    = db.StringProperty()
    region  = db.ReferenceProperty(Region)
    type_name = db.StringProperty(choices=set([u"г.", u"район", u"с."]))
    

class Account(db.Model):
    """A user's account."""
    email = db.EmailProperty(required=True)
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    oauth_token = db.StringProperty()

    @property
    def name(self):
        return u'%s %s' % (self.first_name, self.last_name)

    def __unicode__(self):
       return self.name