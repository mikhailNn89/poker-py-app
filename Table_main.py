from tkinter import Tk, FALSE, Button
import tkinter
from tkinter import *
from tkinter.messagebox import *
from Table_py import *
from PIL import Image, ImageTk #pip install pillow
from time import sleep


# Arseny: too many global variables
# Arseny: you will got problem on debug
# Arseny: pack your variables in one class or object for state
form1 = tkinter.Tk()
form1.title('form1')
form1.resizable(width=FALSE, height=FALSE)
form1.geometry('1300x662+100+100')
image = Image.open("image//suit.jpg")
suit = ImageTk.PhotoImage(image)

# Arseny: buf1, buf2, buf3 what is this?
# Arseny: the names of variables don't mean anything
# Arseny: I can't reach their purpose looking on the name. It's wrong
buf1 = StringVar()
buf2 = StringVar()
buf3 = StringVar()
buf1.set('YOUR NAME')
user_name=server_port = tkinter.Entry(form1,textvariable=buf1)
user_name.place(relx=0.20, rely=0.05, relwidth=0.07, relheight=0.03)
buf2.set('IP')
user_ip=server_port = tkinter.Entry(form1,textvariable=buf2)
user_ip.place(relx=0.30, rely=0.05, relwidth=0.06, relheight=0.03)
buf3.set('PORT')
server_port = tkinter.Entry(form1,textvariable=buf3)
server_port.place(relx=0.40, rely=0.05, relwidth=0.04, relheight=0.03)
user_connect = Button(text='connect', command=connect_click)
user_connect.place(relx=0.45, rely=0.05, relwidth=0.04, relheight=0.03)


def add_card_on_center(master, delta):
        bank = Button(text='bank of casino')
        bank.place(relx=0.3, rely=0.25, relwidth=0.09, relheight=0.03)
        card_server = Button(text='card')
        card_server.place(relx=delta+0.02, rely=0.31, relwidth=0.04, relheight=0.13)
        cards_center.append(card_server)
        return cards_center


def place_for_user(user, x, y):
    #suit = ImageTk.PhotoImage('lena.ppm')
    bank = Button(text='bank of '+user)
    bank.place(relx=x, rely=y, relwidth=0.09, relheight=0.03)

    card1 = Button(text='card1', image=suit)
    card1.place(relx=x, rely=y+0.04, relwidth=0.04, relheight=0.13)

    card2 = Button(text='card2', image=suit)
    card2.place(relx=x+0.05, rely=y+0.04, relwidth=0.04, relheight=0.13)

    bet_bank = Button(text='bet', state='disable')
    bet_bank.place(relx=x+0.11, rely=y+0.02, relwidth=0.04, relheight=0.03)

    raise_bet = Button(text='raise bet', command=raise_bet_click, state='disable')
    raise_bet.place(relx=x+0.11, rely=y+0.06, relwidth=0.04, relheight=0.03)

    pass_button = Button(text='pass', command=pass_button_click, state='disable')
    pass_button.place(relx=x+0.11, rely=y+0.1, relwidth=0.04, relheight=0.03)

    check = Button(text='check', command=check_click, state='disable')
    check.place(relx=x+0.11, rely=y+0.14, relwidth=0.04, relheight=0.03)

    user = Button(text='user '+user)
    user.place(relx=x, rely=y+0.19, relwidth=0.09, relheight=0.03)

    # Arseny: why do you use `dict` for scructs in your code?
    # Arseny: you should use object for this
    return {'bank': bank, 'raise_bet': raise_bet, 'bet': bet_bank, 'card1': card1,
            'card2': card2, 'check': check, 'user': user}


# Arseny: you have section global variables on the top of code
# Arseny: and then new section there. Thats hard to read and debug
cards_center = []
croupier = {'bank': 0, 'cards': cards_center}
player_places = []
size = 0.25
delta_center = 0
cards_center = add_card_on_center(form1, size+delta_center)


position = 3
shift = 0

x_default = 0.02
y_default = 0.75
user_name = {'1': 'player 1', '2': 'user 2', '3': 'player 3', '4': 'player 4', '5': 'player 5', '6': 'player 6', '7':
                    'player 7' }

player_places.append(place_for_user(user_name.get('1'), x_default, y_default-0.6))
player_places.append(place_for_user(user_name.get('2'), x_default, y_default-0.3))
player_places.append(place_for_user(user_name.get('3'), x_default, y_default))
player_places.append(place_for_user(user_name.get('4'), x_default+0.3, y_default))
player_places.append(place_for_user(user_name.get('5'), x_default+0.6, y_default))
player_places.append(place_for_user(user_name.get('6'), x_default+0.6, y_default-0.3))
player_places.append(place_for_user(user_name.get('7'), x_default+0.6, y_default-0.6))

#example for add some cards for the second player
# this wil be dict, where number of range of card will be map to face's card

# Arseny: bad names again. Why not `suite_bking`? Why `suit3`?
image = Image.open("image//king_black.jpg")
suit3 = ImageTk.PhotoImage(image)
image = Image.open("image//five_red.jpg")
suit4 = ImageTk.PhotoImage(image)

player_places[1].get('card1').config(image=suit3)
player_places[1].get('card2').config(image=suit4)
card = (croupier.get('cards'))[0]
card.config(image=suit3)

form1.mainloop()

#case with add new card in dynamic
#this code will be work only with new thred
# will be tinking
sleep(0.01)
cards_center = add_card_on_center(form1, size+0.02)
card = (croupier.get('cards'))[1]
card.config(image=suit3)
print('ok')
form1.mainloop()