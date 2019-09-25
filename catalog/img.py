from flask import Flask,redirect,url_for,request,render_template
app=Flask(__name__)
@app.route('/success/<name>')
def success(name):
    return 'welcome %s'%name

@app.route('/image_upload',methods= ['POST','GET'])
def image_upload():
        if request.method=='POST' :
                f=request.files['f']
                f.save(f.filename)
                return redirect(url_for("success", name = f.filename))

@app.route('/log')
def log():
    return render_template('img.html',name='User')

if __name__ == '__main__':
    app.run(debug=True)