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
			<div><input value="%s" name="adressub"><br>
				<input type="radi </div>
			<div><input type="submit" value="Postuj"></div>
		</form>
		<hr><br>
		<form>Adres komentowanej strony:
			<input value="%s" name="adres"><br>Wyświetlanie:
			<input type="radio" name="jakshow" value="dokladnie">Dokładnie<br>
			<input type="radio" name="jakshow" value="narrowed">Uwzględniając mniej precyzyjne komentarze<br>
			<input type="checkbox" name="jakshowstend" value="widerly">Wszystko zaczynające się od<br>
			<input type="checkbox" name="jakshowstend" value="widerlysta">Wszystko kończące się na<br>
			<input type="submit" value="switch">
		</form>
		<a href="%s">%s</a>
	</body>
</html>
"""



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
