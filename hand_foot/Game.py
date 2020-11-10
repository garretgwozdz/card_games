from Player import *
import Meld
import requests
import socket

class Game:
	socks = list()
	deck = dict()
	players = list()
	discardPile = list()
	turn = int()
	

	def __init__(self):
		self.turn = 0
		self.socks = self.create_sockets()
		self.deck = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/', params={'jokers_enabled':True, 'deck_count':5}).json()
		#print(self.deck)
		self.players = self.get_players()
		self.discardPile.append(self.deal_cards(1)[0])

		player0Data = self.players[0].displayPlayerInfo() + '\n' + self.players[1].displayMelds() + '\n(C)ontinue?'
		self.players[0].getClient().send(player0Data.encode())

		player1Data = self.players[1].displayPlayerInfo() +  '\n' + self.players[0].displayMelds() + '\n(C)ontinue?'
		self.players[1].getClient().send(player1Data.encode())

		datafromclient = self.players[0].getClient().recv(1024)
		datafromclient = self.players[1].getClient().recv(1024)





	def end(self):
		pass

	def play(self):
		while(True):

			self.players[self.turn].turn()

			if self.turn == 0:
				self.turn = 1
			else:
				self.turn = 0


	def create_sockets(self, port1=2020,port2=2929,host='127.0.0.1'):
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

	
	def deal_cards(self, n=1):
		response = requests.get('https://deckofcardsapi.com/api/deck/' + self.deck['deck_id'] + '/draw/?count='+ str(n))
		return response.json()['cards']

	def displayTopDiscard(self):
		topCard = self.discardPile[-1]['code']
		return topCard

	def get_players(self):
		players = []

		(client, address) = self.socks[0].accept()
		data = 'Shall we play a game (y/n)'
		client.send(data.encode())
		datafromclient = client.recv(1024)

		if(datafromclient.decode()[0] == 'y'):
			newPlayer = Player(client, address, self, self.deal_cards(11), self.deal_cards(11))

			players.append(newPlayer)
			print(datafromclient.decode())
		datafromclient = ''
		
		(client, address) = self.socks[1].accept()
		data = 'Shall we play a game (y/n)'
		client.send(data.encode())
		datafromclient = client.recv(1024)

		if(datafromclient.decode()[0] == 'y'):
			newPlayer = Player(client, address, self, self.deal_cards(11), self.deal_cards(11))

			players.append(newPlayer)
			print(datafromclient.decode())
		datafromclient = ''
		
		return players


game = Game()

game.play()