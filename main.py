import urllib
import json
import logging

import webapp2

from google.appengine.api import urlfetch
from google.appengine.api import xmpp
from google.appengine.ext import ndb
from google.appengine.ext.webapp import xmpp_handlers

import config

TRANSLATE_BASE_URI = 'https://www.googleapis.com/language/translate/v2'
TRANSLATE_API_PARAMETERS = 'key=%(key)s&target=%(target)s&q=%(q)s&format=text'
HELP_MSG = ("Translate a text by typing '<target> <text>' "
            "E.g 'es Hello Bot!'. To learn more, go to %s")
RESULT_MSG = "%s *_powered by Google translate_*"
RESULT_ERROR_MSG = 'Whoops... something wrong happened. Try again later.'
COMMAND_ERROR_MSG = "Wrong Command '%s'. Type '/help' for more information."

def translate(q, target, source=None):
  """
  Returns text translations from one language to another using Google Translate
  API.
  
  Args:
    q: Text to translate as string.
    target: Translated text (q) target language as string.
    source: Text (q) source language as string.

  Returns:
    Text translation as string. None if an error occurs.
  """
  # Build the RESTful call.
  p = {
    'key': config.TRANSLATE_API_KEY,
    'target': target,
    'q': urllib.quote_plus(q,"'")
  }
  url = TRANSLATE_BASE_URI + '?' + TRANSLATE_API_PARAMETERS % p

  if source:
    url = url + '&source=%s' % source

  try:
    response = urlfetch.fetch(url=url, method=urlfetch.GET)
    if response.status_code == 200:
      # Succesful API call.
      result = json.loads(response.content)
      # TODO: take into account any errors.
      if 'data' in result:
        return result['data']['translations'][0]['translatedText'] 
    else:
      logging.error('query = %s , http_status_code = %s' % (url, response.status_code))
      return None
  except urlfetch.DownloadError:
    # Request timed out or failed.
    logging.error('There was an error translating the text')
    return None


class XMPPHandler(xmpp_handlers.CommandHandler):
  def help_command(self, message=None):
    """Show help text."""
    message.reply(HELP_MSG % self.request.host_url)

  def text_message(self, message=None):
    """Translate Command."""
    # TODO: validate 'target'
    parts = message.body.split(' ',1)
    
    if len(parts) > 1:
      target = parts[0]
      q = parts[1].strip()
      
      translation = translate(q, target)

      logging.debug('to: %s' % message.to)
      logging.debug('from: %s' % message.sender)
      logging.debug("Target: '%s' q: '%s'" % (target, q)) 
      
      if translation:
        logging.debug("Translation: '%s'" % translation)
        message.reply(RESULT_MSG % translation)
      else:
        # Translate function returned None (an error occured)
        logging.debug('Translation failed!')
        message.reply(RESULT_ERROR_MSG)
    else:
      message.reply(COMMAND_ERROR_MSG % message.body)

  def unhandled_command(self, message=None):
    message.reply(COMMAND_ERROR_MSG % message.body)


application = webapp2.WSGIApplication([
  (r'/_ah/xmpp/message/chat/', XMPPHandler),
], debug=True)
