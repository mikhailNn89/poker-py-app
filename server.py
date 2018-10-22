import threading
import socket
import pickle
import random
import time

lim_players_for_run = 2

"""
diamonds - бубны
hearts - червы
spades - пики
clubs - трефы
ace - туз
king 
queen
jack - валет
"""
#Исправить проеблему, когда в начале игры по два раза отсылается информация первом ходе
#Добавить распознавание комбинаций
#Добавить обработу ошибок и неверно введенных данных
#Передача блайнда
#Добавить завершение игры 
#Доделать определение комбинаций
#Добавить перевод игрока в статус folded
#Названия карт передаются текстом, в должны цифрой

#При call вычитает из денег клиента его ставку + максимальную ставку
#Ошибки;игра начинается без получения "ок" от клиентов
#        один пользователь может добавиться несколько раз
class Player:
    def __init__(self,id,name,conn):
        self.id=id
        self.name=name
        self.conn=conn
        self.money=10000
        self.cards=[]
        self.curr_bet=0 #текущая ставка
        self.bigblind=False
        self.game_status=""#playing\wait\folded\ready
        self.step=False #ход
    def get_money(self):
        return self.money
    def get_name(self):
        return self.name


class Table:
    def __init__(self):
        self.players=[]
        self.count=0 #кол-во игроков
        self.bank=0
        self.game_started=False
        self.is_updating=False
        self.min_bet=100
        self.curr_bet=0
        self.round=0 #торговый раунд
        self.deck=[] #колода
        self.next_card=0 #номер следующей на выдачу карты в списке deck
        self.bigblindid=0
        self.opened_cards=[]
        self.curr_step_pid=0 #id игрока, которые в данный момент может делать ход 
        self.next_id=0 #id, который будет выдан новому игроку
        self.combinations={#пара "название_комбинации":ее_вес
            "royal_flush":10,
            "straight_flush":9,
            "quads":8, #каре
            "full_house":7,
            "flush":6,
            "straight":5,
            "set":4,
            "two_pairs":3,
            "one_pair":2,
            "high_card":1
        } 
        #создание колоды
        mast=["diamonds","hearts","spades","clubs"]
        #просто памятка rol={11:"jack",12:"queen",13:"king",14:"ace"}
        for i in range(0,4):
            for y in range(2,15):
                self.deck.append((y,mast[i]))
        self.mix_deck()
    """
    add_player(self, name, conn) - возвращает ссылку на добавленного игрока
    """        
#==================================================================================
    def get_count(self):
        return self.count
        
    def get_bank(sel):
        return self.bank


