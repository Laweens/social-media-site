from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
from pprint import pprint as print 
import flask_login

app = Flask(__name__)
app.secret_key = "thisisjustthesecretkey"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class user:
    is_authenticated = True 
    is_anonymous = False
    is_active = True
    def __init__(self, id, username):
        self.id = id 
        self.username = username 
    def get_id(self):
        return str(self.id)


connect = pymysql.connect(
    database = 'lfrancois_LCA',
    user = 'lfrancois',
    password = '231566837',
    host = '10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')

def index():
    if flask_login.current_user.is_authenticated:
            return redirect ('/feed')
    return render_template('home.html.jinja')

@app.route('/register',methods=['GET','POST'])

def register():
    if flask_login.current_user.is_authenticated:
            return redirect ('/feed')
    if request.method == 'POST':
        username = request.form['username']
        birthday = request.form['birthday']
        password = request.form['password']
        cursor = connect.cursor()
        cursor.execute(f"INSERT INTO `user` (`username`, `password`, `birthday`) VALUES ('{username}', '{password}', '{birthday}')")
        connect.commit()
        cursor.close()

    redirect('/Signin')
    return render_template('register.html.jinja')

@app.route('/Signin', methods=['GET', 'POST'])
def Signin():
     if flask_login.current_user.is_authenticated:
            return redirect ('/feed')
     
     if request.method == 'POST':
         username = request.form['username']
         password = request.form['password']
         cursor = connect.cursor()
         cursor.execute(f"SELECT * FROM `user` WHERE username='{username}'")
         result = cursor.fetchone()
         if request.form ['password'] == result['password']:
            user = load_user(result['ID'])
            flask_login.login_user(user)
            return redirect(url_for('feed'))
         else:
             return "Invalid username or password. Please try again."

     return render_template('Signin.html.jinja')
 
     
@app.route('/feed')
@flask_login.login_required
def feed():
      return flask_login.current_user
   


@login_manager.user_loader
def load_user(user_id):
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM `user` WHERE id =' + str(user_id))
    result = cursor.fetchone()
    connect.commit()
    cursor.close()

    if result is None:
        return None 
    
    return user(result["ID"], result["username"])

