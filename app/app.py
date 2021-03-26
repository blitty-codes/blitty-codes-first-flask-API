'''
  Source: https://flask.palletsprojects.com/en/1.1.x/quickstart/
'''

from flask import Flask, request, jsonify, url_for, render_template, make_response, redirect, abort, session
from markupsafe import escape
from werkzeug.utils import secure_filename

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

@app.route('/text/')
def text():
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

##### Rendering templates
@app.route('/hello/')
@app.route('/hello/<string:name>')
def hello(name = None):
  return render_template('hello.html', name=name)

##### Request Object
@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  if request.method == 'POST':
    if valid_login(request.form['username'], request.form['password']):
      return hello(request.form['username'])
    else:
      error = 'Invalid username/password'

  # If the method is not POST, then is GET so we will render de login page
  return render_template('login.html', error=error)

def valid_login(username, password):
  return username == 'Blitty' and password == 'UwU^27'

##### File Uploads
# make sure you have 'enctype="multipart/form-data"' in the HTML form
# Uploaded files are stored in memory or at a temporary location on the filesystem.
# (https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/#uploading-files)
@app.route('/upload_img', methods=['GET', 'POST'])
def upload_img():
  if request.method == 'POST':
    img = request.files['image']
    if valid_extension(img.filename):
      # if you want to store the image in the server use:
      #   from werkzeug.utils import secure_filename
      #   img.save('/var/www/uploads/' + secure_filename(f.filename))
      # using secure_filename prevents you from malicioues inputs.
      # (https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.utils.secure_filename)
      img.save('./' + secure_filename(img.filename))
  
  return render_template('upload_file.html')

def valid_extension(filename):
  # verify the file has a . and next, the file has the extension .png,
  # for that we use rsplit(), which the second parameter help us to just
  # split the string in X peaces
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in { 'png' }

##### Cookies
# use cookies as:
#   - .get(key)
#   - .set(key, value)
@app.route('/cookie4u')
def cookie4u():
  name = 'Blitty'
  resp = make_response(render_template('hello.html'))
  resp.set_cookie('nname', name)
  # print(resp.get_cookie('nname'))

  return resp

@app.route('/give_me_cookie')
def give_me_cookie():
  name = request.cookies.get('nname')
  return render_template('hello.html', name=name)

##### REDIRECTS AND ERRORS
@app.route('/be_a_color', methods=['GET', 'POST'])
def be_a_color():
  if request.method == 'POST':
    if request.form['color'] == '#ffffff':
      abort(406)
    
    if request.form['color'] != None:
      color = request.form['color'][1:]
      print(color)
      print(url_for('color', color_name=color))
      return redirect(url_for('color', color_name=color))
    else:
      abort(418, description='You are a teapot')

  return render_template('cp/color_picker.html')

@app.route('/color/<string:color_name>')
def color(color_name):
  return render_template('cp/color.html', color=color_name)

# instead of using default status codes pages, we can customize them and use them
# (https://flask.palletsprojects.com/en/1.1.x/errorhandling/#error-handlers)
@app.errorhandler(406)
def white_color_not_allowed(error):
  return render_template('cp/not_allowed.html'), 406 # the 406 here tells flask the status code of that page

# url_for() you can use this, to get the current path to
# a url, it is good, because you don't have to keep typing

##### APIs with JSON
@app.route('/about_me')
def about_me():
  return {
    'name': 'Blitty',
    'shortcut': 'B',
    'description': 'Just follow me on twitter @blit12_'
  }

##### Sessions
# It is build in top of cookies and they can be seen, but not modify because you need the secret key
# use this python -c 'import os; print(os.urandom(16))' to create random key
app.secret_key = b'asdfiuq0r72o34r_"ff\xec' # octets

@app.route('/candie')
def candie():
  if 'candie' in session:
    return 'Logged as candie: %s' % escape(session['candie'])
  return f'''
    <h1>You have no candie :(</h1>
    <p>Go to <a href="http://localhost:5000/{url_for('get_candie')}">{url_for('get_candie')}</a></p> '''

@app.route('/get_candie', methods=['GET', 'POST'])
def get_candie():
    if request.method == 'POST':
        session['candie'] = request.form['candie']
        return redirect(url_for('candie'))
    return '''
        <form method="post">
            <p><input type=text name=candie></p>
            <p><input type=submit value=Login></p>
        </form>
    '''
@app.route('/candie_out')
def candie_out():
  candie = session['candie']
  session.pop('candie', None)
  return redirect(url_for('chao', candieName=candie))

@app.route('/chao/<string:candieName>')
def chao(candieName):
  return f'''<h1>See you later {candieName}!</h1>'''

with app.test_request_context():
  print(url_for('login'))
  print(url_for('hello'))
  print(url_for('show_PI', PInum=3.1415167, next='/')) 
  print(url_for('show_user', userName='John Doe'))

# this is used for testing. This one tests if the url '/hello/
# can be used with the method POST, if not it gives a console error (assertion)
with app.test_request_context('/hello/', method='POST'):
  assert request.path == '/hello/'
  assert request.method == 'POST'

if __name__ == '__main__':
  app.run(debug=False)
