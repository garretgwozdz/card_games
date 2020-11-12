
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
			if self.game.displayTopDiscard()== '3' or self.game.displayTopDiscard()[0] == 'X' or not self.validPickUp():
				choice = "D"
			else:
				data = data + "\nOptions:\n(D)raw - draw two cards from the draw pile\n(P)ickup - pick up the discard pile"
				choice = sendText(data)

			if (choice == 'D'):
				valid = True
				self.draw()


			elif(choice == 'P'):
				valid = True
				if len(self.hand) == 0:
					self.foot.append(self.game.discardPile()[-1])
					self.game.discardPile().remove(self.game.discardPile()[-1])
					self.layDown(True, self.foot[-1]["code"])
				else:
					self.hand.append(self.game.discardPile()[-1])
					self.game.discardPile().remove(self.game.discardPile()[-1])
					self.layDown(True, self.hand[-1]["code"])


				self.pickUpPile()

			
			else:
				data = 'invalid choice\n'

		
		data = ''
		discard = False

		while (not discard):
			data =  data + self.displayPlayerInfo()
			data = data + '\nOptions:\n(L)ay - lay down cards into a meld\n(D)iscard - discard a card to the discard pile'
			choice = self.sendText(data)[0]
			
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
		self.sendText(data)

		if len(self.foot) > 0:
			return True

		return False

	def layDown(self, pickUp=False, topCard=None):

		data = self.displayPlayerInfo()
		data = data + '\n Pick cards to Lay Down ex <<2C, 2S, 2H>>:'
		choice = self.sendText(data)

		cardCodes = getCardCodesFromString(choice)

		cards = getCardsfromCardCodes(cardCodes)

		if pickUp:
			if topCard not in cardCodes:
				return (False, "You must play the topCard of the Discard Pile\n")


		if len(cardCodes) != len(cards):
			return (False, "You must chooose cards from your hand to lay down\n")


		if len(self.getMelds()) == 0:
			if(self.score(cards) < 90):
				return (False, "You Must Have An Initial LayDown of at least 90 points\n")

		definWilds(cards)

		while cards:
			initLen = len(cards)
			# Checks to see if cards have already been lain down in 
			addToExistingMeld(cards)

			newMeld = True
			while newMeld:
				newMeld = createNewMeld(cards)


			addToExistingCanasta(cards)

			if initlen == len(cards):
				return (False, "Unable to LayDown Cards\n")

		return (True, "LayDown Successfull")

	def draw(self):
		heart = True
		while heart:
			newCard = self.game.deal_cards(1)[0]
			if newCard['code'] != "3H" and newCard['code'] != "3D":
				heart = False
			else:
				self.hearts = self.hearts + 1
		if len(self.getHand()) == 0:
			self.foot.append(newCard)
		else:
			self.hand.append(newCard)

		heart = True
		while heart:
			newCard = self.game.deal_cards(1)[0]
			if newCard['code'] != "3H" and newCard['code'] != "3D":
				heart = False
			else:
				self.hearts = self.hearts + 1
		if len(self.getHand()) == 0:
			self.foot.append(newCard)
		else:
			self.hand.append(newCard)

	def defineWilds(self, cards):
		for x in range(len(cards)):
			if card['value'] == "JOKER" or card['value'] == "2":
				data = data + "What Meld would you like to put your " + card['value'] + " wild card in?\n"
				card['value'] = self.sendText(data)

	def addToExistingCanasta(self, cards):
		if len(self.melds) > 0:
			for meld in self.melds:
				for x in range(len(cards)):
					if meld.getCardType() == card['value'] and meld.getCanasta():
						meld.add(card)
						cards.remove(card)
						x = x - 1		

	def addToExistingMeld(self, cards):
		if len(self.melds) > 0:
			for meld in self.melds:
				for x in range(len(cards)):
					if meld.getCardType() == card['value'] and not meld.getCanasta():
						meld.add(card)
						cards.remove(card)
						x = x - 1		

	def createNewMeld(self, cards):
		for x in range(0, len(cards)):
			for y in range(x+1, len(cards)):
				if cards[x]['value'] == cards[y]['value']:
					for z in range(y+1, len(cards)):
						if cards[z]['value'] == cards[x]['value']:
							newMeld = Meld([cards[x], cards[y], cards[z]])
							cards.remove(cards[z])
							cards.remove(cards[y])
							cards.remove(cards[x])
							return True

		return False

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
			for x in range(len(self.game.discardPile)):
				self.foot.append(self.game.discardPile[x])
		else:
			for x in range(len(self.game.discardPile)):
				self.hand.append(self.game.discardPile[x])
		self.game.discardPile = []

	def getCardsfromCardCodes(self, cardCodes):
		cards = []
		for code in cardCodes:
			if len(self.hand) == 0:
				for footCard in self.foot:
					if footCard['code'] == code:
						cards.append(footCard)
						break
			else:
				for handCard in self.hand:
					if handCard['code'] == code:
						cards.append(handCard)
						break

		return cards

	def getCardCodesFromString(self, cardCodeStrings):
		cardCodes = [cardCodeStrings[0:2]]
		for x in range(4,len(cardCodeStrings),4):
			cardCodes.append(cardCodeStrings[x:x+2])
		return cardCodes

	def validPickUp(self):
		topCard = self.game.displayTopDiscard()
		if topCard == '3C' or topCard == '3S' or topCard[0] == '2' or topCard == 'JOKER':
			return False

		cardNum = 0
		if len(self.hand) == 0:
			for card in self.foot:
				if card['value'] == 'JOKER' or card['value'] == '2' or card['code'][0] == topCard[0]:
					cardNum = cardNum + 1
		else:
			for card in self.hand:
				if card['value'] == 'JOKER' or card['value'] == '2' or card['code'][0] == topCard[0]:
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
		
	def sendText(text, self):
		encodedText = text.encode()
		self.client.send(encodedText)
		recvData = self.client.recv(1024)
		print(recvData)
		return recvDat

	def haveWildCanasta(self):
		for meld in self.melds:
			if meld.getWild():
				return True
		return False

	def haveTwoNaturals(self):
		for x in range(len(self.melds)):
			if not self.melds[x].getMixed():
				for y in range(x, lens(self.melds)):
					if not self.melds[x].getMixed():
						return True
		return False

	def haveTwoMixed(self):
		for x in range(len(self.melds)):
			if self.melds[x].getMixed():
				for y in range(x, lens(self.melds)):
					if self.melds[x].getMixed():
						return True
		return False
