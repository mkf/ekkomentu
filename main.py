#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
	def get(self):
		
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))
		self.response.write(u'Hello worldowy świecie!')


app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
