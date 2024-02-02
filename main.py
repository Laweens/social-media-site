from flask import Flask, render_template, request, redirect 
import pymysql
import pymysql.cursors
from pprint import pprint as print 

app = Flask(__name__)


connect = pymysql.connect(
    database = 'lfrancois_LCA',
    user = 'lfrancois',
    password = '231566837',
    host = '10.100.33.60',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')

def index():
    return render_template('home.html.jinja')

@app.route('/register',methods=['GET','POST'])

def register():
    if request.method == 'POST':
        username = request.form['username']
        bday= request.form['bday']
        password= request.form['password']
        cursor = connect.cursor()
        cursor.execute(f"INSERT INTO `user` (`username`, `password`, `birthday`) VALUES ('{username}', '{password}', '{bday}')")
        connect.commit()
        cursor.close()
        
    
    return render_template('register.html.jinja')
