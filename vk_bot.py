from function import SQL

class vkbot:
    def __init__(self, user_id):
        self.User_id = user_id
        self.Commands = ['начать', 'доход', 'расход', 'расчет', 'остаток', 'трата', 'дата']

    def new_msg(self, message):
        func = SQL(self.User_id)
        if message.lower() == self.Commands[0]:
            func.get_conn()
            if func.handler():
                return 'Вы уже начали работу с ботом в текущем месяце'
            func.add_data()
            return """Финансовый помощник активирован

"дата ГГГГММДД - ввод даты получения следующей выручки, где ГГГГ - год, ММ - месяц, ДД - день (например, 20190830)"

"доход СУММА" - ввод заработной платы, где СУММА - число

"расход СУММА" - ввод суммы обязательных выплат

"остаток СУММА" - ввод кол-ва средств, зарезервированных до конца месяца

"расчет" - отображение ежедневного бюджета в течение текущего месяца"""
        elif self.Commands[1] == message.lower()[:5] and message[5] == ' ':
            try: k = int(message[6:])
            except: return 'Некорректный ввод'
            else: func.add_income(message[6:])
            return 'Принято'
        elif self.Commands[2] == message.lower()[:6] and message[6] == ' ':
            try: k = int(message[7:])
            except: return 'Некорректный ввод'
            else: func.add_residue(message[7:])
            return 'Принято'
        elif self.Commands[4] == message.lower()[:7] and message[7] == ' ':
            try: int(message[8:])
            except: return 'Некорректный ввод'
            else: func.add_balance(message[8:])
            return 'Принято'
        elif message.lower() == self.Commands[3]:
            try: 
                func.add_result()
                result = str(func.select_result())
            except: return 'Проверьте правильность ранее вводимых данных'
            return ("""Бюджет на день: %s
Теперь вы вправе заносить ежедневные данные
"трата СУММА" - ввод потраченных средств (разрешается многократное использование)""" %result)
        elif message.lower()[:4] == self.Commands[6] and message[4] == ' ':
            try: k = int(message[5:])
            except: return 'Некорректный ввод'
            else: func.add_nextdata(message[5:])
            return 'Принято'
        elif func.handler_nextdata():
            if message.lower()[:5] == self.Commands[5] and message[5] == ' ':
                try: k = int(message[6:])
                except: return 'Некорректный ввод'
                else: 
                    if func.handler_expense() == 0:
                    #print(25)
                        func.add_data()
                        result = str(func.add_daily_data(int(message[6:])))        
                    else: result = str(func.add_expense(int(message[6:])))
                    return 'На сегодняшний день в запасе: ' + result
            else: return 'Некорректный ввод'
        else: return 'Неизвестная команда'
