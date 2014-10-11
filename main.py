#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import webapp2
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

GLOWNA = """\
	<form action="/com?%s" method="post">
		<div><textarea name="tresc" rows="4" cols="60"></textarea></div>
		<div><input type="submit" value="Postuj"></div>
	</form>
	<hr>
	<form>Obiekt komentu:
		<input value="%s"

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
