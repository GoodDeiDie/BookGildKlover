from email import message
from vk_api.longpoll import VkLongPoll, VkEventType
from pas import token as tk

import vk_api
import random
import time
import requests
import sqlite3 as sql 






token = tk
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

id_chat_buff = 8

con = sql.connect('libgild.db')
cur = con.cursor()



def registration_count(resp):
    
    sp = resp.split()
    id_user = sp[0][1:-1]
    book = sp[5:-4]
    namebook = ''
    for i in book:
        namebook = namebook + i + ' '

    
    colbook = int(namebook.split('*')[0][1:])
    # name = namebook[3:-2]
    name = namebook.split('*')[1][:-2]
    print( name ,'  ',colbook, '    ', id_user)



    cur.execute("SELECT * FROM book where name = (?);", (name, ))
    result = cur.fetchall()
    if len(result) == 0:
        cur.executemany("INSERT INTO book VALUES(?,?,?,?);", ((name,555555,1,0),))
        coastbook = 1
        con.commit()
    else:
        coastbook = int(result[0][2])



    cur.execute("SELECT * FROM user where id = (?);", (id_user, ))
    result = cur.fetchall()
    if len(result) == 0:
        cur.executemany("INSERT INTO user VALUES(?,?,?,?,?);", ((id_user,int(resp.split('|')[0][4:]),0,0,'reserv'),))
        con.commit()
        count = 0
        cur.execute("update user set count = (?) where  id = (?);", (count,id_user))
        con.commit()

    else:
        count = int(result[0][2])
        coast = count  + coastbook*colbook
        cur.execute("update user set count = (?) where  id = (?);", (coast,id_user))
        con.commit()

    

def antireg(resp, id, id_user):
    our_loot = ''
    if len(resp.split('-')) == 1:
        col = 1
        loot = resp.split()[1:]
        for i in loot:
            our_loot = our_loot + i + ' '
    else:
        col = int(resp.split('-')[-1])
        loot = resp.split('-')[0].split()[1:]
        for i in loot:
            our_loot = our_loot + i + ' '


    cur.execute("SELECT * FROM book where name = (?);", (our_loot.strip(), ))
    result = cur.fetchall()
    if len(result) == 0:
        vk_session.method('messages.send',{'chat_id': id_chat_buff, 'reply_to': id,'message': 'выдать ' + our_loot + '- ' + str(col) + ' штук', 'random_id': 0})
    else:
        coastbook = int(result[0][2])
        cur.execute("SELECT * FROM user where idnumber = (?);", (id_user, ))
        result = cur.fetchall()
        if len(result) == 0:
            vk_session.method('messages.send',{'chat_id': id_chat_buff, 'reply_to': id,'message': 'Не зарегистрирован в системе!', 'random_id': 0})
        else:
            count = int(result[0][2])
            coast = count  - coastbook*col
            if coast < 0:
                vk_session.method('messages.send',{'chat_id': id_chat_buff, 'reply_to': id,'message': 'Не достаточно очков, ваши баллы - ' + str(count), 'random_id': 0})
            else:
                vk_session.method('messages.send',{'chat_id': id_chat_buff, 'reply_to': id,'message': 'выдать ' + our_loot + '- ' + str(col) + ' штук', 'random_id': 0})
                cur.execute("update user set count = (?) where  idnumber = (?);", (coast,id_user))


            con.commit()


def updatecoast(resp):
    loot = resp.split()[2:-1]
    our_loot = ''
    for i in loot:
        our_loot = our_loot + i + ' '
    print(our_loot)
    coast = resp.split()[-1] 
    cur.execute("update book set coast = (?) where name = (?);", (coast,our_loot.rstrip()))
    con.commit()
    vk_session.method('messages.send',{'chat_id': id_chat_buff, 'message': 'изменила', 'random_id': 0})


