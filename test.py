from flask import Flask, redirect, url_for, request, render_template
from flask_socketio import SocketIO, send, emit


app = Flask("PyMessageChat")

# Main route
@app.route('/')
def hello_world():
   return 'Main World'

# 
@app.route('/2')
def index():
   return ("<html><body><h1>Hell</h1><h2>o</h2> <h1>World</h1></body></html>")

# hardcoded
@app.route('/hard/')
def hard():
   return render_template('test/hard.html')
   
  
# score pass >50
@app.route('/score/<int:score>')
def score_value(score):
   return render_template('test/score.html', marks = score)


# dict result
@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('test/result.html', result = dict)


# str
@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name
  
   
# int in url
@app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID


# float in url
@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo
   
   
# Redirect used url_for to build dynamic urls
@app.route('/admin')
def hello_admin():
   return 'Hello Admin'


@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name))
      

# logging
# use html
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))
     
 

if __name__ == '__main__':
   app.run(debug = True)



