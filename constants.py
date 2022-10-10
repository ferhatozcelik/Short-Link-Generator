import os

API_KEY = 'Basic FERHATOZCELIK'
APP_SECRET_KEY = 'FERHAT_OZCELIK'
SUCCESS_MESSAGE = 'SUCCESS'
FAILED_MESSAGE = 'FAILED'

DEBUG = True

if DEBUG:
    DATABASE_URL = 'postgresql://root:QhOHVwDDX41cH0lN8vELnfr8WsIUHKIY@dpg-cd21fjsgqg4akcf8gv3g-a.frankfurt-postgres.render.com:5432/shortlink_ipbw'
else:
    DATABASE_URL = os.environ.get('DATABASE_URL')