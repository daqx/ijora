import setup_env
import urllib
import webapp2

import routes
import config
from error_handlers import handle_404, handle_500

app = webapp2.WSGIApplication(config=config.webapp2_config, debug=True)
routes.add_routes(app)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

#app = webapp2.WSGIApplication([('/', MainPage),
#                               ('/sign', Guestbook)],
#                              debug=True)