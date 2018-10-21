import socket
import threading
import pickle

testmode=False

class Client(object):
	def __init__(self):
		print('Hello Client')
		self.username=""
		self.count_max_raise = 0
		self.is_connected=False
		self.my_socket = socket.socket()
		#self.adapt_card = {'11': 'jack', '12': 'queen', '13': 'king', '14': 'ace'} #или тут таки адаптировать
		#Функции =======================
		#или даже типа сигналы
		self.update=0
		self.allow_to_step=0
		self.game_has_begun=0
		self.whose_step=0
		self.end_game=0
		self.invite_to_game=0
		#==============================

	def load_data(self):
		return pickle.loads(self.my_socket.recv(500))
		
	def send_data(self,data):
		self.my_socket.send(pickle.dumps(data))

	def connect(self,ip,port,username):
		self.my_socket.connect((ip, port))
		self.send_data({'name': username})
		data = self.load_data()
		print(data)
		if data['status'] == 'ok':
			self.my_id = data['yourid']
			self.username=username
			self.my_thread = threading.Thread(target=self.listener)
			self.is_connected=True
			self.my_thread.start()
		else:	
			#тут можно выкидывать какую-нибудь ошибку
			pass
			
	def get_id(self):
		return self.my_id
		
	def get_username(self):
		return self.username
		
	def listener(self):
		while True:
			data_from_server = pickle.loads(self.my_socket.recv(500))
			print(data_from_server)
			if data_from_server['action'] == 'step':# and data_from_server['id'] == self.my_id:
				if data_from_server['id'] == self.my_id:
					self.allow_to_step()
				self.whose_step(data_from_server)
				if testmode:				
					step = self.do_step(data_from_server['id']) #do_step() функция, которая возвращает список из действия играок(1) и суммы(2)
					self.send_data({'action': 'move', 'move': step[0], 'count': step[1]})
			elif data_from_server['action'] == 'update':
				self.set_bank(data_from_server['bank']) #установка у клиента текущего банка
				self.players=data_from_server['gamers']
				self.update(data_from_server)#это типа сигнал
			elif data_from_server['action'] == 'end':
				self.end_game(data_from_server)
			elif data_from_server['action'] == 'start?':
				 self.invite_to_game();
			elif data_from_server['action'] == 'start_game':
				self.game_has_begun(data_from_server)
				self.send_data({'action': 'ok'})
			elif data_from_server['action'] == 'end_game':
				pass
				
	def start_game(self):
		self.send_data({'action': 'start?', 'answer': True})
		
	def step(self,data):
		self.send_data({'action': 'move', 'move': data[0], 'count': data[1]})

	def do_step(self, id):
		if id == self.my_id:
			return ['raise', 100]
		
		#if self.count_max_raise > 2:
		#	self.count_max_raise = 0
		#	return ['call', 100]
		#else:
		#	self.count_max_raise = self.count_max_raise + 1
		#	return ['raise', 100]

	def set_bank(self,money):
		pass
	















if __name__ == '__main__':
	pass
	#a = Client('localhost', 8011, 'Sergey')

## name of cards 'suit', 'ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4''3''2''j_red', 'j_black'
## suit of cards (FOLDERS) -'suit', 'joker', 'club', 'diamond', 'heart', 'spade'
#
## case of play
#
##change cards of first player
#my_gui.set_card_one_player(1, 'diamond', 'queen', 'club', '2')
##add card from croupie
#cards_center = my_gui.change_croupier(100, 'joker', 'j_red')
##add card from croupie
##cards_center = my_gui.change_croupier(1000, 'club', 'jack')
##change state of button first player
#my_gui.change_button_player(1, True)
##my_gui.change_button_player(1, FALSE) # example for disabled button for a player
#
##cases of player
#my_gui.change_name_user(1, "boris")
#
#my_gui.add_bank_player(1, 100)
#
#my_gui.change_bet_player(1, 10)

