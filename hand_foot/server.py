
import requests
import socket


def create_sockets(port1=2020,port2=2929,host='192.168.1.99'):
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind((host, port1))
    sock1.listen(10)
    print("Listening on {}:{}".format(host,port1))

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock2.bind((host, port2))
    sock2.listen(10)
    print("Listening on {}:{}".format(host,port2))
    
    return [sock1, sock2]

def get_players(socks):
    players = []

    (client, address) = socks[0].accept()
    data = 'Shall we play a game (y/n)'
    client.send(data.encode())
    datafromclient = client.recv(1024)

    if(datafromclient.decode()[0] == 'y'):
        players.append((client, address))
        print(datafromclient.decode())
    datafromclient = ''
    
    (client, address) = socks[1].accept()
    data = 'Shall we play a game (y/n)'
    client.send(data.encode())
    datafromclient = client.recv(1024)

    if(datafromclient.decode()[0] == 'y'):
        players.append((client, address))
        print(datafromclient.decode())
    datafromclient = ''
    
    return players

def create_deck():
    params = {'jokers_enabled':True, 'deck_count':5}
    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/', params=params)
    
#    print(response.json())
    deck_id = response.json()['deck_id']
#    print(deck_id)
    return deck_id

def deal(deck_id):
    cards = 0
    while (cards < 11):
    
        response = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=1')
        
#        print(response.json())
        
        card_id = response.json()['cards'][0]['code']
        
        response = requests.get('https://deckofcardsapi.com/api/deck/'+ deck_id +'/pile/player1/add/?cards=' + card_id)

        
        response = requests.get('https://deckofcardsapi.com/api/deck/' + deck_id + '/draw/?count=1')

        
        card_id = response.json()['cards'][0]['code']
        
        response = requests.get('https://deckofcardsapi.com/api/deck/'+ deck_id +'/pile/player2/add/?cards=' + card_id)
        
        cards = cards + 1
        
    response = requests.get('https://deckofcardsapi.com/api/deck/'+ deck_id+'/pile/player1/list/')
    
    print(response.json())
    


socks = create_sockets()

players = get_players(socks)

deck_id = create_deck()

deal(deck_id)
