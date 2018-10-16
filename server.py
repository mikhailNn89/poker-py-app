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
		return money
	def get_name(self):
		return names


class Table:
	def __init__(self):
		self.players=[]
		self.count=0 #кол-во игроков
		self.bank=0
		self.min_bet=100
		self.curr_bet=0
		self.round=0 #торговый раунд
		self.next_round=False #можно ли начинать следующий раунд торгов. когда все ставки равны и пр.
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
		rol={11:"jack",12:"queen",13:"king",14:"ace"}
		for i in range(0,4):
			for y in range(1,15):
					self.deck.append((y,mast[i]))
		self.mix_deck()
	"""
	get_player_by_id() - возвращает объект Player
	add_player(self, name, conn) - возвращает ссылку на добавленного игрока
	"""		
#==================================================================================
	def get_count(self):
		return self.count
		
	def get_bank(sel):
		return self.bank

	def get_player_by_id(self, id):	
		for player in self.players:
			if player.id==id:
				return player
#==================================================================================		
	def mix_deck(self):
		#мешаем колоду
		for i in range(0, 56):
			rindex=random.randint(0,55)
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
	#использовать блокировку потоков тут?
		flag=True
		for player in self.players:
			print(1,player.game_status,status,player.game_status!=status)
			if player.game_status!=status:
				flag=False
				break
		return flag
		
	def wait_to_play(self,player):
		player.game_status="wait"
		if self.check_status("wait",player):
			print("Create?")
			self.create_game()
	
	def ready_to_play(self,player):
		player.game_status="ready"
		if self.check_status("ready",player):#все ли игроки получили начальные данные и готовы играть
			print("ready start")
			self.start_game()
				
	def update(self):
		#один игрок сделал шаг и оповещение отсылается всем
		gamers=[]
		for player in self.players:
			gamers.append((player.id,player.curr_bet,player.money))
		#переосмыслить to_rise
		upd={'action':"update",'bank':self.bank,'gamers':gamers,'to_raise':100,'open_cards':self.opened_cards}
		self.send_all(upd)

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
			player.game_status="playing"
		print("Game started")
		self.update()
		self.next_step();
	
	def next_step(self):
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
		self.send_all({'action':'step','id':self.curr_step_pid})
	
	def step(self,id,action):
		#Тут нужно проянить , что передается в count`e от клиента
		print("step",action['move'],action['move']=='rise')
		player=self.get_player_by_id(id)	
		if player.id==self.curr_step_pid:#если у игрока есть право на ход то:
			if action['move']=='call':
				player.money-=(self.curr_bet-player.curr_bet)
				player.curr_bet=self.curr_bet
			elif action['move']=='rise':
				self.curr_bet+=action['count']
				if player.curr_bet==0:
					player.money-=self.curr_bet
				else:
					player.money-=action['count']
				player.curr_bet=self.curr_bet
			elif action['move']=='fold':
				player.game_status='folded'
				#ставка складывается в банк и зануляется тут?
				#self.bank+=player.curr_bet
				#player.curr_bet=0
				
			self.update()
			all_eq=True
			#если ставки всех игроков одинаковые, то считаем банк и начинаем новый раунд торгов. если нет, то передаём ход дальше
			for player in self.players:
				print("curr_bet",player.curr_bet,self.curr_bet)
				if player.curr_bet!=self.curr_bet:
					all_eq=False
					self.next_step()
					break
			#складываем ставки в банк, обнуляем ставки игроков, открываем карты
			if all_eq==True:
				for player in self.players:
					#Надо:Проверка, чтобы не обсчитывать игроков, которые вышли
					self.bank+=player.curr_bet
					player.curr_bet=0
				if self.round==4:
					self.update()
					self.end_game()
				else:
					if self.round==1:
						self.opened_cards=self.get_cards(3)
					elif self.round<4:
						self.opened_cards=self.get_cards(1)
					self.update()
					self.next_step()
					self.round+=1
				
	def end_game():
		self.round=0
		#Проверяем комбинации, определяем победителя. Их может быть несколько?
		max_cmbn=""
		plr=0 #игрок
		for player in self.players:
			cmbn=check_combination(player.cards+self.opened_cards)
			if self.combinations[cmbn]>self.combinations[max_cmbn]:
				max_cmbn=cmbn
				plr=player
		plr.money=self.bank			
		data={
			'action':'end',
			'players':[(plr.id,plr.cards+self.opened_cards)],
			'winners':[plr.id] ,
			'combination':max_cmbn
		}
		self.bank=0	
		#self.send_all(data)
	
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
			"heart":[],
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
		if is_royal_flush(masti):
			print("is_royal_flush")
		elif is_straight_flush(masti):
			print("is_straight_flush")
		elif is_quads(pair):
			print("is_quads")
		elif is_full_house(pair):
			print("is_full_house")
		elif is_flush(masti):
			print("is_flush")
		elif is_straight(masti):
			print("is_straight")
		elif is_set(pair):
			print("is_set")
		elif is_two_pairs(pair):
			print("is_two_pairs")
		elif is_one_pair(pair):
			print("is_one_pair")
		else:
			print("oldcard")#is_high_card(lsp))		
		
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
		return is_one_pair(pair) and is_set(pair)

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

table1=Table() #создаём стол	
def listen(name,conn):
	print("Client connected:",name);
	player=table1.add_player(name, conn)
	try:
		table1.send(player, {'status':'ok', 'yourid':player.id}) 
		#если игроков два и более, то расслылать приглашение для начала игры
		if table1.get_count() > 1:
			table1.send_all({'action':'start?', 'players': table1.get_count()})
		while True:
			obj=pickle.loads(conn.recv(200))
			print(obj)
			#Все проверки должны быть тут
			for i in threads:
				if player.conn!=i:	
					threads[i].acquire(blocking=True)
			
			if obj['action']=="move":
				table1.step(player.id,obj)
			elif obj['action']=="fold":
				print("Fold")
			elif obj['action']=="start?" and obj['answer']==True:
				table1.wait_to_play(player)
			elif obj['action']=="ok":
				table1.ready_to_play(player)
			
			for i in threads:
				if player.conn!=i:
					threads[i].release()
			
	except(ConnectionResetError):
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
			threads[conn]=threading.Lock();
		else:
			conn.send(pickle.dumps({'status':'err'}))
			conn.close()
