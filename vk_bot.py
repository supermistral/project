import function as func

class vkbot:
    def __init__(self, user_id):
        self.User_id = user_id
        self.Commands = ['старт', 'доход', 'расход', 'расчет']

    def new_msg(self, message):
        if message.lower() == self.Commands[0]:
            func.get_conn(self.User_id)
            func.add_data(self.User_id)
            return 'Финансовый помощник активирован'
        elif self.Commands[1] in message.lower():
            func.add_income(self.User_id, message[6:])
            return 'Принято'
        elif self.Commands[2] in message.lower():
            func.add_residue(self.User_id, message[7:])
            return 'Принято'
        elif message.lower() == self.Commands[3]:
            func.add_result(self.User_id)
            return 'Бюджет на день - ' + str(func.select_result(self.User_id))
        else: return 'Неизвестная команда'
