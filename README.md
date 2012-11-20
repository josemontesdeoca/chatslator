Chatslator
==========

App Engine XMPP bot to conveniently translate text by sending an IM to a gTalk buddy.

How to use it?
-------------
Add your application contact to your buddy list (E.g your-app-id@appspot.com).

Send text messages to translate content following this convention:

'target text' __E.g:__ 'es Hello world'

Technology used
---------------
- Python 2.7
- [Google App Engine][gae]
 - [XMPP service][xmpp]
 - [XMPP webapp handlers][xmpp_handlers]
- [Google Translate API][translate]

[gae]: http://developers.google.com/appengine
[xmpp]: https://www.googleapis.com/language/translate/v2?key=AIzaSyCA3MAa9V4BBiH4qrKMojPIiCPpblYCnbY&target=es&q=Hello
[xmpp_handlers]: https://developers.google.com/appengine/articles/using_xmpp
[translate]: https://developers.google.com/translate/

Get started
-----------
1. Download the latest App Engine SDK [here](https://developers.google.com/appengine/downloads).
2. Download the code.
3. Visit the [Google APIs Console](https://code.google.com/apis/console/) and create a new project enabling Translate API service.
4. Rename 'config.sample.py' to 'config.py' and add your [API Key](https://developers.google.com/translate/v2/using_rest#auth)
5. Create an [App Engine Application](https://appengine.google.com)
6. Set your 'application' name in app.yaml
7. [Deploy online](https://developers.google.com/appengine/docs/python/tools/uploadinganapp#Uploading_the_App)

Once the application is deployed, your App Engine buddy chat is your-app-id@appspot.com.
