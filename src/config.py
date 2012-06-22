import jinja2
import os

webapp2_config = {}


webapp2_config['webapp2_extras.sessions'] = {
    'secret_key': '5023a964-ea67-4965-b8c1-8b098b87a51a',
}

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'))