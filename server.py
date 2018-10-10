import threading
import socket
import pickle
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
		self.bank=0
		self.min_bet=100
		self.curr_bet=0
		self.round=0
		self.deck=[]
		self.opened_cards=[]
		#создание колоды
		mast=["diamonds","hearts","spades","clubs"]
		rol={10:"jack",11:"queen",12:"king",13:"ace"}
		for i in range(0,4):
			for y in range(1,14):
				if y>10:
					self.deck.append((rol[y],mast[i]))
				else:
					self.deck.append((y,mast[i]))
	def update_bank(self,num):
		self.bank=num
	def get_count(self):
		return self.count
	def get_bank(sel):
		return self.bank
	def add_player(self, player):
		self.count+=1
		if self.count == 1:
			player.bigblind=True #первый подключившийся игрок сразу помечается как большой блайнд
		self.players[self.count]=player
		
	def update(self,conn, obj):
		#один игрок сделал шаг и оповещение отсылается всем
		gamers=[]
		for i in players:
			gamers.append((players[i].get_name(),players[i].get_money()))
		upd={'action':"update",'bank':bank,'gamers':gamers,'to_raise':100,'open_cards':opened.cards}
		"""
		if obj.move=="call":
			
		elif obj.move=="raise":
			last_rise=obj.count
		elif obj.move=="check":
			
		elif obj.move=="fold":
			#выйти из игры
		elif obj.move=="bet":
		"""
		for i in players:
			if conn!= players[i].conn:
				players[i].conn.send(pickle.dumps(upd))
		
	def create_game(self):
		#тут рандом
		for i in players:
			cards=[(1,'hearts'),(3,'spades')]
			data={
				'action':start_game,
				'cards':cards,
				'bigblind':players[i].bigblind,
				'min_money':100,
				'money':10000
			}
			player[i].conn.send(pickle.dumps(update))
		

class Player:
	def __init__(self,name,conn):
		self.name=name
		self.conn=conn
		self.money=10000
		self.cards={}
		self.curr_bet=0 #текущая ставка
		self.bigblind=False
		self.game_status="playing"#playing\wait\fold
		self.move=False #ход
	def get_money(self):
		return money
	def get_name(self):
		return name
	

table1=Table() #создаём стол	
def listen(name,conn):
	print("Client connected");
	table1.add_player(Player(name,conn))
	conn.send( pickle.dumps({'status':'ok', 'count':table1.get_count()}) ) 
	#если игроков два и более, то расслылать приглашение для начала игры
	if table1.get_count() > 1:
		for i in table1.players:
			players[i].conn.send(pickle.dumps({'action':'start?', 'players': table1.get_count()}))
	while True:
		#должен приходить объект
		obj=pickle.loads(conn.recv(200))
		print(obj)
		##for i in listeners.keys():
		if obj.action=="start" and obj.answer==True:
			#player.game_status="wait"
			#create_game(player)
			print(obj)
		elif obj.action=="move":
			table1.step(conn, obj)
		elif obj.action=="ok":
			check=True
			for i in table1.players:
				if table1.players[1]!="playing":
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
