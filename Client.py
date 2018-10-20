import socket
import threading
import pickle

class Client(object):
	def __init__(self, ip, port, username, myGui):
		print('Hello Client')
		self.username=username
		self.count_max_raise = 0
		self.myGui = myGui
		self.my_socket = socket.socket()
		self.adapt_card = {'11': 'jack', '12': 'queen', '13': 'king', '14': 'ace'}
		self.connect(ip,port)

	def load_data(self):
		return pickle.loads(self.my_socket.recv(200))

	def send_data(self,data):
		self.my_socket.send(pickle.dumps(data))

	def connect(self,ip,port):
		self.my_socket.connect((ip, port))
		self.send_data({'name': self.username})
		data = self.load_data()
		print(data)
		if data['status'] == 'ok':
			self.my_id = data['yourid']
			self.myGui.myId = self.my_id
			self.myGui.change_name_user(self.my_id, self.username)
			self.my_thread = threading.Thread(target=self.listener)
			self.my_thread.start()
		else:	
			#тут можно выкидывать какую-нибудь ошибку
			pass
	
	def listener(self):
		while True:
			data_from_server = pickle.loads(self.my_socket.recv(200))
			print(data_from_server)
			if data_from_server['action'] == 'step' and data_from_server['id'] == self.my_id:
				
				for i in self.myGui.player_places:#даем игроку возможность ходить. пока так 
					if i['user']['text'] == self.username:
						i['raise_bet']['state']='normal'
					
				step = self.do_step(data_from_server['id']) #do_step() функция, которая возвращает список из действия играок(1) и суммы(2)
				#self.send_data({'action': 'move', 'move': step[0], 'count': step[1]})
			elif data_from_server['action'] == 'update':
				self.update(data_from_server)
			elif data_from_server['action'] == 'start?':
				self.send_data({'action': 'start?', 'answer': def_invite(data_from_server['players'])})  # def_invite функция, которая предлогает игроку начать игру, возвращает True/False
			elif data_from_server['action'] == 'start_game':
				self.set_bank_of_player(data_from_server['money'])
				self.set_card_on_player(data_from_server['cards'])
				self.send_data({'action': 'ok'})
			elif data_from_server['action'] == 'end_game':
				pass
				
	def update(self,data):
		self.set_bank(data['bank']) #установка у клиента текущего банка
		print(data)
		for player in data['gamers']:
			print(player)
			id = player[0]
			curr_bet = player[1]
			player_bank = player[2]
			
			#self.myGui.change_name_user(id, player[3])# пока так. чтобы у других игроков тоже были имена
			
			self.set_money(id, curr_bet, player_bank)
			self.set_min_raise(data['to_raise']) #становка минимальной суммы для повышения ставки
			self.set_open_cards(data['open_cards'], data['bank'])
			
	def adapt_cards(self, num_card):
		if num_card <= 10:
			return str(num_card)
		else:
			return self.adapt_card.get(str(num_card))

	def set_card_on_player(self, cards):
		card0 = cards[0]
		num_card0 = self.adapt_cards(card0[0])
		suit_card0 = (card0[1])[:-1]
		card1 = cards[1]
		num_card1 = self.adapt_cards(card1[0])
		suit_card1 = (card1[1])[:-1]
		self.myGui.set_card_one_player(self.myGui.getMyId(), suit_card0, num_card0, suit_card1, num_card1)

	def set_bank_of_player(self, money):
		self.myGui.add_bank_player(self.myGui.getMyId(), money)
	
	# curr_bet
	def set_money(self, id, curr_bet, player_money):
		self.myGui.add_bank_player(id, player_money)
		self.myGui.change_bet_player(id, curr_bet)

	def set_min_raise(self, min_bet):
		pass

	def set_open_cards(self, open_cards, bank):
		if len(open_cards) != 0:
			self.myGui.clean_card_on_center()
			for card in open_cards:
				num_card = self.adapt_cards(card[0])
				suit_card = (card[1])[:-1]
				self.myGui.change_croupier(bank, suit_card, num_card)
				
	def step(self,data):
		self.send_data({'action': 'move', 'move': data[0], 'count': data[1]})
		for i in self.myGui.player_places:#даем игроку возможность ходить. пока так 
			if i['user']['text'] == self.username:
				i['raise_bet']['state']='disable'
		
	def do_step(self, id):
		if id == 0:
			return ['raise', 100]
		else:
			return ['call', 100]
		#if self.count_max_raise > 2:
		#	self.count_max_raise = 0
		#	return ['call', 100]
		#else:
		#	self.count_max_raise = self.count_max_raise + 1
		#	return ['raise', 100]

	def set_bank(self,money):
		pass












def def_invite(players):
	if players >= 2:
		return True
	else:
		return False


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

