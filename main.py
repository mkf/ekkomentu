#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import webapp2
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

GLOWNA = """\
		<form action="/comm?%s" method="post">
			<div><textarea name="tresc" rows="4" cols="60"></textarea></div>
			<div><input value="%s" name="adressub"><br>
				<input type="radio" name="jakwys" value="dokladnie">Tylko dla dokładnie tego adresu (jeżeli zawiera jakieś unikalne zmienne, komentarze będą niewidoczne dla innych, przeglądających tą samą treść, dopóki nie wybiorą wyświetlania szerszego filtru)<br>
				<input type="radio" name="jakwys" value="pocz">Wszystkich zaczynających się od<br>
				<input type="radio" name="jakwys" value="konc">Wszystkich kończących się na<br>
				<input type="radio" name="jakwys" value="mid">Wszystkich zawierających<br>
				</div>
			<div><input type="submit" value="Postuj"></div>
		</form>
		<hr><br>
		<form>Adres komentowanej strony:
			<input value="%s" name="adres"><br>Wyświetlanie:
			<input type="radio" name="jakshow" value="dokladnie">Tylko dla dokładnie tego adresu (jeżeli adres zawiera unikalne zmienne, zobaczysz co najwyżej swoje własne komentarze, dopóki nie wybierzesz szerszego filtru)<br>
			<input type="radio" name="jakshow" value="pocz">Wszystkich zaczynających się od<br>
			<input type="radio" name="jakshow" value="konc">Wszystkich kończących się na<br>
			<input type="radio" name="jakshow" value="mid">Wszystkich zawierających<br>
			Porada: Wpisz __world__, aby pisać ogólnie do wszystkich. <br>
			W późniejszym czasie nie będą to wyłącznie komentarze, ale samoodświeżający się czas dotyczący każdej z witryn. <br> 
			Również w późniejszym czasie będzie tak, że będzie widać, dla jakiego adresu publikujesz (tu uwaga: problem bezpieczeństwa, polegający na częstym przechowywaniu kluczy autoryzacyjnych w adresach URL zamiast w ciasteczkach!).<br>
			Jeszcze jednym pomysłem jest wyświetlanie, kto aktualnie przegląda dany wątek komentarzy, i na jakiej szerokości, w tym czy jest mniejsza od Twojej, większa od Twojej, czy taka sama, i jaka jest różnica w URL.<br>
			<input type="submit" value="switch">
		</form>
	</body>
</html>
"""

DEFAULT_COMMENTED_ADDRESS = '__world__'

def commentedaddr_key(commented_addr=DEFAULT_COMMENTED_ADDRESS):
	return ndb.Key('Komentarze', commented_addr)

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	address = ndb.StringProperty()
	content = ndb.TextProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)




class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))
		
		self.response.write('<html><body bgcolor="#68CBFF">')
		commented_addr = self.request.get('commented_addr', DEFAULT_COMMENTED_ADDRESS)
		greetings_query = Greeting.query(ancestor=commentedaddr_key(commented_addr)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)
		
		for greeting in greetings:
			self.response.write('<b>%s</b> wrote:' % greeting.author.nickname())
		
		sign_query_params = urllib.urlencode({'commented_addr': commented_addr})
		self.response.write(GLOWNA % (sign_query_params, cgi.escape(guestbook_name)))
		
class Komentarzowywanie(webapp2.RequestHandler):
	def post(self):
			commented_addr = self.request.get('commented_addr', DEFAULT_COMMENTED_ADDRESS)
			greeting = Greeting(parent=commentedaddr_key(commented_addr))
			greeting.author = users.get_current_user()
			greeting.content = self.request.get('content')
			greeting.put()
			query_params = {'commented_addr': commented_addr}
			self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/sign', Komentarzowywanie),
], debug=True)
