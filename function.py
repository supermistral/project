import sqlite3 as sql
import calendar
import datetime

#user = input()

class SQL:
    def __init__(self, user):
        self.User = 'name'+str(user)
        self.date = datetime.datetime.now().strftime("%Y%m%d")

    def open_close(subfunction):
        def wrapper(self, *args):
            self.conn = sql.connect("base_db.sqlite")
            self.cur = self.conn.cursor()
            a = subfunction(self, *args)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return a
        return wrapper

    @open_close
    def get_conn(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS %s (income INTEGER DEFAULT 0, residue INTEGER DEFAULT 0, daily_res INTEGER, data TEXT, balance INTEGER DEFAULT 0, expense INTEGER DEFAULT 0, reserve INTEGER, nextdata TEXT)" %self.User)

    @open_close
    def handler(self):                                                                    #Обработчик команды старт, чтобы не дублировать записи в один день
        #self.cur.execute("SELECT data FROM %s WHERE data IS NOT NULL" %self.User)
        #for i in self.cur: temp_data = i[0]
        self.cur.execute("SELECT nextdata FROM %s" %self.User)
        if self.cur.fetchone() == None: return 0
        self.cur.execute("SELECT nextdata FROM %s" %self.User)
        for i in self.cur: temp_nextdata = i[0]
        if self.date <= temp_nextdata: return 1
        return 0

    @open_close
    def handler_expense(self):                                                              #Обработчик ячейки дата, чтобы избежать нарушений алгоритма 
        self.cur.execute("SELECT data FROM %s WHERE data = %s" %(self.User, self.date))     #обновления трат и запаса
        #print(self.cur.fetchall())
        if self.cur.fetchall() == []: 
            return 0
        return 1

    @open_close
    def handler_nextdata(self):                                                              #Обработчик вносимой юзером даты получения з/п - отслеживает
        self.cur.execute("SELECT nextdata FROM %s" %(self.User))                             #связь с текущей датой
        for i in self.cur: temp_nextdata = i[0]
        if self.date > temp_nextdata: return 0
        return 1
    
    @open_close
    def add_income(self, value):                                                            #Обновление доходов и ячеек бюджета на день и трат (защита от ошибок
        self.cur.execute("UPDATE %s SET income = %s, expense = 0, daily_res = 0 WHERE data = %s" %(self.User, value, self.date))    #при перезаписи)

    @open_close
    def add_residue(self, value):
        self.cur.execute("UPDATE %s SET residue = %s, expense = 0, daily_res = 0 WHERE data = %s" %(self.User, value, self.date))
    
    @open_close
    def add_data(self):
        #print(self.date)
        self.cur.execute("INSERT INTO %s (data) VALUES (%s)" %(self.User, self.date)) 

    @open_close
    def add_daily_data(self, value):                                                        #Установщик даты, ежедневного бюджета, траты и запаса 
        #print(self.date)                                                                   #при первом вызове команды трата в новый день
        #self.cur.execute("INSERT INTO %s (data) VALUES (%s)" %(self.User, self.date)) 
        self.cur.execute("SELECT daily_res FROM %s WHERE data < %s" %(self.User, self.date))
        temp = self.cur.fetchone()[0]
        self.cur.execute("UPDATE %s SET daily_res = %d WHERE data = %s" %(self.User, temp, self.date))
        self.cur.execute("SELECT expense FROM %s WHERE data = %s" %(self.User, self.date))
        temp_expense = self.cur.fetchone()[0]
        self.cur.execute("UPDATE %s SET expense = %d WHERE data = %s" %(self.User, value + temp_expense, self.date))
        self.cur.execute("SELECT data, reserve, nextdata FROM %s WHERE data < %s" %(self.User, self.date))
        for i in self.cur: temp_data, temp_reserve, temp_nextdata = str(i[0]), i[1], str(i[2])
        #print(temp_data, temp_reserve)
        self.cur.execute("SELECT daily_res FROM %s WHERE data = %s" %(self.User, self.date))
        temp_daily_res = int(self.cur.fetchone()[0])
        temp_data = (datetime.datetime.now() - datetime.datetime(int(temp_data[:4]), int(temp_data[4:6]), int(temp_data[6:]))).days
        self.cur.execute("UPDATE %s SET reserve = %d, nextdata = %s WHERE data = %s" %(self.User, (temp_reserve + temp_data*temp_daily_res - value), temp_nextdata, self.date))
        return temp_reserve + temp_data*temp_daily_res - value
    
    @open_close
    def add_result(self):
        now = datetime.datetime.now()
        self.cur.execute("SELECT (nextdata) FROM %s WHERE data = %s" %(self.User, self.date))
        temp_data = self.cur.fetchone()[0]
        days = abs((now - datetime.datetime(int(temp_data[:4]), int(temp_data[4:6]), int(temp_data[6:]))).days)
        print(days)
        self.cur.execute("SELECT (income) FROM %s WHERE data = %s" %(self.User, self.date))
        temp_income = self.cur.fetchone()[0]
        self.cur.execute("SELECT (residue) FROM %s WHERE data = %s" %(self.User, self.date))
        temp_residue = self.cur.fetchone()[0]
        self.cur.execute("SELECT (balance) FROM %s WHERE data = %s" %(self.User, self.date))
        temp_balance = self.cur.fetchone()[0]
        self.cur.execute("UPDATE %s SET daily_res = %d WHERE data = %s" %(self.User, (temp_income - temp_balance - temp_residue)/days, self.date))
        self.cur.execute("UPDATE %s SET reserve = %d WHERE data = %s" %(self.User, (temp_income - temp_balance - temp_residue)/days, self.date))
    
    @open_close
    def select_result(self):
        self.cur.execute("SELECT (daily_res) FROM %s WHERE data = %s" %(self.User, self.date))
        for i in self.cur: 
            if not i[0]: return 'Неполный ввод'
            daily_res_send = i[0]
        return daily_res_send
    
    @open_close
    def add_balance(self, value):
        self.cur.execute("UPDATE %s SET balance = %s WHERE data = %s" %(self.User, value, self.date)) 

    @open_close
    def add_expense(self, value):                                                                  #Обработчик команды трата, вызываемой повторно в один день                              
        self.cur.execute("SELECT expense FROM %s WHERE data = %s" %(self.User, self.date))
        temp_expense = self.cur.fetchone()[0]
        self.cur.execute("SELECT reserve FROM %s WHERE data = %s" %(self.User, self.date))
        temp_reserve = self.cur.fetchone()[0]
        self.cur.execute("UPDATE %s SET expense = %d, reserve = %d WHERE data = %s" %(self.User, temp_expense + value, temp_reserve - value, self.date))
        return temp_reserve - value

    @open_close
    def add_nextdata(self, value):                                                                        #Обновлятор введенной юзером даты
        self.cur.execute("UPDATE %s SET nextdata = %s WHERE data = %s" %(self.User, value, self.date))


        
