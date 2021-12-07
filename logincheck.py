import sqlite3
def loginmatch(login_id, password):
    conn = sqlite3.connect('Profile.db')
    my_cursor = conn.cursor()

    sql1 = "SELECT Profile.Login_id,Profile.Password FROM Profile"

    my_cursor.execute(sql1)

    profile_list = my_cursor.fetchall()

    checklist = list()
    for i in profile_list:
        checklist.append(i)
    
    login_id = str(login_id)
    password = str(password)

    input_crudential = (login_id, password)

    for tu in checklist:
        if input_crudential in checklist:
            return True
        else:
            return False

# print(loginmatch('Corinna', 123456))