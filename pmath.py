from tabulate import TableFormat, tabulate
from werkzeug.datastructures import Headers
def find_user_id(Login_id):
    import mysql.connector
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='425575404',
        database='OIM3640_Project'
    )
    my_cursor = mydb.cursor()
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
    import mysql.connector
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='425575404',
        database='OIM3640_Project'
    )
    my_cursor = mydb.cursor()
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
    import mysql.connector
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='425575404',
        database='OIM3640_Project'
    )
    my_cursor = mydb.cursor()
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
    pl_per_hr = profit_loss(Login_id) / time(Login_id)
    return f'{pl_per_hr:2f}'
# print(pl_per_hr('Michael'))
# 200/12


def BB_per_hr(Login_id):
    import mysql.connector
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='425575404',
        database='OIM3640_Project'
    )
    my_cursor = mydb.cursor()
    sql_6 = 'SELECT Session.Profit, Session.Loss, Session.BB, Session.User_id FROM Session'
    my_cursor.execute(sql_5)

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
    import mysql.connector
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password='425575404',
        database='OIM3640_Project'
    )
    my_cursor = mydb.cursor()
    sql_7 = 'SELECT * FROM Session'
    my_cursor.execute(sql_7)

    user_id = find_user_id(Login_id)
    sql_list = my_cursor.fetchall()
    table_list = list()

    for i in sql_list:
        table_list.append(i)
    # print(table_list)

    table = [['Session_id', 'Big_Blind', 'Small_Blind', 'Win', 'Loss', 'Location', 'Time']]
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

    user_table = tabulate(table,headers='firstrow',tablefmt='fancy_grid')
    return user_table

print(user_table('Michael'))
