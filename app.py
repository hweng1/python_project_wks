from flask import Flask, render_template, request
from logincheck import loginmatch
from calculations import find_user_id, profit_loss, time, BB_per_hr, pl_per_hr, user_table, new_session_id
import sqlite3
# from logincheck import loginid

app = Flask(__name__)

conn = sqlite3.connect('Profile.db')
my_cursor = conn.cursor()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        login_id = (request.form['login_id'])
        password = (request.form['password'])
        try:
            check = loginmatch(login_id, password)
            print(check)
            if check == True:
                return render_template('result_output.html',
                p_l=profit_loss(login_id), 
                t=time(login_id), 
                pl_h=pl_per_hr(login_id), 
                BB_h=BB_per_hr(login_id),
                u_t=user_table(login_id))
        except:
            return render_template('login_page.html', error=True)
    return render_template('login_page.html', error=None)

                
@app.route('/input',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sessionDetails = request.form
        location = sessionDetails['location']
        hours = sessionDetails['hours']
        win = sessionDetails['win']
        loss = sessionDetails['loss']
        small_blind = sessionDetails['SB']
        big_blind = sessionDetails['BB']
        # sid = new_session_id()
        session_id = new_session_id(Login_id=request.form['login_id'])
        cur = sqlite3.connect('Profile.db').cursor()
        cur.execute('INSERT INTO Session (BB, SB, win, loss, location, hours) VALUES(?,?,?,?,?,?,?)',(session_id, big_blind, small_blind, win, loss, location, hours))
        conn.connection.commit()
        cur.close()
        return 'data has been entered'
    return render_template('data_input.html')

@app.route('/result')
def result():
    return render_template('result_output.html')

# @app.route('/delete', method=['GET','POST'])
# def delete():
#     pass

if __name__ =='__main__':
    app.run(debug=True)