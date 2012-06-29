# -*- coding: utf-8 -*-
import webapp2
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from models import *
from config import *
from forms import *
from google.appengine.api import users
import forms


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))

def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


def user_required(handler):
    """
         Decorator for checking if there's a user associated with the current session.
         Will also fail if there's no session present.
     """

    def check_login(self, *args, **kwargs):
        auth = self.auth
        if not auth.get_user_by_session():
            # If handler has no login_url specified invoke a 403 error
            try:
                self.redirect(self.auth_config['login_url'], abort=True)
            except (AttributeError, KeyError), e:
                self.abort(403)
        else:
            return handler(self, *args, **kwargs)

    return check_login

class MainPage(BaseHandler):
    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Greeting.all().ancestor(
            guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        #template = jinja_environment.get_template('index.html')
        self.render_template('index.html', template_values)


class RegionList(webapp2.RequestHandler):
    
    def get(self):        
        regions = Region.all()
        #regions = []
        add_url = 'add'
        template_values = {
            'regions': regions,            
            'url_linktext': add_url,
        }

        template = jinja_environment.get_template('region_list.html')
        self.response.write(template.render(template_values))
        
class RegionForm(webapp2.RequestHandler):
    
    def get(self):        
        form = forms.RegionForm()
        template = jinja_environment.get_template('region_form.html')
        self.response.out.write(template.render({'form':form}))
    
    def post(self):
        r = Region()
        r.name = self.request.POST.get('name')
        r.put()
        self.redirect('/admin/regions')

class EditRegion(BaseHandler):
    
    def get(self, region_id , act = ''):        
        if act == 'delete':
            iden = int(region_id)
            region = db.get(db.Key.from_path('Region', iden))
            db.delete(region)
            self.redirect('/admin/regions')
        else:        
            form = forms.RegionForm()
            iden = int(region_id)
            region = db.get(db.Key.from_path('Region', iden))
            form.name.data = region.name        
            form.city.data = region.city
            
            values_ = {'form':form,'action': self.request.url,'region':region, 'del_url':''}        
            self.render_template('region_form.html', values_)
    
    def post(self, region_id, act = ''):
        iden = int(region_id)
        r = db.get(db.Key.from_path('Region', iden))
        r.name = self.request.POST.get('name')
        #r.city = self.request.POST.get('city')
        city = db.get(db.Key.from_path('Town',int(self.request.POST.get('city'))))
        r.city = city
        r.put()
        self.redirect('/admin/regions')


class TownList(BaseHandler):
    
    def get(self):        
        towns = Town.all()
        #regions = []
        add_url = 'add'
        template_values = {
            'towns': towns,            
            'url_linktext': add_url,
        }

        template = jinja_environment.get_template('town_list.html')
        self.render_template('town_list.html',template_values)
        
class TownForm(BaseHandler):
    
    def get(self):        
        form = forms.TownForm()
        
        self.render_template('town_form.html',{'form':form})
    
    def post(self):
        r = Town()
        r.name = self.request.POST.get('name')
        r.type_name = self.request.POST.get('type_name')
        try:
            reg = db.get(self.request.POST.get('region'))
            r.region = reg
        except Exception, e:
            pass
        r.put()
        self.redirect('/admin/towns')


class EditTown(BaseHandler):
    
    def get(self, town_id , act = ''):        
        if act == 'delete':
            iden = int(town_id)
            town = db.get(db.Key.from_path('Town', iden))
            db.delete(town)
            self.redirect('/admin/towns')
        else:        
            form = forms.TownForm()
            iden = int(town_id)
            town = db.get(db.Key.from_path('Town', iden))
            form.name.data = town.name        
            form.region.data = town.region
            form.type_name.data = town.type_name
            values_ = {'form':form,'action': self.request.url,'town':town, 'del_url':''}        
            self.render_template('town_form.html', values_)
    
    def post(self, town_id, act = ''):
        iden = int(town_id)
        r = db.get(db.Key.from_path('Town', iden))
        r.name = self.request.POST.get('name')
        r.type_name = self.request.POST.get('type_name')
        reg = db.get(self.request.POST.get('region'))
        r.region = reg
        r.put()
        self.redirect('/admin/towns')

class DeleteTown(BaseHandler):
    
    def get(self, id_):        
        form = forms.TownForm()
        iden = int(id_)
        town = db.get(db.Key.from_path('Town', iden))
        db.delete(town)
        self.redirect('/admin/towns')

class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
