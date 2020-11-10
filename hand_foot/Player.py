
from Meld import *

class Player:
	hand = list()
	foot = list()
	melds = list()
	hearts = int()
	client = None
	addr = None
	game = None


	def __init__(self, client, addr, game, hand, foot):
		self.melds = []
		self.client = client
		self.addr = addr
		self.game = game
		self.hand = hand
		self.foot = foot
		for card in self.hand:
			if card['code'] == '3H' or card['code'] == '3D':
				self.hearts = self.hearts + 1
				self.hand.remove(card)
				self.hand.append(self.game.deal_cards(1)[0])
		for card in self.foot:
			if card['code'] == '3H' or card['code'] == '3D':
				self.foot.remove(card)
				self.hearts = self.hearts + 1
				self.foot.append(self.game.deal_cards(1)[0])

	def turn(self):
		data = ''

		valid = False
		while (not valid):
			data = data + self.displayPlayerInfo()
			if self.game.displayTopDiscard()== '3C' or self.game.displayTopDiscard()== '3S':
				data = data +  "\nOptions:\n(D)raw - draw two cards from the draw pile"
			else:
				data = data + "\nOptions:\n(D)raw - draw two cards from the draw pile\n(P)ickup - pick up the discard pile"
			self.client.send(data.encode())

			choice = self.client.recv(1024).decode()[0]
			print(choice)	
			
			if (choice == 'D'):
				valid = True
				self.draw()


			elif(choice == 'P'):
				if(self.validPickUp()):
					valid = True
					if len(self.hand) == 0:
						self.foot.append(self.game.discardPile()[-1])
						self.game.discardPile().remove(self.game.discardPile()[-1])
					else:
						self.hand.append(self.game.discardPile()[-1])
						self.game.discardPile().remove(self.game.discardPile()[-1])
					self.layDown(True, self.displayTopDiscard())
					self.pickUpPile()
				else:
					data = 'Unable to pick up pile\n'
			else:
				data = 'invalid choice\n'

		
		data = ''
		discard = False

		while (not discard):
			data =  data + self.displayPlayerInfo()
			data = data + '\nOptions:\n(L)ay - lay down cards into a meld\n(D)iscard - discard a card to the discard pile'
			self.client.send(data.encode())

			choice = self.client.recv(1024).decode()[0]
			print(choice)
			
			if(choice == 'D'):
				discard = True
				self.discard()
			elif(choice == 'L'):
				discard = self.layDown()
				code = discard[1]
				discard = discard[0]
				if not discard:
					data = code

			else:
				data = "Invlaid Choice\n"

		data = self.displayPlayerInfo() + "\n(C)ontinue"
		self.client.send(data.encode())
		self.client.recv(1024)



	def layDown(self, pickUp=False, topCard=None):
		# Checks to see if opening meld
		data = self.displayPlayerInfo()
		data = data + '\n Pick cards to Lay Down ex (2C, 2S, 2H):'
		self.client.send(data.encode())
		choice = self.client.recv(1024).decode()

		cardCodes = [choice[0:2]]
		for x in range(4,len(choice),4):
			cardCodes.append(choice[x:x+2])

		if pickUp:
			if topCard not in cardCodes:
				return (False, "You must play the topCard of the Discard Pile\n")

		cards = []
		for code in cardCodes:
			if len(self.hand) == 0:
				for footCard in self.foot:
					if footCard['code'] == code:
						cards.append(footCard)
						break
					if self.foot[-1] == handCard:
						return (False, "You must choose cards from your hand to lay down\n")
			else:
				for handCard in self.hand:
					if handCard['code'] == code:
						cards.append(handCard)
						break
		if len(cardCodes) != len(cards):
			return (False, "You must chooose cards from your hand to lay down\n")


		# if len(self.getMelds()) == 0:
		# 	if(self.score(cards) < 90):
		# 		return (False, "You Must Have An Initial LayDown of at least 90 points\n")

		while cards:
			initLen = len(cards)
			# Checks to see if cards have already been lain down in 
			for card in cards:
				#TODO: this is where you see where the wild cards go
				wild = True
				data = ""
				while wild:
					if len(self.melds) > 0 and card['value'] == "JOKER" or card["value"] == "2":
						data = data + "What Meld would you like to put your "+card['value']+" wild card in?\n"
						self.client.send(data.encode())
						recv = self.client.recv(1024).decode()
						card['value'] = recv
						wild = False
					else:
						break

				for meld in self.melds:

					if meld.getCardType() == card['value'] and not meld.getCanasta():
						meld.add(card)
						cards.remove(card)

			wild1 = False
			wild2 = False
			wild3 = False
			meldBool = False

			for x in range(len(cards)):
				if cards[x]['value'] == "JOKER" or cards[x]['value'] == '2':
					wild1 = True
				for y in range(1, len(cards)):
					if cards[y]['value'] == "JOKER" or cards[y]['value'] == '2':
						wild2 = True
					if cards.index(cards[x]) != cards.index(cards[y]):
						if cards[x]['value'] == cards[y]['value'] or wild1 or wild2:
							for z in range(2, len(cards)):
								if cards[z]['value'] == "JOKER" or cards[z]['value'] == '2':
									wild3 = True
								if cards.index(cards[x]) != cards.index(cards[z]):
									if cards.index(cards[y]) != cards.index(cards[z]):
										if (cards[z]['value'] == cards[x]['value'] and cards[z]['value'] == cards[y][
											'value']) or (cards[y]['value'] == cards[z]['value'] and wild1) or (
												cards[x]['value'] == cards[z]['value'] and wild2) or (
												cards[x]['value'] == cards[y]['value'] and wild3) or (
												wild1 and wild3) or (wild2 and wild1) or (wild2 and wild3) or (
												wild1 and wild2 and wild3):
											meldBool = True
											print(cards[x]['value'], cards[y]['value'], cards[z]['value'])
											newMeld = Meld([cards[x], cards[y], cards[z]])
											self.melds.append(newMeld)

											card1, card2, card3 = cards[x], cards[y], cards[z]
											cards.remove(card3)
											if len(self.hand) == 0:
												self.foot.remove(card3)
											else:
												self.hand.remove(card3)
											break
					if meldBool:
						cards.remove(card2)
						if len(self.hand) == 0:
							self.foot.remove(card2)
						else:
							self.hand.remove(card2)
						break
				if meldBool:
					cards.remove(card1)
					if len(self.hand) == 0:
						self.foot.remove(card1)
					else:
						self.hand.remove(card1)
					break

				meldBool = False
				wild1 = False
				wild2 = False
				wild3 = False

			if initLen == len(cards):
				return (False, "You cannot Play those cards\n")
		return (True, "Lay Down Correct")


	def draw(self):
		heart1 = True
		heart2 = True
		while heart1 or heart2:
			newCard1 = self.game.deal_cards(1)[0]
			newCard2 = self.game.deal_cards(1)[0]
			if newCard1['code'] != '3H' and newCard1['code'] != '3D':
				heart1 = False
			else:
				self.hearts = self.hearts + 1
				newCard1 = self.game.deal_cards(1)[0]

			if newCard2['code'] != '3H' and newCard2['code'] != '3D':
				heart2 = False
			else:
				self.hearts = self.hearts + 1
				newCard2 = self.game.deal_cards(1)[0]

		if len(self.getHand()) == 0:

			self.foot.append(newCard1)
			self.foot.append(newCard2)
		else:
			self.hand.append(newCard1)
			self.hand.append(newCard2)


	def discard(self):
		data = ""
		valid = False
		while not valid:
			data = data + "select a card to discard:"
			self.client.send(data.encode())
			choice = self.client.recv(1024).decode()
			print(choice)
			if len(self.hand) == 0:
				for card in self.foot:
					if card['code'] == choice:
						valid = True
						self.game.discardPile.append(card)
						self.foot.remove(card)
						break
			else:
				for card in self.hand:
					print(card['code'])
					print(choice)
					if card['code'] == choice:
						valid = True
						self.game.discardPile.append(card)
						self.hand.remove(card)
						break
			data = "Invalid Choice\n"



		self.checkGoOut()

	def pickUpPile(self):
		if len(self.hand) == 0:
			for card in self.game.discardPile:
				self.foot.append(card)
				self.game.discardPile.remove(card)
		else:
			for card in self.game.discardPile:
				self.hand.append(card)
				self.game.discardPile.remove(card)


	def validLayDown(self):
		pass

	def validPickUp(self):
		topCard = self.game.displayTopDiscard()
		if topCard == '3C' or topCard == '3S' or topCard[0] == '2' or topCard == 'JOKER':
			return False

		cardNum = 0
		if len(self.hand) == 0:
			for card in self.foot:
				if card['code'] == 'JOKER' or card['code'] == '2' or card['code'][0] == topCard[0]:
					cardNum = cardNum + 1
		else:
			for card in self.hand:
				if card['code'] == 'JOKER' or card['code'] == '2' or card['code'][0] == topCard[0]:
					cardNum = cardNum + 1
		if cardNum < 2:
			return False

		return True

	def getHand(self):
		retHand = list()
		for card in self.hand:
			retHand.append(card['code'])
		retHand.sort()
		return retHand

	def getFoot(self):
		retFoot = list()
		for card in self.foot:
			retFoot.append(card['code'])
		retFoot.sort()
		return retFoot

	def getMelds(self):
		melds = []
		for meld in self.melds:
			melds.append(meld.displayCards())
		return melds

	def getClient(self):
		return self.client

	def displayMelds(self):
		meldInfo = "Opponent's Melds: {}".format(self.getMelds())
		return meldInfo

	def displayPlayerInfo(self):
		if len(self.getHand()) == 0:
			playerInfo = 'Foot: {}\nPlayer 0\'s Melds: {}\nDiscard Pile: {}\nPlayer 1\'s Melds: {}'.format(self.getFoot(), self.game.players[0].getMelds(), self.game.displayTopDiscard(), self.game.players[1].getMelds())
		else:
			playerInfo = 'Hand: {}\nPlayer 0\'s Melds: {}\nDiscard Pile: {}\nPlayer 1\'s Melds: {}'.format(self.getHand(), self.game.players[0].getMelds(), self.game.displayTopDiscard(), self.game.players[1].getMelds())

		return playerInfo

	def score(self, cards):
		score = 0
		print(cards)
		for card in cards:
			if card['value'] == 'ACE':
				score = score + 20
			elif card['value'] == 'JOKER':
				score = score + 50
			elif card['value'] == "KING" or card['value'] == 'QUEEN' or card['value'] == "JACK":
				score = score + 10
			elif int(card['value']) > 7:
				score = score + 10
			elif int(card['value']) == 2:
				score = score + 20
			else:
				score = score + 5
		return score

	def checkGoOut(self):
		if (len(self.hand) == 0 and self.foot != None):
			print('going to foot!')
			self.hand = self.foot.copy()
			self.foot = None
		elif (len(self.hand) == 0 and self.foot == None):
			print('you are going out')
		
