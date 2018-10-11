import threading
import socket
import pickle
import random
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



class Table:
	def __init__(self):
		self.players={}
		self.count=0 #кол-во игроков
		self.bank=0#сумма всех текущих ставок
		self.min_bet=100
		self.curr_bet=0
		self.round=0
		self.deck=[] #колода
		self.next_card=0 #номер следующей на выдачу карты в списке deck
		self.bigblindid=0
		self.opened_cards=[]
		self.next_id=0
		#создание колоды
		mast=["diamonds","hearts","spades","clubs"]
		rol={10:"jack",11:"queen",12:"king",13:"ace"}
		for i in range(0,4):
			for y in range(1,14):
				if y>10:
					self.deck.append((rol[y],mast[i]))
				else:
					self.deck.append((y,mast[i]))
		#мешаем колоду
		for i in range(0, 52):
			rindex=random.randint(0,51)
			temp=self.deck[i]
			self.deck[i]=self.deck[rindex]
			self.deck[rindex]=temp
	def get_player_by_id(self, id):	
		for i in self.plaeyrs:
			if self.players[i].id==id:
				return self.players[i]
	def update_bank(self,num):
		self.bank=num
	def get_next_id(self):
		u=self.next_id
		self.next_id+=1
		return u;
	def get_count(self):
		return self.count
	def get_bank(sel):
		return self.bank
	def add_player(self, player):
		self.count+=1
		if self.count == 1:
			player.bigblind=True #первый подключившийся игрок сразу помечается как большой блайнд
			self.bigblindid = player.id
		self.players[self.count]=player
		
	def update(self):
		#один игрок сделал шаг и оповещение отсылается всем
		gamers=[]
		for i in self.players:
			gamers.append((players[i].id,players[i].curr_bet,players[i].money))
		#переосмыслить to_rise
		upd={'action':"update",'bank':self.bank,'gamers':gamers,'to_raise':100,'open_cards':self.opened_cards}
		
		for i in players:
			players[i].conn.send(pickle.dumps(upd))
		
	def create_game(self):
		#Если се игроки согласны играть то рассылаем
		for i in self.players:
			if self.players[i].game_status=="ready":
				continue
			data={
				'action':'start_game',
				'cards':self.get_cards(2),
				'bigblind':self.bigblindid,
				'min_money':self.min_bet,
				'money':self.players[i].money
			}
			self.players[i].conn.send(pickle.dumps(data))
			self.players[i].game_status="ready"
	def start_game(self):
		#Доделть:Выбираем кому нужно передать ход и тут же взымаем ставку (та что до начала торгов)
		
		id=0
		for i in self.players:
			if self.players[i].bigblind==True:
				id=self.players[i].id
				break
		for i in self.players:
			self.players[i].game_status="playing"
			self.players[i].conn.send(pickle.dumps({'action':'step','id':id}))
	def next_step(self):
		id=0
		flag=False #False - флаг занят, True - свободен
		#Находим игрока у которого сейчас флаг ходаб снимаем этот флаг и отдаем следующему
		for i in self.players: #
			if self.players[i].game_status=="playing":
				if self.players[i].move==True:
					self.players[i].move=False
					flag==True
				elif flag==True and self.players[i].move==False:
					self.players[i].move=True
					id=self.players[i].id
					break
				
				
		for i in self.players:
			self.players[i].conn.send(pickle.dumps({'action':'step','id':id}))
	def step(self,id,action):
		player=get_player_by_id(id)	
		if player.step==True:
			if action['move']=='call':
				player.curr_bet=self.curr_bet
				player.money-=player.curr_bet
			elif action['move']=='rise':
				player.curr_bet=action['move'].count
				player.money-=player.curr_bet
				self.curr_bet=action['move'].count
			
			update()
			#если все сделали свой ход, то открываем след карту, если нет то передаем следующему ход
			flag=True
			for i in self.players:
				if self.payers[i].curr_bet==self.curr_bet:
					flag=False
					next_step()
					break
			if flag==True:
				open_card()
	def get_cards(self, count):
		cards=[]
		for i in range(0,count):
			cards.append(self.deck[self.next_card])
			self.next_card+=1
		return cards
	def open_card(self):
		for i in self.players:
			self.bank=+self.players[i].curr_bet
			self.players[i].curr_bet=0
			
		self.opened_cards=get_cards(1)
		update()
		

class Player:
	def __init__(self,name,conn,id):
		self.id=id
		self.name=name
		self.conn=conn
		self.money=10000
		self.cards={}
		self.curr_bet=0 #текущая ставка
		self.bigblind=False
		self.game_status="playing"#playing\wait\folded\ready
		self.step=False #ход
	def get_money(self):
		return money
	def get_name(self):
		return name
	

table1=Table() #создаём стол	
def listen(name,conn):
	print("Client connected");
	playerid=table1.get_next_id()
	player=Player(name,conn,playerid)
	table1.add_player(player)
	conn.send( pickle.dumps({'status':'ok', 'yourid':playerid}) ) 
	#если игроков два и более, то расслылать приглашение для начала игры
	if table1.get_count() > 1:
		for i in table1.players:
			table1.players[i].conn.send(pickle.dumps({'action':'start?', 'players': table1.get_count()}))
	while True:
		obj=pickle.loads(conn.recv(200))
		print(obj)
		##for i in listeners.keys():
		if obj['action']=="start?" and obj['answer']==True:
			player.game_status="wait"
			table1.create_game()
		elif obj['action']=="move":
			table1.step(playerid,obj)
		elif obj['action']=="ok":
			check=True
			for i in table1.players:
				if table1.players[i].game_status!="ready":
					check=False
			if check==True:
				table1.start_game();
			 
				
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
		else:
			conn.send(pickle.dumps({'status':'err'}))
			conn.close()
