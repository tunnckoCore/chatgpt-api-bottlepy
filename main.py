import os
from pychatgpt import Chat
from bottle import debug, request, get, post, run, parse_auth, template

# On dev:
# debug(True)

cached = {}

@get('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@post('/prompt')
def api():
		(username, password) = parse_auth(request.headers.get('Authorization', None))

		OPENAI_USER = os.environ.get('OPENAI_USER')
		OPENAI_PASS = os.environ.get('OPENAI_PASS')

		# Check if the username and password are correct
		if username != OPENAI_USER or password != OPENAI_PASS:
				return {'error': 'Not logged. Please use Authorization header correctly.'}
		else:
				if 'gpt' not in cached:
						cached['gpt'] = Chat(email=username, password=password)
				else:
						print('FROM CACHE')

				return {'data': cached['gpt'].ask(request.json['prompt'])}

# One dev:
# run(reloader=True, host='localhost', port=8080)
run()
