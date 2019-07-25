'''import sqlite3 as sql
conn = sql.connect("db_db.sqlite")
cur = conn.cursor()
def execute():
    cur.execute("CREATE TABLE IF NOT %s (id INTEGER,  )")'''

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_bot import vkbot
import function as func

def msg(user_id, Message):
    vk.messages.send(user_id = event.user_id, random_id = get_random_id(), message = Message)    
    
vk_sess = vk_api.VkApi(token = "b2988ed57b558cca8bb1b8ec5e4b998a45214845e964fca9463dd09e2f79c62e9e6f900a8451e6a5f6709")
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)

for event in longpoll.listen():
    print(event)
    #boolean1 = boolean2 = False
    if event.type == VkEventType.MESSAGE_NEW and event.text and event.to_me and event.from_user:
        bot = vkbot(event.user_id)
        msg(event.user_id, bot.new_msg(event.text))
