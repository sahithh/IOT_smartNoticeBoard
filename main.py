from flask import Flask, flash, redirect, render_template, request, session, abort
from passlib.hash import sha256_crypt
import mysql.connector as mariadb
import os
import lcddriver
import display
import time
import qr
app = Flask(__name__)
mariadb_connection = mariadb.connect(user="root", password="12345678", host="localhost", database="login")
queue = []
flag=True
obj=display.msgdisplay()
#Opening login page and redirecting to welcome page after successful authentication   
@app.route('/')
def home():
    
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')
  

#Authentication
@app.route('/login', methods=['POST'])
def do_admin_login():
  login = request.form

  userName = login['username']
  password = login['password']
  
  cur=mariadb_connection.cursor()
  cur.execute("SELECT username,password FROM Login WHERE username='{}'".format(userName))
  rows=cur.fetchone()

  
  if sha256_crypt.verify(password, rows[1]):
      account = True
  else:
      account = False
  if account:
    session['logged_in'] = True
    
  else:
      flash("invalid credentials")
  return home()
#Sending message that have to be displayed on LCD screen
@app.route('/lcdmsg' , methods=['POST'])
def send():
    global flag
    flag=False
    data=request.form
    msg=data['msg']
    queue.append(msg)
    global obj
    obj.append(msg)
    flash("message received successful")
    if len(queue)==1:
        while True:
            obj.display()
    return home()
#Editing of message
@app.route('/edit',methods = ['POST','GET'])
def edit():
    result=[]
    result.append(len(queue))
    for i in queue:
        result.append(i)
    return render_template('edit.html',result=result)
#Deleting the selected message by user
@app.route('/delete',methods = ['POST','GET'])
def delete():
    q= request.form.getlist('msg')
    for i in q:
        queue.remove(i)
    obj.delete(q)
    return edit()
#Logging out
@app.route('/logout')
def logout():
  session['logged_in'] = False
  return home()

     
if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='0.0.0.0', port=8080)
