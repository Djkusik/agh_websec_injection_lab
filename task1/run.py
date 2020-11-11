import os
from app import app


FLAG = os.environ.get('MEDIUM_FLAG', 'bit{there_should_be_medium_flag}')
app.run(host='0.0.0.0', debug=True)