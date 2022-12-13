from flask_app import app
from flask import Flask, render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt=Bcrypt(app)


@app.route("/")
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")


@app.route("/create",methods=['post'])
def create_user():
    if not User.validator(request.form):
        return redirect('/')
    hashed_pass=bcrypt.generate_password_hash(request.form['password'])
    data={
        **request.form,
        'password':hashed_pass
    }
    logged_user_id=User.create(data)
    session['user_id']=logged_user_id
    return redirect('/dashboard')


@app.route("/login",methods=['post'])
def login_user():
    data={
        'email':request.form['email']
    }
    user_in_db=User.get_by_email(data)
    if not user_in_db:
        flash("Invalid!",'log')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
        flash("Invalid!",'log')
        return redirect('/')
    session['user_id']=user_in_db.id
    return redirect('/dashboard')




@app.route("/dashboard")
def success():
    if 'user_id' not in session:
        return redirect('/')
    data={
        'id':session['user_id']
    }
    logged_user=User.get_by_id(data)
    return render_template("success.html",logged_user=logged_user)




@app.route("/logout")
def logout():
    del session['user_id']
    return redirect('/')
