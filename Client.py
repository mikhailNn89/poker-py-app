import socket
import threading
import pickle


class Client(object):
    def __init__(self, ip, port, username):
        self.my_socket = socket.socket()
        self.my_socket.connect((ip, port))
        self.my_socket.send(pickle.dumps({'name': username}))
        data = pickle.loads(self.my_socket.recv(200))
        if data['status'] == 'ok':
            self.my_id = data['yourid']
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

    def wait_game(self):
        while True:
            data_from_server = pickle.loads(self.my_socket.recv(200))
            if data_from_server['action'] == 'start?':
                self.my_socket.send(pickle.dumps({'action': 'start?', 'answer': def_invite(data_from_server[
                                                                         'players'])}))  # def_invite функция, которая предлогает игроку начать игру, возвращает True/False
            elif data_from_server['action'] == 'start_game':
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
    a = Client('localhost', 8011, 'Sergey')