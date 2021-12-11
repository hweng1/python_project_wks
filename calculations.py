from tabulate import tabulate
import sqlite3

def find_user_id(Login_id):
    '''find the user_id in the database according to the user inputs'''
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_3 = 'SELECT Profile.Login_id, Profile.User_id FROM Profile'
    my_cursor.execute(sql_3)

    Profile_Login_User_id = my_cursor.fetchall()
    id_list = list()

    for i in Profile_Login_User_id:
        id_list.append(i)
    # print(id_list)

    id_dic = {}
    for t in id_list:
        id_dic[t[0]] = t[1]
    # print(id_dic)

    for key in id_dic:
        if Login_id == key:
            return id_dic[key]
        

# find_user_id('Michael')



def profit_loss(Login_id):
    """find the total amount won/lost based on all sessions inputed by a user"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_4 = 'SELECT Session.Profit, Session.Loss, Session.User_id FROM Session'
    my_cursor.execute(sql_4)

    user_id = find_user_id(Login_id)

    Session_pl_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_pl_list:
        whole_list.append(i)
    # print(whole_list)

    pl_sum = 0
    for t in whole_list:
        if t[2] == user_id:
            pl_sum += float(t[0]) - float(t[1])
    return pl_sum

# print(profit_loss('Michael'))
# 200

def time(Login_id):
    """calculate the total time of each user spends playing poker"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_5 = 'SELECT Session.Time, Session.User_id FROM Session'
    my_cursor.execute(sql_5)
    user_id = find_user_id(Login_id)

    Session_pl_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_pl_list:
        whole_list.append(i)
    # print(whole_list)

    time_sum = 0
    for t in whole_list:
        if t[1] == user_id:
            time_sum += float(t[0])
    return time_sum
# print(time('Michael'))
# 12

def pl_per_hr(Login_id):
    """calculate overall profit loss per hour"""
    pl_per_hr = profit_loss(Login_id) / time(Login_id)
    return f'{pl_per_hr:.2f}'
# print(pl_per_hr('Michael'))
# 200/12


def BB_per_hr(Login_id):
    """calculate the number of big blind a player can win per hour"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_6 = 'SELECT Session.Profit, Session.Loss, Session.BB, Session.User_id FROM Session'
    my_cursor.execute(sql_6)
    user_id = find_user_id(Login_id)
    Session_pl_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_pl_list:
        whole_list.append(i)
    # print(whole_list)

    pl_sum_in_bb = 0
    for t in whole_list:
        if t[3] == user_id:
            pl_sum_in_bb += (float(t[0]) - float(t[1]))/float(t[2])
            bb_per_hr = pl_sum_in_bb/time(Login_id)
    return (f'{bb_per_hr:.2f}')
# print(BB_per_hr('Michael'))
    #50/12

def user_table(Login_id):
    """show all session input by an user on the result page. the outcome is a html formatted string."""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_7 = 'SELECT * FROM Session'
    my_cursor.execute(sql_7)

    user_id = find_user_id(Login_id)
    sql_list = my_cursor.fetchall()
    table_list = list()

    for i in sql_list:
        table_list.append(i)
    # print(table_list)

    table = [['Session_id', 'Big_Blind', 'Small_Blind', 'Win', 'Loss', 'Location', 'Time','User_id']]
    sessions = []
    for t in table_list:
        if user_id ==t[7]:
            sessions.append(t)
    # print(sessions)

    for i in sessions:
        column_list = list(i)
        table.append(column_list)
    # print(table)    
    # another way of alter the list
    # table_list = []
    # for t in sessions:
    #     loop_list = []
    #     for i in range(len(t)):
    #         loop_list.append(t[i])
    #     table_list.append(loop_list)
    # print(table_list)

    user_table = tabulate(table,headers='firstrow',tablefmt='html')
    return user_table
# print(user_table('Michael'))

def new_user_id():
    """calculate the new user id for newly registered users"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_8 = 'SELECT * FROM Profile'
    my_cursor.execute(sql_8)
    Profile_list = my_cursor.fetchall()
    id_list = list()

    for i in Profile_list:
        id_list.append(i)
    print(id_list)

    last_id = len(id_list)-1
    hst_sid = int(id_list[last_id][0])
    new_id = hst_sid+1
    return new_id
# print(new_user_id())

def new_session_id():
    """calculate new session ID for newly input session information"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_8 = 'SELECT * FROM Session'
    my_cursor.execute(sql_8)
    Session_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_list:
        whole_list.append(i)
    # print(whole_list)

    last_session_t = len(whole_list)-1
    hst_sid = int(whole_list[last_session_t][0])
    new_session_id = hst_sid+1
    return new_session_id
# print(new_session_id())
# expect: 4

def graph_label(Login_id):
    """form a new list for labels on the x-axis for the outcome table"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_4 = 'SELECT Session.session_id, Session.Profit, Session.Loss, Session.User_id FROM Session'
    my_cursor.execute(sql_4)

    user_id = find_user_id(Login_id)

    Session_pl_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_pl_list:
        whole_list.append(i)
    # print(whole_list)

    labels = []
    for t in whole_list:
        if t[3] == user_id:
            # a.replace("'","")
            labels.append(f'Session {t[0]}')
    return labels

def graph_data(Login_id):
    """show session win or lose situation on the y axis"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_4 = 'SELECT Session.session_id, Session.Profit, Session.Loss, Session.User_id FROM Session'
    my_cursor.execute(sql_4)

    user_id = find_user_id(Login_id)

    Session_pl_list = my_cursor.fetchall()
    whole_list = list()

    for i in Session_pl_list:
        whole_list.append(i)
    # print(whole_list)

    datas = []
    for t in whole_list:
        if t[3] == user_id:
            pl_sum = float(t[1]) - float(t[2])
            datas.append(pl_sum)
    return datas


def first_input(Login_id):
    """check whether the login input has any sessions under the login user id"""
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()
    sql_4 = 'SELECT Session.session_id, Session.Profit, Session.Loss, Session.User_id FROM Session'
    my_cursor.execute(sql_4)
    whole_list = my_cursor.fetchall()
    user_id = find_user_id(Login_id)
    session_list = []
    for t in whole_list:
        if t[3] == user_id:
            # a.replace("'","")
            session_list.append(f'Session {t[0]}')
    # print(len(session_list))
    return session_list

# print(graph_data('Michael'))
# print(graph_label('Michael'))
    # session_id_list = 
    # for t in whole_list:
    #     for i in range(t):
            