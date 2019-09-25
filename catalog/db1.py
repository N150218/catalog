from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from db import Register,Base,User #import class register ,base 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager,current_user,login_user,logout_user,login_required
app=Flask(__name__)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))

@app.route("/login2",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))
    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()
            if user:
                login_user(user)
                return redirect(url_for('showData'))
            else:
                flash('login Failed')
        else:
            return render_template('auth.html',title='login')
    except Exception as e:
        flash("Login Failed")
    else:
        return render_template('auth.html',title='login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('registerData')) #logout doesnot send the post request

engine=create_engine('sqlite:///register.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind= engine
DBsession=sessionmaker(bind=engine)
session=DBsession()
app.secret_key='helo'

@app.route('/register',methods=['POST','GET'])
def registerData():
    if request.method=='POST':
        regdata1=User(name=request.form['name'],email=request.form['email'],password=request.form['password'])
        session.add(regdata1)
        session.commit()
        return redirect(url_for('showData2'))
    else:
        return render_template('login.html')    #from logout it comes to Create your  profile

@app.route('/show')
@login_required
def showData():
    register1=session.query(Register).all()#register class
    return render_template('show.html',reg=register1)
@app.route('/show2')
def showData2():
    login_cred=session.query(User).all()#register class
    return render_template('show.html',reg=login_cred)

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/nav')
def nav():
    return render_template('nav.html')

@app.route('/addData',methods=['POST','GET'])
def addData():
    if request.method=='POST':
        newData=Register(name=request.form['name'],email=request.form['email'],des=request.form['des'])
        session.add(newData)
        session.commit()
        flash("new data is added","my name is sumanth")
        return  redirect(url_for('showData2'))
    else:
        return render_template('form.html')
    

@app.route('/edit/<int:register_id>',methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editedData.name=request.form['name']
        editedData.email=request.form['email']
        editedData.des=request.form['des']
        session.add(editedData)
        session.commit()
        return redirect(url_for('showData'))
    else:
        return render_template('edit.html',old=editedData,user_given_id=register_id)

@app.route('/delete/<int:register_id>')
def delete(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if(editData):
        session.delete(editedData)
        session.commit()
        return redirect(url_for('showData'))
    else:
        return redirect(url_for('form'))

if __name__=='__main__':
    app.run(debug=True)
