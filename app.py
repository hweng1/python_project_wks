from flask import Flask, render_template, request
# from flaskext.mysql import MySQL
from flask.mysql import MySQL
import yaml
from logincheck import loginmatch
from pmath import find_user_id, profit_loss, time, BB_per_hr, pl_per_hr, user_table

app = Flask(__name__)

db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login_id = (request.form['login_id'])
        password = (request.form['password'])
        try:
            check = loginmatch(login_id, password)
            if check == True:
                return render_template('result_output.html', profit_loss, time, pl_per_hr, BB_per_hr,user_table)
        except:
            return render_template('error.html', error=True)
    return render_template('login_page.html', error=None)
                
@app.route('/input',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sessionDetails = request.form
        location = sessionDetails['location']
        session_time = sessionDetails['hours']
        total_gain = sessionDetails['win']
        total_loss = sessionDetails['loss']
        small_blind = sessionDetails['SB']
        big_blind = sessionDetails['BB']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO Session(BB, SB, win, loss, location, hours) VALUES(%f,%f,%f,%f,%s,%f)',(BB,SB,Profit,Loss,Location,Time))
        mysql.connection.commit()
        cur.close()
        return 'data has been entered'
    return render_template('data_input.html')

@app.route('/result', method=['GET','POST'])
def table():
    return render_template('result_output.html')

@app.route('/delete', method=['GET','POST'])
def delete():
    pass

if __name__ =='__main__':
    app.run(debug=True)