#==================================================================================        
    def mix_deck(self):
        #мешаем колоду
        for i in range(0, 52):
            rindex=random.randint(0,51)
            temp=self.deck[i]
            self.deck[i]=self.deck[rindex]
            self.deck[rindex]=temp
            
    def add_player(self, name, conn):
        player=Player(self.next_id,name,conn)
        self.players.append(player)
        self.next_id+=1
        self.count+=1
        return player
        
    def send_all(self,data):
        for player in self.players:
            self.send(player,data)
            
    def send(self,player,data):
        player.conn.send(pickle.dumps(data))

    def check_status(self,status,player):
        for player in self.players:
            print(1,player.game_status,status,player.game_status!=status)
            if player.game_status!=status:
                return False
                #break
        return True
        
    def wait_to_play(self,player):
        player.game_status="wait"
        if self.check_status("wait",player):
            print("Create")
            self.create_game()
    
    def ready_to_play(self,player):
        player.game_status="playing"
        if self.check_status("playing",player):#все ли игроки получили начальные данные и готовы играть
            self.start_game()
                
    def update(self):
        #один игрок сделал шаг и оповещение отсылается всем
        if self.is_updating==False: #т.к вызывалось слишко часто и бились данные.пока так
            self.is_updating=True
            gamers=[]
            for player in self.players:
                gamers.append((player.id,player.curr_bet,player.money,player.name))
            #переосмыслить to_rise. это поле не нужно?
            upd={'action':"update",'bank':self.bank,'gamers':gamers,'to_raise':100,'open_cards':self.opened_cards}
            self.send_all(upd)
            self.is_updating=False

    def create_game(self):
        #Если все игроки готовы играть, то рассылаем начальные данные
        #вынести выбор блайндов в отдельную функцию?
        self.bigblindid = self.players[0].id
        for player in self.players:
            if player.game_status!="ready":
                player.cards = self.get_cards(2)
                data = {
                    'action':'start_game',
                    'cards':player.cards,
                    'bigblind':self.bigblindid,
                    'min_money':self.min_bet,
                    'money':player.money
                }
                self.send(player,data)
                player.game_status = "ready"
                print(player.name, data)
                
    def start_game(self):
        #Находим игрока с ББ, взымаем с него минимальную сттавку(та что до начала торгов) и передаем ход другому игроку
        if self.round==1:#пока костыль т.к вызывалось несколько раз
            return 0
        self.round=1
        for player in self.players:
            if player.id==self.bigblindid:
                player.curr_bet=self.min_bet
                self.curr_bet=player.curr_bet
                player.money-=player.curr_bet
                curr_step_pid=id=player.id
        print("Game started")
        self.game_started=True
        self.update()
        self.next_step()
    
    def next_step(self):
        #ход передается просто по кругу или каждый раунд один и тот же игрок?
        i=0
        flag=False
        while True:
            if self.players[i].game_status=="playing":
                if self.players[i].id==self.curr_step_pid:
                    flag=True
                elif flag==True:
                    self.curr_step_pid=self.players[i].id
                    break
            if i==len(self.players)-1:
                i=0
            else:
                i+=1
        print("Ожидается ход игрока:",self.curr_step_pid)
        self.send_all({'action': 'step', 'id': self.curr_step_pid})
    
    def step(self,player,action):
        print("step",action['move'],action['move']=='raise')
        if player.id==self.curr_step_pid:#если у игрока есть право на ход то:
            if action['move']=='call':
                player.money-=(self.curr_bet-player.curr_bet)
                player.curr_bet=self.curr_bet
            elif action['move']=='raise':
                player.money-=action['count']
                player.curr_bet+=action['count']
                if player.curr_bet > self.curr_bet:
                    self.curr_bet = player.curr_bet
            elif action['move']=='fold':
                player.game_status='folded'
                self.bank+=player.curr_bet
                player.curr_bet=0
            elif action['move']=='check':
                pass
            else:
                return 1 #выставь нормальную обработку ошибок, Ошибка: вместо raise передавалось rise, а игра продолжалась
                
    def calc_bank(self):
        for player in self.players:
            if player.game_status=="playing":
                self.bank+=player.curr_bet
                player.curr_bet=0
        self.curr_bet=0
                
    def next_round(self):
        self.calc_bank()
        if self.round==4:
            #self.update()
            self.end_game()
        else:
            if self.round==1:
                self.opened_cards+=self.get_cards(3)
            elif self.round<4:
                self.opened_cards+=self.get_cards(1)
            self.round+=1
            self.update()
            self.next_step()
            print("Начало раунда:",self.round)
            
    def check_bets(self):
        for player in self.players:
            print("curr_bet",player.curr_bet,self.curr_bet)
            if player.curr_bet!=self.curr_bet:
                return False
        return True

    def end_game(self):
        self.round=0
        #Проверяем комбинации, определяем победителя. Их может быть несколько?
        max_cmbn="high_card"
        plr=0 #игрок
        for player in self.players:
            cmbn=self.check_combination(player.cards+self.opened_cards)
            if self.combinations[cmbn]>=self.combinations[max_cmbn]:
                max_cmbn=cmbn
                plr=player
        print(plr.name,max_cmbn)
        plr.money=self.bank            
        data={
            'action':'end',
            'players':[(plr.id,plr.cards+self.opened_cards)],
            'winners':[plr.id,plr.name] ,
            'combination':max_cmbn
        }
        
        
        print("end game")
        self.bank=0    
        dmp=pickle.dumps(data)
        udmp=pickle.loads(dmp)
        print(data, dmp, udmp)
        #time.sleep(3) 
        self.send_all(data)
    
    def get_cards(self, count):
        cards=[]
        for i in range(0,count):
            cards.append(self.deck[self.next_card])
            self.next_card+=1
        return cards
