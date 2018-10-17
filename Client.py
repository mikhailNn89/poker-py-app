import socket
import threading
import pickle

class Client(object):
    def __init__(self, ip, port, username, myGui):
        print('Hello Client')
        self.myGui = myGui
        self.my_socket = socket.socket()
        self.my_socket.connect((ip, port))
        self.my_socket.send(pickle.dumps({'name': username}))
        self.adapt_card = {'11': 'jack', '12': 'queen', '13': 'king', '14': 'ace'}
        data = pickle.loads(self.my_socket.recv(200))
        if data['status'] == 'ok':
            self.my_id = data['yourid']
            myGui.myId = self.my_id
            myGui.change_name_user(self.my_id, username)
            self.my_thread = threading.Thread(target=self.wait_game)
            self.my_thread.start()

    def game_listener(self, cards, bigblind, min_money, money):
        self.my_socket.send(pickle.dumps({'action': 'ok'}))
        while True:
            data_from_server = pickle.loads(self.my_socket.recv(200))
            if data_from_server['action'] == 'step' and data_from_server['id'] == self.my_id:
                step = do_step() #do_step() функция, которая возвращает список из действия играок(1) и суммы(2)
                self.my_socket.send(pickle.dumps({'action': 'move', 'move': step()[0], 'count': step()[1]}))
            elif data_from_server['action'] == 'update':
                set_bank(data_from_server['bank']) #установка у клиента текущего банка
                for player in data_from_server['gamers']:
                    set_money(player[0], player[1])
                set_min_rise(data_from_server['to_rise']) #становка минимальной суммы для повышения ставки
                set_open_cards(data_from_server['cards'])

    def adapt_cards(self, num_card):
        if num_card <= 10:
            return str(num_card)
        else:
            return self.adapt_card.get(str(num_card))

    def wait_game(self):
        while True:
            data_from_server = pickle.loads(self.my_socket.recv(200))
            if data_from_server['action'] == 'start?':
                self.my_socket.send(pickle.dumps({'action': 'start?', 'answer': def_invite(data_from_server[
                                                                         'players'])}))  # def_invite функция, которая предлогает игроку начать игру, возвращает True/False
            elif data_from_server['action'] == 'start_game':


                card0 = data_from_server['cards'][0]
                card1 = data_from_server['cards'][1]
                print((card0[1])[:-1])
                print(card0[0])
                print((card1[1])[:-1])
                print(card1[0])
                self.myGui.set_card_one_player(self.my_id, (card0[1])[:-1], self.adapt_cards(card0[0]),
                                               (card1[1])[:-1], self.adapt_cards(card1[0]))
                self.myGui.add_bank_player(self.my_id, data_from_server['money'])

                #print(data_from_server['cards'][0])
                #print(data_from_server['cards'][1])
                #print(self.my_id)
                self.game_listener(data_from_server['cards'], data_from_server['bigblind'],
                                   data_from_server['min_money'], data_from_server['money'])

                break


def do_step():
    pass


def set_bank():
    pass


def set_money():
    pass


def set_min_rise():
    pass


def set_open_cards():
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

