import os
_basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TESTING = True

#SECRET_KEY = 'SecretKeyForSessionSigning'

THREADS_PER_PAGE = 8

CSRF_ENABLED=True
CSRF_SESSION_KEY="somethingimpossibletoguess"