##################################################################
####################Проверка комбинаций###########################
##################################################################

    def check_combination(self,lsp):
        masti={
            "hearts":[],
            "spades":[],
            "diamonds":[],
            "clubs":[]
        }
        pair={}
        combination=""
        for i in range(0,len(lsp)):
            masti[lsp[i][1]].append(lsp[i][0])
            if lsp[i][0] in pair:
                pair[lsp[i][0]]+=1
            else:
                pair[lsp[i][0]]=1
        if self.is_royal_flush(masti):
            combination="royal_flush"
        elif self.is_straight_flush(masti):
            combination="straight_flush"
        elif self.is_quads(pair):
            combination="quads"
        elif self.is_full_house(pair):
            combination="full_house"
        elif self.is_flush(masti):
            combination="flush"
        elif self.is_straight(masti):
            combination="straight"
        elif self.is_set(pair):
            combination="set"
        elif self.is_two_pairs(pair):
            combination="two_pairs"
        elif self.is_one_pair(pair):
            combination="one_pair"
        else:
            combination="high_card"#is_high_card(lsp))        
        return combination
            
    def is_royal_flush(self,masti):
        royal_flush=False
        for i in masti:
            if len(masti[i])>=5:
                masti[i].sort()
                masti[i].reverse()
                num=masti[i][0]
                ls=list(set(masti[i]))
                if num==14:
                    royal_flush=True
                for y in range(1,5):#тут нужно просматривать только первыу пять карт а не все
                    if num-ls[y]!=1:
                        royal_flush=False
                        break
                    else:
                        num=ls[y]
        return royal_flush

    def is_straight_flush(self,masti):
        straight_flush=False
        for i in masti:
            if len(masti[i])>=5:
                masti[i].sort()
                masti[i].reverse()
                num=masti[i][0]
                ls=list(set(masti[i]))
                for y in range(1,5):#тут нужно просматривать только первыу пять карт а не все
                    if num-ls[y]!=1:
                        straight_flush=False
                        break
                    else:
                        straight_flush=True
                    num=ls[y]
        return straight_flush
                
    def is_quads(self,pair):
        for i in pair:
            if pair[i]==4:
                return True
        return False
            
    def is_full_house(self,pair):
        return self.is_one_pair(pair) and self.is_set(pair)

    def is_flush(self,masti):
        for i in masti:
            if len(masti[i])>=5:
                return True
        return False
            
    def is_straight(self,masti):#переписать!
        ls=[]
        for i in masti:
            ls+=masti[i]
        #ls.sort()
        ls=list(set(ls))#тут происходит сортировка
        num=ls[0]
        straight=True
        for y in range(1,5):#тут нужно просматривать только первыу пять карт а не все
            print(ls[y],num)
            if ls[y]-num!=1:
                straight=False
                break
            num=ls[y]
        return straight
            
    def is_set(self,pair):
        for i in pair:
            if pair[i]==3:
                return True
        return False

    def is_two_pairs(self,pair):
        count=0
        for i in pair:
            if pair[i]==2:
                count+=1
        if count==2:
            return True
        else:
            return False
        
    def is_one_pair(self,pair):
        for i in pair:
            if pair[i]==2:
                return True
        return False

    def is_high_card(self,ls):
        imax=0
        card=()
        for i in ls:
            if i[0]>imax:
                imax=i[0]
                card=i
        return card
    
    def abort_game(self):
        self.count=0
        self.bank=0
        self.game_started=False
        self.curr_bet=0
        self.round=0
        self.next_card=0 #номер следующей на выдачу карты в списке deck
        self.bigblindid=0
        self.opened_cards=[]
        self.curr_step_pid=0
table1=Table() #создаём стол    
def listen(name,conn):
    print("Client connected:",name)
    player=table1.add_player(name, conn)
    try:
        table1.send(player, {'status':'ok', 'yourid':player.id}) 
        #если игроков два и более, то расслылать приглашение для начала игры
        if table1.get_count() >= lim_players_for_run:
            table1.send_all({'action':'start?', 'players': table1.get_count()})
        while True:
            obj=pickle.loads(conn.recv(200))
            print(obj)
            #Все проверки должны быть тут
            for i in threads:
                if player.conn!=i:    
                    threads[i].acquire(blocking=True)
            
            if obj['action']=="move" and table1.game_started:
                table1.step(player,obj)
                #если ставки всех игроков одинаковые, то считаем банк и начинаем новый раунд торгов. если нет, то передаём ход дальше
                if table1.check_bets()==False:
                    table1.update()
                    table1.next_step()
                else:
                    table1.next_round()
            elif obj['action']=="start?" and obj['answer']==True:
                table1.wait_to_play(player)
            elif obj['action']=="ok":
                print(player.name,obj)
                table1.ready_to_play(player)
            
            for i in threads:
                if player.conn!=i:
                    threads[i].release()
            
    except(ConnectionResetError):
        table1.abort_game()
        for i in range(0,len(table1.players)-1):
            if player.id==table1.players[i].id:
                del table1.players[i]
        print("Соединение с клиентом потеряно",player.name)
threads={}
if __name__=="__main__":
    my_socket=socket.socket()
    my_socket.bind(("",8011))
    my_socket.listen(5)
    while True:
        conn,ip_addr=my_socket.accept()
        name=pickle.loads(conn.recv(200))
        if len(name['name'])<10:
            new_thread=threading.Thread(target=listen, args=(name["name"],conn))
            new_thread.start()
            threads[conn]=threading.Lock()
        else:
            conn.send(pickle.dumps({'status':'err'}))
            print('Closing ----------------------')
            conn.close()
