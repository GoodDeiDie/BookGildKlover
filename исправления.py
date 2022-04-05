from email import message
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import time
import requests
import sqlite3 as sql 





token = "18b76a9af54ed5d8e8c3c66ce59f76459a0a2148b57392ab2899c03a1a184ebd1549e71d5c5a258b62008"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


con = sql.connect('libone.db')
cur = con.cursor()

cur.execute("SELECT * FROM book;")
result = cur.fetchall()

for i in result:
    id = i[1]
    our_loot =i[0]
    
    new_loot = our_loot.rstrip()
    cur.execute("update book set name = (?) where name = (?) and id = (?);", (new_loot,our_loot,id))
    con.commit()




# cur.execute("update book set coast = (?) where name = (?) and id = (?);", (coast,our_loot,id))
# con.commit()