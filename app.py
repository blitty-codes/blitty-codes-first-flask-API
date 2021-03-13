'''
  Source: https://flask.palletsprojects.com/en/1.1.x/quickstart/
'''

from flask import Flask, request, jsonify, url_for
from markupsafe import escape

app = Flask(__name__)

# From https://flask.palletsprojects.com/en/1.1.x/quickstart/
# $ flask run --host=0.0.0.0
# This tells your operating system to listen on all public IPs.

# By doing:
#   $ export FLASK_ENV=development
#   $ export FLASK_DEBUG=1
# we don't need to restart the program
# when we make changes.

# MAKE SURE TO HAVE ALL ENVIROMENT VARIABLES UP

# defining an API route
@app.route('/')
def index():
  return 'First API call!!!'

@app.route('/hello/')
def hello():
  return 'YEY'

@app.route('/post', methods=['POST'])
def test_post():
  input_json = request.get_json(force=True)
  json = {
    'Return': input_json['name'],
  }

  return jsonify(json)

# Variable Rules
# Types:
#   string - default (accepts string whitout a slash)
#   int - positive integers
#   float - positive floating point values
#   path - string that accepts slash
#   uuid -accepts UUID strings

@app.route('/user/<userName>')
def show_user(userName):
  return 'User %s' % escape(userName)

@app.route('/hero/<int:hero_id>')
def show_hero(hero_id):
  return f'Hero number: {hero_id}'

@app.route('/goto/<path:subpath>')
def goto(subpath):
  return 'Subpath selected: %s' % escape(subpath)

@app.route('/giveMePI/<float:PInum>')
def show_PI(PInum):
  return 'Is this PI? %f' % PInum

# url_for() you can use this, to get the current path to
# a url, it is good, because you don't have to keep typing

with app.test_request_context():
  print(url_for('index'))
  print(url_for('hello'))
  print(url_for('show_PI', PInum=3.1415167, next='/')) 
  print(url_for('show_user', userName='John Doe'))

##### NEXT:
##### HTTP Methods


if __name__ == '__main__':
  app.run(debug=True)

