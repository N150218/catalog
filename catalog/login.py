from flask import Flask,redirect,url_for,request,render_template
app=Flask(__name__)
@app.route('/success/<name>')
def success(name):
    return 'welcome %s'%name
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user=request.form['n']
        return redirect(url_for('success',name=user))
    else:
        user=request.args.get('n')
        return redirect(url_for('success',name=user))
@app.route('/log')

def log():
    return render_template('index.html',name='User')
if __name__ == '__main__':
    app.run(debug=True)