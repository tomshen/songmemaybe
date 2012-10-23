import jinja2
import os
import time
import cgi
import urllib
import webapp2
from pytinysong.request import TinySongRequest
from pytinysong.helper import formattedSearch

from google.appengine.ext import db

# loads framework for HTML templates
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(
	[os.path.dirname(__file__), '/templates']))

# reprsentation of the message in the database
class Message(db.Model):
	id = db.StringProperty()
	sender = db.StringProperty()
	recipient = db.StringProperty()
	message = db.TextProperty()
	songID = db.StringProperty() # SongID for Grooveshark/TinySong API
	URL = db.StringProperty()

	
class LetterSend(webapp2.RequestHandler):
	def get(self):
		message_id = self.request.get("id")
		messages = Message.all();
		messages.filter("id =", message_id)
		for message in messages:
			template_values = {
				'sender': cgi.escape(message.sender),
				'recipient': cgi.escape(message.recipient),
				'message': cgi.escape(message.message),
				'songID': message.songID,
				'URL': message.URL
			}
		template = jinja_environment.get_template('templates/lettersent.html')
		self.response.out.write(template.render(template_values))
			
class LetterStart(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/letterstart.html')
		self.response.out.write(template.render())

# displays the information for a letter (message) based on id # in URL
class LetterPreview(webapp2.RequestHandler):
	def post(self):
		message = Message(id = str(int(time.time()*100)),
			sender = self.request.get('sender'),
			recipient = self.request.get('recipient'),
			message = self.request.get('message'),
			songID = self.request.get('songID'),
			URL = self.request.url[:self.request.url.index('preview')] + 'display?')
		message.URL += urllib.urlencode({'id': message.id})
		message.put()
		template_values = {
			'id': message.id,
			'sender': cgi.escape(message.sender),
			'recipient': cgi.escape(message.recipient),
			'message': cgi.escape(message.message),
			'songID': message.songID,
			'URL': message.URL
		}
		template = jinja_environment.get_template('templates/letterpreview.html')
		self.response.out.write(template.render(template_values))
		
class LetterDisplay(webapp2.RequestHandler):
	def get(self):
		message_id = self.request.get('id')
		messages = Message.all()
		messages.filter("id =", message_id)
		for message in messages:
			template_values = {
				'sender': cgi.escape(message.sender),
				'recipient': cgi.escape(message.recipient),
				'message': cgi.escape(message.message),
				'songID': message.songID,
				'URL': message.URL
			}
		template = jinja_environment.get_template('templates/letterdisplay.html')
		self.response.out.write(template.render(template_values))

class LetterSearch(webapp2.RequestHandler):
	def post(self):
		query = self.request.get('query')
		template = jinja_environment.get_template('templates/search.html')
		self.response.out.write(template.render(query = query, results = formattedSearch(query)))
		
class MainPage(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/index.html')
		self.response.out.write(template.render())

# actually launches the app
app = webapp2.WSGIApplication([('/', MainPage),('/start', LetterStart), ('/send', LetterSend), ('/preview', LetterPreview), ('/search', LetterSearch), ('/display', LetterDisplay)], debug=True)
