from flask import Flask, render_template, request, redirect, session
from calculations import find_user_id, profit_loss, time, BB_per_hr, pl_per_hr, user_table, new_user_id, new_session_id, graph_data, graph_label, first_input
import sqlite3
    

app = Flask(__name__)
app.secret_key = 'secretkeyfortexasholdemamazingapp'

conn = sqlite3.connect('Profile.db', check_same_thread=False)
my_cursor = conn.cursor()


@app.route('/', methods=['GET','POST'])
def checklogin():
    if request.method == 'POST':
        login_id = (request.form['login_id'])
        session["slogin_id"] = login_id
        password = (request.form['password'])
        query1 = "SELECT Login_id, Password From Profile WHERE Login_id = '{un}'AND Password = '{pw}'".format(un = login_id, pw = password )
        rows = my_cursor.execute(query1)
        rows = rows.fetchall()
        if len(rows) == 1:
            return redirect('/result')
        else:
            return render_template('login_page.html')
    else:
        return render_template('login_page.html')


@app.route('/register', methods = ['GET', 'POST'])
def registerpage():
    if request.method == 'POST':
        D_login_id = request.form['D_login_id']
        D_password = request.form['D_password']
        D_user_id = new_user_id()
        query2 = "INSERT INTO Profile (Login_id, Password, User_id) VALUES ('{u}','{p}','{e}')".format(u = D_login_id, p = D_password, e = D_user_id)
        my_cursor.execute(query2)
        conn.commit()
        return render_template('register_success.html')
    return render_template('register.html')

                
@app.route('/input',methods=['GET','POST'])
def index():
    if 'slogin_id' in session:
        login_id = session['slogin_id']
    if request.method == 'POST':
        try:
            User_id = find_user_id(login_id)
            sessionDetails = request.form
            location = sessionDetails['location']
            hours = sessionDetails['hours']
            win = sessionDetails['win']
            loss = sessionDetails['loss']
            small_blind = sessionDetails['SB']
            big_blind = sessionDetails['BB']
            session_id = new_session_id()
            # cur.execute("INSERT INTO Session (session_id, BB, SB, Profit, Loss, Location, Time, User_id) VALUES (?,?,?,?,?,?,?,?)", [session_id, big_blind, small_blind, win, loss, location, hours, User_id))
            query7 = ("INSERT INTO Session (session_id, BB, SB, Profit, Loss, Location, Time, User_id) VALUES ('{a}','{b}','{c}','{d}','{f}','{g}','{h}','{i}')".format(a = session_id, b = big_blind, c = small_blind, d = win, f = loss, g = location, h = hours, i = User_id))
            my_cursor.execute(query7)
            conn.commit()
            return render_template('enter_success.html')
        except:
            return redirect('/input')
    return render_template('data_input.html')


@app.route('/result')
def result():
    if 'slogin_id' in session:
        login_id = session['slogin_id']
        if len(first_input(login_id)) == 0:
            return redirect('/input')
        return render_template('result_output.html', p_l=profit_loss(login_id), 
            t=time(login_id), 
            pl_h=pl_per_hr(login_id), 
            BB_h=BB_per_hr(login_id),
            u_t=user_table(login_id),
            graph_label=graph_label(login_id),
            graph_data=graph_data(login_id))


@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        try:
            dl_id = (request.form['dl_id'])
            query3 = "DELETE FROM Session WHERE session_id = '{n}'".format(n = dl_id)
            my_cursor.execute(query3)
            conn.commit()
            return render_template('success.html', session_id = dl_id)
        except:
            return render_template('delete.html')
    else:
        return render_template('delete.html')



if __name__ =='__main__':
    app.run(debug=True)
