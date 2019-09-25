from flask import Flask,redirect,url_for,request,render_template
app=Flask(__name__)

@app.route('/table/<int:value1>')
def table(value1):
    return render_template('index1.html',value=value1,len=10)
if __name__ == '__main__':
    app.run(debug=True)