import sys
sys.path.insert(0,'db/')
from flask import Flask,request,redirect,url_for,flash,session,render_template
from dbhelper import *

app:any = Flask(__name__)
app.secret_key='056cbae6d7b34d718e278eb858744c33'

@app.after_request
def after_request(response)->None:
    response.headers['Cache-Control']="no-cache, no-store, must-revalidate max-age=0"
    response.headers["Pragma"]="no-cache"
    response.headers["Expires"]="0"
    return response
    
@app.route("/")
def index()->None:
    return render_template("index.html")

@app.route("/signup",methods=['GET','POST'])
def signup()->None:
    if request.method == 'POST':
        email:str = request.form['email']
        password:str = request.form['password']
        confirm_password:str = request.form['confirm_password']

        if password != confirm_password:
            flash('PASSWORDS DO NOT MATCH')
            return redirect(url_for('signup'))

        user:list = getrecord('users',email=email)

        if len(user)>0:
            flash('EMAIL ALREADY REGISTERED')
            return redirect(url_for('signup'))

        if addrecord('users',email=email,password=password):
            flash('REGISTRATION SUCCESSFUL')
            return redirect(url_for('index'))
        else:
            flash('REGISTRATION FAILED')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route("/logout")
def logout()->None:
    session.clear()
    response = redirect(url_for('index'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    
@app.route("/main")
def main()->None:
    email = session.get('email')

    if email:
        slist:list = getall('students')
        return render_template("main.html",students=slist,email=email)
    else:
        flash('PLEASE LOG IN AGAIN TO ACCESS THIS PAGE.')
        return redirect(url_for('index'))
    
@app.route("/userlogin",methods=['POST'])
def userlogin()->None:
    email:str = request.form['email']
    password:str = request.form['password']

    user:list = getrecord('users',email=email)

    if len(user)>0:
        if user[0][2] == password:
            print('LOGIN SUCCESS')
            session['email'] = email
            return redirect(url_for('main'))
        else:
            flash('INCORRECT PASSWORD')
            return redirect(url_for('index'))
    else:
        flash('INVALID USER')
        return redirect(url_for('index'))    
    
if __name__=="__main__":
    app.run(debug=True)