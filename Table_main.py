from tkinter import Tk, FALSE, Button, StringVar
import tkinter
from Client import *
from PIL import Image, ImageTk #pip install pillow
import os

        
class GUI:
    def __init__(self, form):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.myId = -100
        self.form1 = form
        
        self.client=Client()
        self.client.update=self.update_data#когда приходит обновление в клиент, то дергается эта функция
        self.client.allow_to_step=self.allow_to_step
        self.client.game_has_begun=self.begin_game
        self.client.end_game=self.end_game
        self.client.invite_to_game=self.invite_to_game
        self.client.whose_step=self.whose_step
        
        self.form1.title('form1')
        self.form1.resizable(width=FALSE, height=FALSE)
        self.form1.geometry('1200x662+100+100')
        self.weigh_card = 0.046
        self.height_card = 0.13
        line = StringVar()
        line.set('Sergey')
        self.user_name = tkinter.Entry(self.form1, textvariable=line)
        self.user_name.place(relx=0.20, rely=0.05, relwidth=0.07, relheight=0.03)
        line2 = StringVar()
        line2.set('127.0.0.1')
        self.user_ip = tkinter.Entry(self.form1, textvariable=line2)
        self.user_ip.place(relx=0.30, rely=0.05, relwidth=0.06, relheight=0.03)
        line3 = StringVar()
        line3.set('8011')
        self.server_port = tkinter.Entry(self.form1, textvariable=line3)
        self.server_port.place(relx=0.40, rely=0.05, relwidth=0.04, relheight=0.03)
        self.user_connect = Button(text='connect', command=self.connect_click)
        self.user_connect.place(relx=0.45, rely=0.05, relwidth=0.04, relheight=0.03)
        self.startbtn = Button(text='start', command=self.start_game, state="disable")
        self.startbtn.place(relx=0.45, rely=0.02, relwidth=0.04, relheight=0.03)
        self.cards_center = []
        self.bank = Button(text='bank of casino')
        self.croupier = {'bank': self.bank, 'cards': self.cards_center}
        self.players_name = {'1': 'player 1', '2': 'user 2', '3': 'player 3', '4': 'player 4', '5': 'player 5', '6': 'player 6',
                     '7':'player 7'}
        # name of cards 'suit', 'ace', 'king', 'queen', 'jack', '10', '9', '8', '7', '6', '5', '4''3''2''j_red', 'j_black'
        # suit of cards (FOLDERS) -'suit', 'joker', 'club', 'diamond', 'heart', 'spade'
        self.shirt = ""
        self.store_image = []
        self.player_places = []

    def setMyId(self, id):
        self.myId = id

    def getMyId(self):
        return self.myId

    def get_image(self, suit, name):
        #self.store_image.append(ImageTk.PhotoImage(Image.open(os.path.join('image', 'cards', suit, name + '.jpg'))))
        self.store_image.append(ImageTk.PhotoImage(Image.open(os.path.join('image', 'cards', suit, name + '.jpg'))))
        return self.store_image[len(self.store_image)-1]
        
    def set_card_player(self, number,):
        pass
        
    def update_bank_croupier(self, data):
        self.croupier.get('bank')['text'] = data

    def clean_card_on_center(self):
        self.cards_center = []
        self.croupier = {'bank': self.bank, 'cards': self.cards_center}

    def add_card_on_center(self, suit, name):
        #last number is start 'x'
        delta = (len(self.croupier.get('cards')) * 0.03) + 0.25
        self.bank.place(relx=0.3, rely=0.25, relwidth=0.09, relheight=0.03)
        card_server = (Button(text='card'))
        card_server.place(relx=delta, rely=0.31, relwidth=self.weigh_card, relheight=self.height_card)
        card_server.config(image=self.get_image(suit, name))
        (self.croupier.get('cards')).append(card_server)
        return self.croupier
        
    def place_for_user(self, user, x, y):
        bank = Button(text="0")
        bank.place(relx=x, rely=y, relwidth=0.09, relheight=0.03)
        #self.bank = tkinter.Entry(self.form1, textvariable="empty")
        #self.bank.place(relx=x, rely=y, relwidth=0.09, relheight=0.03)
        info_text = Button(text='', state='disable')#для вывода информации о шаге или победе
        info_text.place(relx=x + 0.01, rely=y - 0.04, relwidth=0.1, relheight=0.03)#
        card1 = Button(text='card1', image=self.shirt)
        card1.place(relx=x, rely=y + 0.04, relwidth=self.weigh_card, relheight=self.height_card)
        card2 = Button(text='card2', image=self.shirt)
        card2.place(relx=x + 0.05, rely=y + 0.04,  relwidth=self.weigh_card, relheight=self.height_card)
        curr_bet_text = StringVar()#
        curr_bet= tkinter.Entry(self.form1, textvariable=curr_bet_text)#
        curr_bet.place(relx=x + 0.11, rely=y + 0.00, relwidth=0.04, relheight=0.03)#
        bet_bank = Button(text='0', state='disable')
        bet_bank.place(relx=x + 0.11, rely=y + 0.02, relwidth=0.04, relheight=0.03)
        raise_bet = Button(text='raise bet', command=self.raise_bet_click, state='disable')
        raise_bet.place(relx=x + 0.11, rely=y + 0.06, relwidth=0.04, relheight=0.03)
        pass_button = Button(text='pass', command=self.pass_button_click, state='disable')
        pass_button.place(relx=x + 0.11, rely=y + 0.1, relwidth=0.04, relheight=0.03)
        check = Button(text='check', command=self.check_click, state='disable')
        check.place(relx=x + 0.11, rely=y + 0.14, relwidth=0.04, relheight=0.03)
        user = Button(text='user ' + user)
        user.place(relx=x, rely=y + 0.19, relwidth=0.09, relheight=0.03)
        return {'bank': bank, 'raise_bet': raise_bet, 'bet': bet_bank, 'card1': card1,
                'card2': card2, 'check': check, 'user': user, 'pass': pass_button,'curr_bet':curr_bet_text,'info':info_text,'id':-1}
                
    def setting_player_places(self):
        x_default = 0.02
        y_default = 0.75
        user_name = my_gui.user_name
        self.player_places.append(my_gui.place_for_user(self.players_name.get('1'), x_default, y_default - 0.6))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('2'), x_default, y_default - 0.3))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('3'), x_default, y_default))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('4'), x_default + 0.3, y_default))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('5'), x_default + 0.6, y_default))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('6'), x_default + 0.6, y_default - 0.3))
        self.player_places.append(my_gui.place_for_user(self.players_name.get('7'), x_default + 0.6, y_default - 0.6))

    def set_card_one_player(self, position, suit1, name_card1, suit2, name_card2):
        my_gui.player_places[position].get('card1').config(image=my_gui.get_image(suit1, name_card1))
        my_gui.player_places[position].get('card2').config(image=my_gui.get_image(suit2, name_card2))

    def change_croupier(self, bank, suit, name_card):
        self.croupier.get('bank')['text'] = bank
        self.add_card_on_center(suit, name_card)
        return self.croupier
        
    def change_button_player(self, position, flag):
        #disabled on default setting
        status = 'disable'
        if flag:
            status = 'active'
            
        (self.player_places[position].get('bet'))['state'] = status
        (self.player_places[position].get('raise_bet'))['state'] = status
        (self.player_places[position].get('pass'))['state'] = status
        (self.player_places[position].get('check'))['state'] = status
        
    def change_bet_player(self,position, bet):
        # bank = (self.player_places[position].get('bank'))['text']
        # if (int(bank) - int(bet)) > 0:
        (self.player_places[position].get('bet'))['text'] = bet
        # else:
        #    bet = bank
        #    (self.player_places[position].get('bet'))['text'] = bet
        #    (self.player_places[position].get('bank'))['text'] = bank
        #if int(bank) > 0:
        #    (self.player_places[position].get('bank'))['text'] = (int(bank) - int(bet))
    
    def start_game(self):
        self.startbtn['text']= "Ждём других"
        self.client.start_game()
    
    def whose_step(self,data):
        for i in self.player_places:
            if i['id'] == data['id'] and i['id']!=self.client.my_id:
                i['info']['text']="Ход"
                break
    
    def invite_to_game(self):
        self.startbtn['state']='normal'
        
    def add_bank_player(self,position, summa):
        if summa > 0:
            (self.player_places[position].get('bank'))['text'] = summa

    def change_name_user(self,position, name):
        (self.player_places[position].get('user'))['text'] = name
    
    def raise_bet_click(self):
        for i in self.player_places:#забираем возможность делать ход
            if i['id'] == self.client.my_id:
                i['raise_bet']['state']='disable'
                i['info']['text']=''
        for i in self.player_places:
            if i['id'] == self.client.my_id:
                self.client.step(('raise',int(i['curr_bet'].get())))#для теста
                

    def check_click(self):
        self.client.step(('check',0))

    def pass_button_click(self):
        self.client.step(('fold',0))
        
    def begin_game(self,data):
        self.startbtn['text']= "Идёт игра"
        self.set_bank_of_player(data['money'])
        self.set_card_on_player(data['cards'])
        
    def connect_click(self):
        self.client.connect(self.user_ip.get(), int(self.server_port.get()),self.user_name.get())
        if self.client.is_connected:
            self.myId = self.client.get_id()
            self.change_name_user(self.client.get_id(), self.user_name.get())
            self.set_userid(self.client.get_id())#пока так
            
    def allow_to_step(self):
        for i in self.player_places:#даем игроку возможность ходить. пока так 
            if i['id'] == self.client.my_id:
                i['raise_bet']['state']='normal'
                i['info']['text']='Твой ход'
            else:
                i['info']['text']=''
        
    def end_game(self,data):
        if self.client.my_id==data['winners'][0]:
            for i in self.player_places:
                if i['id'] == data['winners'][0]:
                    i['info']['text']= "Ты победил! "+data['combination']
        else:
            for i in self.player_places:
                if i['id'] == data['winners'][0]:
                    i['info']['text']= "Победа. "+data['combination']
                    
    def update_data(self,data):
        print(data)
        for player in self.client.players:
            print(player)
            id = player[0]
            curr_bet = player[1]
            player_bank = player[2]
            self.set_money(id, curr_bet, player_bank)
            self.change_name_user(id, player[3])#пока так
            self.set_userid(id)#пока так
            self.set_min_raise(data['to_raise']) #становка минимальной суммы для повышения ставки
            self.set_open_cards(data['open_cards'], data['bank'])
            
    def set_money(self, id, curr_bet, player_money):
        self.add_bank_player(id, player_money)
        self.change_bet_player(id, curr_bet)
            
    def set_min_raise(self, min_bet):
        pass
        
    def set_userid(self,id):
        position=id#пока так
        self.player_places[position]['id']=id
        #print((self.player_places[position].get('user'))['id'])
        #(self.player_places[position].get('user'))['id'] = id
        
    def set_open_cards(self, open_cards, bank):
        if len(open_cards) != 0:
            self.clean_card_on_center()
            for card in open_cards:
                num_card = self.adapt_cards(card[0])
                suit_card = (card[1])[:-1]
                self.change_croupier(bank, suit_card, num_card)
                
    def adapt_cards(self, num_card):
        self.adapt_card = {'11': 'jack', '12': 'queen', '13': 'king', '14': 'ace'}
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
        self.set_card_one_player(self.getMyId(), suit_card0, num_card0, suit_card1, num_card1)

    def set_bank_of_player(self, money):
        self.add_bank_player(self.getMyId(), money)
        
root = Tk()
my_gui = GUI(root)
my_gui.shirt = my_gui.get_image('shirt', 'shirt')
my_gui.setting_player_places()

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


root.mainloop()


#print("it never print")



