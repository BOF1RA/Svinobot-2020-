# -*- coding: utf-8 -*-
import vk_api,random,requests,traceback,glob,time,json
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors
from threading import Thread
tkn = "f35356bbcc6928f04a42eb0846891eacf79b509e44046ab2da7bc079ab6a814378b24a12869199a369ce7" #ваш токен
idvk = 560873211 #ваш айди
adminki = [560873211] #пользователи которые могут управлять командами
ignorelist = [560873211] #игнор пользователей
conf = [] #игнор конф
title1 = "@basedata.json" #название беседы
photo = "photo.jpg" #фото для смены аватарки конфы
captch = "ваш токен с anti-captcha.com" #антикаптча
def captcha_handler(captcha):
    key = ImageToTextTask.ImageToTextTask(anticaptcha_key=captch, save_format='const') \
            .captcha_handler(captcha_link=captcha.get_url())
    return captcha.try_again(key['solution']['text'])

vk_session = vk_api.VkApi(token=tkn, captcha_handler=captcha_handler)
vk = vk_session.get_api()


def friends(): #эта функция автоматически принимает в друзья
    while True:
        try:
            zayavki=vk.friends.getRequests(v=5.92)['items']
            for u in zayavki:
                vk.friends.add(user_id=u)
        except:
            pass
            time.sleep(10)
        try:
            zayavki1=vk.friends.getRequests(out="true")['items']
            for u in zayavki1:
                vk.friends.delete(user_id=u)
        except:
            pass
            time.sleep(10)
