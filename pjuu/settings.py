# -*- coding: utf8 -*-

# Pjuu example settings file
# Please change the below for production
# Please make sure all settings have been updated for your
# development environment

# Will show debug information when running in 'manage.py runserver'
DEBUG = True

# Are you testing Pjuu? This will prevent Flask-Mail sending any e-mails and
# will also force Flask-WTF Recaptcha to return True
TESTING = True

# In the case of testing we need a server name, so here's one:
#SERVER_NAME = 'localhost'

# Keep it secret, keep it safe
# Ensure you change this!
SECRET_KEY = 'Development Key'

# Redis settings (this is just the datastore, not sessions)
REDIS_HOST = 'localhost'
REDIS_DB = 0

# Sessions
# Redis settings for sessions
SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_DB = 1

SESSION_COOKIE_HTTPONLY = True
# Ensure this is True in productions
# This will only work if communicating over HTTPS
SESSION_COOKIE_SECURE = False

# Flask-Mail
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = 'Pjuu <noreply@pjuu.com>'

# Flask-WTF (Cross site request forgery)
# CSRF should be off during testing to allow us to submit forms
WTF_CSRF_ENABLED = True
# Change this for extra security
WTF_CSRF_SESSION_KEY = SECRET_KEY

# Recaptcha
# Add in your Recaptcha keys here
RECAPTCHA_USE_SSL = True
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
RECAPTCHA_OPTIONS = {
    'theme': 'white'
}

# Pagination
FEED_ITEMS_PER_PAGE = 25
PROFILE_ITEMS_PER_PAGE = 25

# Signer Keys
# Please see pjuu.auth.backend for details
# You can change the TOKEN_KEY for extra security
TOKEN_KEY = SECRET_KEY
TOKEN_SALT_ACTIVATE = 'ACTIVATE'
TOKEN_SALT_FORGOT = 'FORGOT'
TOKEN_SALT_EMAIL = 'EMAIL'

# Sentry settings
# If you do not add a Sentry DSN you will not receive any logging information
# If you do not run Sentry then you can add a custom logger in see the Flask
# documentation: http://flask.pocoo.org/docs/errorhandling/
SENTRY_DSN = ''