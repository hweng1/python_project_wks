from flask import Flask, render_template, request, redirect, session
from calculations import find_user_id, profit_loss, time, BB_per_hr, pl_per_hr, user_table, new_session_id
import sqlite3
# import sqlalchemy
# from logincheck import loginid
    

app = Flask(__name__)
app.secret_key = 'secretkeyfortexasholdemamazingapp'

conn = sqlite3.connect('Profile.db', check_same_thread=False)
my_cursor = conn.cursor()


@app.route('/', methods=['GET','POST'])
def checklogin():
    if request.method == 'POST':
        session.pop('user_name', None)
        session.pop('user_password', None)
        login_id = (request.form['login_id'])
        password = (request.form['password'])
        query1 = "SELECT Login_id, Password From Profile WHERE Login_id = '{un}'AND Password = '{pw}'".format(un = login_id, pw = password )
        rows = my_cursor.execute(query1)
        rows = rows.fetchall()
        if len(rows) == 1:
            session['user_name'] = login_id
            session['password'] = password
            return render_template('result_output.html'
            )
        else:
            return redirect('/')
    else:
        return render_template('login_page.html')

@app.route('/register', methods = ['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        D_login_id = request.form['D_login_id']
        D_password = request.form['D_password']
        query2 = "INSERT INTO Profile (Login_id, Password) VALUES ('{u}','{p}')".format(u = D_login_id, p = D_password)
        my_cursor.execute(query2)
        conn.commit()
        return redirect('/')
    return render_template('register.html')

                
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
        conn.commit()
        cur.close()
        return 'data has been entered'
    return render_template('data_input.html')

@app.route('/result')
def result():
    return render_template('result_output.html')

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        try:
            dl_id = (request.form['dl_id'])
            query1 = 'DELETE * From Session WHERE session_id = {un}'.format(un = dl_id)
            my_cursor.execute(query1)
            conn.commit()
            return render_template('success.html', session_id = dl_id)
        except:
            return render_template('delete.html')
    else:
        return render_template('delete.html')

if __name__ =='__main__':
    app.run(debug=True)
