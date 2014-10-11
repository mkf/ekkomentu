#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(u'Hello worldowy świecie!')


app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