def msgs(): #эта функция отправляет сообщения
    while True:
        def captcha_handler(captcha):
            key = ImageToTextTask.ImageToTextTask(anticaptcha_key=captch, save_format='const') \
                    .captcha_handler(captcha_link=captcha.get_url())
            return captcha.try_again(key['solution']['text'])
        vk_session = vk_api.VkApi(token=tkn, captcha_handler=captcha_handler)
        vk = vk_session.get_api()
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.user_id != idvk:
                    peer_id = event.peer_id
                    user_id = event.user_id
                    b=event.text
                    c=random.choice([1,1,1,2])
                    if c == 1 and event.user_id > 0 and event.user_id != idvk:
                        if peer_id > 2000000000 and not event.chat_id in conf and not event.user_id in ignorelist:
                            f = open('фразы.txt',encoding='utf-8', errors='ignore')
                            data1 = f.read()
                            msg = random.choice(data1.split('\n'))
                            g = open('фотки.txt',encoding='utf-8', errors='ignore')
                            data2 = g.read()
                            photo = random.choice(data2.split('\n'))
                            vk.messages.setActivity(peer_id=peer_id,type='typing')
                            time.sleep(random.randint(10,16))
                            vk.messages.send(peer_id=peer_id,random_id=random.randint(100000,999999),message=msg,attachment=random.choice([str(photo),'','','','']))
                        elif peer_id < 2000000000 and user_id > 0:
                            if b[0:8] == "https://":
                                print(vk.messages.joinChatByInviteLink(link=b))
                            else:
                                if not event.user_id in ignorelist:
                                    f = open('фразы.txt',encoding='utf-8', errors='ignore')
                                    data = f.read()
                                    msg = random.choice(data.split('\n'))
                                    g = open('фотки.txt',encoding='utf-8', errors='ignore')
                                    data2 = g.read()
                                    photo = random.choice(data2.split('\n'))
                                    vk.messages.setActivity(peer_id=peer_id,type='typing')
                                    time.sleep(random.randint(10,16))
                                    vk.messages.send(peer_id=peer_id,random_id=random.randint(100000,999999),message=msg,attachment=random.choice([str(photo),'','','','']))
                    if c == 2 and event.user_id > 0:
                        if peer_id > 2000000000 and not event.chat_id in conf and not event.user_id in ignorelist:
                            a=vk.docs.getMessagesUploadServer(type='audio_message',peer_id=user_id)['upload_url']
                            try:
                                say=random.choice(glob.glob("voice/*.ogg"))
                            except:
                                say=random.choice(glob.glob("voice/*.mp3"))
                            img = {'file': ('a.mp3', open(say, 'rb'))}
                            response = requests.post(a, files=img)
                            result = json.loads(response.text)['file']
                            owner=vk.docs.save(file=result)['audio_message']['owner_id']
                            document=vk.docs.save(file=result)['audio_message']['id']
                            send = 'doc'+str(owner)+'_'+str(document)
                            vk.messages.setActivity(peer_id=peer_id,type="audiomessage")
                            time.sleep(random.randint(1,3))
                            vk.messages.send(random_id=random.randint(100000,999999),attachment=send,peer_id=peer_id)
                        elif peer_id < 2000000000:
                            if b[0:8] == "https://":
                                print(vk.messages.joinChatByInviteLink(link=b))
                            else:
                                if not event.user_id in ignorelist:
                                    a=vk.docs.getMessagesUploadServer(type='audio_message',peer_id=user_id)['upload_url']
                                    try:
                                        say=random.choice(glob.glob("voice/*.ogg"))
                                    except:
                                        say=random.choice(glob.glob("voice/*.mp3"))
                                    img = {'file': ('a.mp3', open(say, 'rb'))}
                                    response = requests.post(a, files=img)
                                    result = json.loads(response.text)['file']
                                    owner=vk.docs.save(file=result)['audio_message']['owner_id']
                                    document=vk.docs.save(file=result)['audio_message']['id']
                                    send = 'doc'+str(owner)+'_'+str(document)
                                    vk.messages.setActivity(peer_id=peer_id,type="audiomessage")
                                    time.sleep(random.randint(10,16))
                                    vk.messages.send(random_id=random.randint(100000,999999),attachment=send,peer_id=peer_id)
                break
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
def bot(): #эта функция активирует команды админов
    while True:
        try:
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                try:
                    if event.user_id in adminki:
                        if event.text.lower() == "друзья!":
                            class dr(Thread):
                                def __init__(self,event):
                                    Thread.__init__(self)
                                    self.event = event
                                def run(self):
                                    ct=requests.get("https://api.vk.com/method/friends.get?access_token="+tkn+"&v=5.92&user_id=0").json()["response"]["items"]
                                    ln=len(ct)
                                    k=0
                                    while k != (ln//25)+1:
                                        try:
                                            x = []
                                            x2=0
                                            while x2 != 25:
                                                try:
                                                    x.append(ct[x2])
                                                except:
                                                    pass
                                                x2+=1
                                            x2=0
                                            while x2 != 25:
                                                try:
                                                    ct.pop(x2)
                                                except:
                                                    pass
                                                x2+=1
                                            scrp='var b = '+str(x)+';var c = 24;while (c !=-1){API.messages.addChatUser({"chat_id":'+str(self.event.chat_id)+',user_id:b[c]});c=c-1;};'
                                            vk.execute(code=scrp)
                                        except:
                                            pass
                                        k+=1
                            dr(event).start()
                        elif event.text.lower() == "пендосы!":
                            vk.messages.removeChatUser(chat_id=event.chat_id,user_id=idvk)
                except:
                    pass
                if event.type_id == VkChatEventType.USER_JOINED:
                    class invite(Thread):
                        def __init__(self,event):
                            Thread.__init__(self)
                            self.event = event
                        def run(self):
                            a=self.event.info['user_id']
                            chat_id = self.event.chat_id
                            peer_id = self.event.peer_id
                            if a == idvk:
                                try:
                                    vk.messages.editChat(chat_id=chat_id,title=title1)
                                    j=vk.photos.getChatUploadServer(chat_id=chat_id,crop_x=10,crop_y=25)['upload_url']
                                    img = {'photo': ("photo.jpg", open("photo.jpg", 'rb'))}
                                    response = requests.post(j, files=img)
                                    result = json.loads(response.text)['response']
                                    vk.messages.setChatPhoto(file=result)
                                except:
                                    pass
                                try:
                                    vk.messages.unpin(peer_id=peer_id)
                                except:
                                    pass
                                usrlist=[]
                                for x in usrlist:
                                    try:
                                        vk.messages.addChatUser(chat_id=chat_id,user_id=x)
                                    except:
                                        pass
                    invite(event).start()
                elif event.type_id == VkChatEventType.MESSAGE_PINNED:
                    class pinn(Thread):
                        def __init__(self,event):
                            Thread.__init__(self)
                            self.event = event
                        def run(self):
                            peer_id=self.event.peer_id
                            r=int(vk.messages.getHistory(peer_id=peer_id,count=1)['items'][0]['from_id'])
                            if r != idvk and r > 0 and not r in ignorelist:
                                vk.messages.unpin(peer_id=peer_id)
                    pinn(event).start()
                elif event.type_id == VkChatEventType.PHOTO:
                    class fotka(Thread):
                        def __init__(self,event):
                            Thread.__init__(self)
                            self.event = event
                        def run(self):
                            chat_id = self.event.chat_id
                            peer_id = self.event.peer_id
                            r=int(vk.messages.getHistory(peer_id=peer_id,count=1)['items'][0]['from_id'])
                            if r != idvk and r > 0 and not r in ignorelist:
                                a=vk.photos.getChatUploadServer(chat_id=event.chat_id,crop_x=10,crop_y=25)['upload_url']
                                img = {'photo': ("photo.jpg", open("photo.jpg", 'rb'))}
                                response = requests.post(a, files=img)
                                result = json.loads(response.text)['response']
                                vk.messages.setChatPhoto(file=result)
                    fotka(event).start()
                elif event.type_id == VkChatEventType.TITLE:
                    class titol(Thread):
                        def __init__(self,event):
                            Thread.__init__(self)
                            self.event = event
                        def run(self):
                            chat_id = self.event.chat_id
                            peer_id = self.event.peer_id
                            r=int(vk.messages.getHistory(peer_id=peer_id,count=1)['items'][0]['from_id'])
                            if r != idvk and r > 0 and not r in ignorelist:
                                vk.messages.editChat(chat_id=chat_id,title=title1)
                    titol(event).start()
        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
class f(Thread):
    def __init__(self,a):
        Thread.__init__(self)
        self.a = a
    def run(self):
        print(self.a)
        friends()
class m(Thread):
    def __init__(self,a):
        Thread.__init__(self)
        self.a = a
    def run(self):
        print(self.a)
        msgs()
class b(Thread):
    def __init__(self,a):
        Thread.__init__(self)
        self.a = a
    def run(self):
        print(self.a)
        bot()

f("Проверка друзей запущена!").start()
m("Отправка сообщений запущена!").start()
b("Переименовывание кф запущено!").start()
