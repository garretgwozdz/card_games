
# from Game import *

class Player:
	hand = list()
	foot = list()
	melds = list()
	client = None
	addr = None
	game = None


	def __init__(self, client, addr, game, hand, foot):
		self.client = client
		self.addr = addr
		self.game = game
		self.hand = hand
		self.foot = foot

	def turn(self):
		self.displayPlayerInfo()
		print("Options:\ndraw - draw two cards from the draw pile\npickup - pick up the discard pile")
		valid = False
		while (not valid):
			choice = input()
			if (choice == 'draw'):
				valid = True
				self.draw()
			elif(choice == 'pickup'):
				if(validPickUp):
					valid = True
					self.pickUpPile()
				else:
					print('Unable to pick up pile')
			else:
				print('invalid choice')

		self.displayPlayerInfo()
		
		discard = False
		print('Options:\nlay - lay down cards into a meld\ndiscard - discard a card to the discard pile')
		while (not discard):
			choice = input()
			if(choice == 'discard'):
				discard = True
				self.discard()
			elif(choice == 'lay'):
				if(validLayDown):
					self.layDown()
				else:
					print('unable to lay down')
			else:
				print('invalid choice')


	def layDown(cards, self):
		# Checks to see if opening meld
		if len(self.getMelds) == 0:
			if(self.score(cards) < 90):
				print("You must lay down an opening meld of at least 90")

		# Checks to see if cards have already been lain down
		for card in cards:
			for meld in self.getMelds:
				if meld.getCardType() == card['value']:
					meld.add(card)
					cards.remove(card)

		for card1 in cards:
			for card2 in cards:
				if cards.getindex(card1) != cards.getindex(carc2):
					if card1['value'] == card2['value']:
						for card3 in  cards:
							if cards.getindex(card1) != cards.getindex(card3):
								if cards.getindex(card2) != cards.getindex(card3):
									if card3['value'] == card1['value']:
										newMeld = Meld([card1, card2, card3])
										melds.append(newMeld)
										cards.remove(card1)
										cards.remove(card2)
										cards.remove(card3)

		if len(cards) != 0:
			self.layDown(cards)


	def draw(self):
		pass

	def discard(self):
		pass
		self.checkGoOut()

	def pickUpPile(self):
		pass
		#get discard pile from game

		#get first item from pile

		#lay down first item with pair from hand

		#add rest of pile to hand

	def validLayDown(self):
		pass

	def validPickUp(self):
		pass

	def getHand(self):
		retHand = list()
		for card in self.hand:
			retHand.append(card['code'])
		return retHand

	def getFoot(self):
		retFoot = list()
		for card in self.foot:
			retFoot.append(card['code'])
		return retFoot

	def getMelds(self):
		return self.melds
	
	def displayPlayerInfo(self):
		print('Hand: {}'.format(self.getHand()))
		print('Melds: {}'.format(self.melds))
		print('foot: {}'.format(self.getFoot()))
		print('client: {}'.format(self.client))
		print('addr: {}'.format(self.addr))
		print('game: {}'.format(self.game))

	def score(cards, self):
		score = 0
		for card in cards:
			if card['value'] == 'ACE':
				score = score + 20
			if card['value'] == 'JOKER':
				score = score + 50
			if int(card['value']) > 7:
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
		
