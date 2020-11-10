# import Player.py
# import Meld.py
import requests
import socket

class Game:
	socks = list()
	deck = dict()
	players = list()
	discardPile = list()
	

	def __init__(self):
		self.socks = self.create_sockets()
		self.deck = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/', params={'jokers_enabled':True, 'deck_count':5}).json()
		print(self.deck)
		# players = self.get_players(self)
		response = self.deal_cards(11)
		print(len(response))
		pass

	def end(self):
		pass

	def play(self):
		pass

	def create_sockets(self, port1=2020,port2=2929,host='192.168.1.99'):
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


	def get_players(self):
		players = []

		(client, address) = self.socks[0].accept()
		data = 'Shall we play a game (y/n)'
		client.send(data.encode())
		datafromclient = client.recv(1024)

		if(datafromclient.decode()[0] == 'y'):
			players.append((client, address))
			print(datafromclient.decode())
		datafromclient = ''
		
		(client, address) = self.socks[1].accept()
		data = 'Shall we play a game (y/n)'
		client.send(data.encode())
		datafromclient = client.recv(1024)

		if(datafromclient.decode()[0] == 'y'):
			players.append((client, address))
			print(datafromclient.decode())
		datafromclient = ''
		
		return players
	
	def deal_cards(self, n=1):
		print(self.deck)
		deck = self.deck['deck_id']
		print(deck)
		send = 'https://deckofcardsapi.com/api/deck/' + deck + '/draw/?count='+ str(n)
		print(send)
		response = requests.get(send)
		print(type(response))
		print(response)
		print(response.json())
		print(type(response.json()))
		return response

game = Game()