def price():
    cur.execute("SELECT * FROM book ;")
    result = cur.fetchall()
    msgactiv = ''
    msgpas = ''
    for i in result:
        if i[3] == 0:
            icon = '📘 '
            msgpas = msgpas + icon + i[0] + ' ' + str(i[2]) + '\n'
        else:
            icon = '📕 '
            msgactiv = msgactiv + icon + i[0] + ' ' + str(i[2]) + '\n'

    msg = 'Активные способности:' + '\n' + msgactiv + '\n\n'+ 'Пассивные способности:' + '\n' + msgpas

    vk_session.method('messages.send',{'chat_id': id_chat_buff, 'message': msg, 'random_id': 0})



def icon(resp):
    loot = resp.split()[2:-1]
    our_loot = ''
    for i in loot:
        our_loot = our_loot + i + ' '
    book = our_loot.strip()
    icon = resp.split()[-1]
    
    cur.execute("update book set icon = (?) where name = (?);", (int(icon), book))
    con.commit()
    vk_session.method('messages.send',{'chat_id': id_chat_buff, 'message': 'изменила', 'random_id': 0})


def count_user(resp):
    id_user = resp.split()[2]
    count = resp.split()[3]

    cur.execute("update user set count = (?) where idnumber = (?);", (int(count), int(id_user)))
    con.commit()
    vk_session.method('messages.send',{'chat_id': id_chat_buff, 'message': 'очки изменены', 'random_id': 0})

    print(id_user, '    ', count)


def balance(id, id_s, perem):
    if perem == 1:
        cur.execute("SELECT * FROM user where idnumber = (?);", (id, ))
        result = cur.fetchall()
        if len(result) == 0:
            vk_session.method('messages.send',{'chat_id': id_chat_buff, 'reply_to': id_s,'message': 'Не зарегистрирован в системе!', 'random_id': 0})
        else:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': result[0][0] + ', ваш баланс - ' + str(result[0][2]), 'random_id': 0})
        con.commit()
    elif perem == 0:
        cur.execute("SELECT id, count FROM user;")
        result = cur.fetchall()
        con.commit()
        msg = 'Баланс всех игроков: \n'
        for i in result:
            msg+=i[0] + ' - ' + str(i[1]) + ' очков\n'
        vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': msg, 'random_id': 0})
        


def admin(id):
    cur.execute("SELECT admin FROM user where idnumber = (?);", (id, ))
    result = cur.fetchall()
    con.commit()
    if result[0][0] == 1:
        return True
    else:
        return False

def aaadmin(resp):
    id = resp.split()[2]
    print(resp.split()[3])
    if resp.split()[3] == 'снять':
        ad = 0
        msg = '[id'+ id +'|Администратор] снят!' 
    elif resp.split()[3] == 'назначить':
        ad = 1
        msg = '[id'+ id +'|Администратор] назначен!' 
        

    cur.execute("update user set admin = (?) where idnumber = (?);", (ad, int(id)))
    con.commit()
    vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': msg, 'random_id': 0})


def spravka(resp):
    if 'справка' in resp:
        return False
    else:
        return True



def help(resp):
    rsp = resp.split()

    if rsp[0] == '!добавьописание':
        description = resp.split('|')[1]
        cur.execute("SELECT * FROM help where id = (?);", (rsp[1], ))
        result = cur.fetchall()
        if len(result) == 0:
            cur.executemany("INSERT INTO help VALUES(?,?);", ((rsp[1], description),))
            con.commit()
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Описание добавлено', 'random_id': 0})
        else:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Описание существует!', 'random_id': 0})

    elif rsp[0] == '!измениописание':
        description = resp.split('|')[1]
        cur.execute("SELECT * FROM help where id = (?);", (rsp[1], ))
        result = cur.fetchall()
        if len(result) == 0:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Описания не существует!', 'random_id': 0})
        else:
            cur.execute("update help set description = (?) where id = (?);", (description, rsp[1]))
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Описание изменено!', 'random_id': 0})
            con.commit()
    elif rsp[0] == '!покажиописание':
        cur.execute("SELECT description FROM help where id = (?);", (rsp[1], ))
        result = cur.fetchall()
        if len(result) == 0:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Описания не существует!', 'random_id': 0})
        else:
            msg = result[0][0]
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': msg, 'random_id': 0})
            con.commit()



