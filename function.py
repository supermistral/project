import sqlite3 as sql
import calendar
import datetime

#user = input()


def get_conn(user):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS %s (income INTEGER, residue INTEGER, daily_res INTEGER, data TEXT)" %('name'+str(user)))
    conn.commit()
    cur.close()
    conn.close()

def add_income(user, value):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE %s SET income = %s WHERE data = %s" %('name'+str(user), value, str(datetime.datetime.now())[:10]))
    conn.commit()
    cur.close()
    conn.close()

def add_residue(user, value):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    cur.execute("UPDATE %s SET residue = %s WHERE data = %s" %('name'+str(user), value, str(datetime.datetime.now())[:10]))
    conn.commit()
    cur.close()
    conn.close()

def add_data(user):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    print(str(datetime.datetime.now())[:10])
    cur.execute("INSERT INTO %s (data) VALUES (%s)" %('name'+str(user), str(datetime.datetime.now())[:10])) 
    conn.commit()
    cur.close()
    conn.close()

def add_result(user):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    now = datetime.datetime.now()
    temp_now = str(now)[:10]
    days = calendar.monthrange(now.year, now.month)[1]
    temp = '((SELECT income FROM %s WHERE data = %s) - (SELECT residue FROM %s WHERE data = %s))/%d' %('name'+str(user), temp_now, 'name'+str(user), temp_now, days)
    cur.execute("UPDATE %s SET daily_res = %s" %('name'+str(user), temp))
    conn.commit()
    cur.close()
    conn.close()

def select_result(user):
    conn = sql.connect("base_db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT (daily_res) FROM %s WHERE data = %s" %('name'+str(user), str(datetime.datetime.now())[:10]))
    for i in cur: 
        print(i)
        daily_res_send = i[0]
    if cur.fetchall() == (): daily_res_send = 'Неполный ввод'
    conn.commit()
    cur.close()
    conn.close()
    return daily_res_send
