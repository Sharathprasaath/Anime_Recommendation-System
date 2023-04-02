from flask import Flask, request,render_template,redirect,url_for
import mysql.connector
import re
app = Flask(__name__)
l=[]
import pickle
cnx=mysql.connector.connect(user='root', password='sharath123', host='127.0.0.1' , port='3306', database='flask')
cur=cnx.cursor()
cur.execute("select database();")
rec=cur.fetchone()
print("you are connected to databse:",rec)
model=pickle.load(open("model.pkl","rb"))
@app.route("/")
def main():
    return render_template("index.html")
@app.route("/log",methods=["post"])
def log():
    ms = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cur.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cur.fetchone()
        print(username)
        #print(account[0])
        if account:
            return render_template("mainpage.html")
        else:
            ms="invalid username or password!"
    return render_template("index.html",ms=ms)
        
@app.route("/reg", methods=['post'])
def reg():
    msg = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form.get('name','')
        password = request.form.get('password','')
        email = request.form.get('email','')
       # print(username,password)
        if(username =='' and password =='' and email==''):
            msg='please fill the form!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Invalid username !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        else:
            cur.execute('INSERT INTO user (username,password,email) VALUES (%s,%s,%s)', (username, password, email ))
            cnx.commit()
            msg = 'You have successfully registered !'
            return render_template("index.html")
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("register.html",msg=msg)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/predict", methods=['post'])
def predict():
    name=request.form['name']
    print(name)
    try:
     l=model.recommend(name)
     print(l)
     return render_template("mainpage.html",users=l)
    except:
     return render_template("mainpage.html",err="Check the spelling or try another movie")

if __name__=='__main__':
    app.run(host='localhost',port=1000)