def dhelp(resp):
    cur.execute("SELECT description FROM help where id = (?);", (resp[1:], ))
    result = cur.fetchall()
    vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': result[0][0], 'random_id': 0})
    con.commit()


def delbook(resp):
    rp = resp.split()[2:]
    book = ''
    for i in rp:
        book += i + ' '

    cur.execute("delete from book where name = (?)", (book.strip(), ))
    con.commit()

def convertgold(resp, id, id_s):
    gold = resp.split()[1]
    cur.execute("SELECT count FROM user where idnumber = (?);", (id, ))
    result = cur.fetchall()
    if len(result) == 0:
        vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Вы не зарегистрированны в системе!', 'random_id': 0})
    else:
        count= result[0][0]
        ostatok = count - int(gold)
        if ostatok >0:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'reply_to': id_s,'message': 'выдать ' + gold + ' золота', 'random_id': 0})
            cur.execute("update user set count = (?) where idnumber = (?);", (ostatok, id))
        else:
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Недостаточно балов! Ваши балы: ' + str(count), 'random_id': 0})


    con.commit()

def adk():
    cur.execute("SELECT id FROM user where admin = (?);", (1, ))
    result = cur.fetchall()
    con.commit()
    msg = '✨Администраторы беседы: \n'
    for i in result:
        msg += i[0] + '\n'
    vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': msg, 'random_id': 0})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        response = event.text.lower()
        if '!взять' in response and event.chat_id == id_chat_buff and spravka(response):
            antireg(response, event.message_id, event.user_id)
        elif 'вы положили на склад' in response and event.chat_id == id_chat_buff and ('📘' in response or '📕' in response) and spravka(response):
            registration_count(response)
        elif '!малая цена' in response and event.chat_id == id_chat_buff and admin(event.user_id) and spravka(response):
            updatecoast(response)
        elif '!малая удали' in response and event.chat_id == id_chat_buff and admin(event.user_id) and spravka(response):
            delbook(response)
        elif '!малая прайс' in response and event.chat_id == id_chat_buff and spravka(response):
            price()
        elif '!малая иконка' in response and event.chat_id == id_chat_buff and admin(event.user_id) and spravka(response):
            icon(response)
        elif '!малая очки' in response and event.chat_id == id_chat_buff and admin(event.user_id) and spravka(response):
            count_user(response)
        elif '!баланс' in response and event.chat_id == id_chat_buff and spravka(response):
            balance(event.user_id, event.message_id, 1)
        if '!малая админ' in response and event.chat_id == id_chat_buff and event.user_id == 177617355 and spravka(response):
            aaadmin(response)
        elif '!малая рестарт' in response and admin(event.user_id) and spravka(response):
            vk_session.method('messages.send',{'chat_id': id_chat_buff,'message': 'Перезапустила!', 'random_id': 0})
            break
        elif '!общийбаланс' in response and event.chat_id == id_chat_buff and admin(event.user_id) and spravka(response):
            balance(event.user_id, event.message_id, 0)
        elif (response == '!помощь' or response == '!админинфо' or response == '!налогинфо' or response == '!бафинфо' or response == '!общее') and event.chat_id == id_chat_buff:
            dhelp(response)
        elif response == '!админы' and event.chat_id == id_chat_buff and spravka(response):
            adk()
        elif ('!добавьописание' in response or '!измениописание' in response or '!покажиописание' in response) and admin(event.user_id):
            help(event.message)
        elif '!вывести' in response and event.chat_id == id_chat_buff and spravka(response):
            convertgold(response, event.user_id, event.message_id)
        

    
        
