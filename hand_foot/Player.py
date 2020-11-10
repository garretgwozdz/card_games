
class Player:
	hand = list()
	foot = list()
	melds = list()
	sock = None
	addr = None
	game = None


	def __init__(self, sock, addr, game):
		self.sock = sock
		self.addr = addr
		self.game = game

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


	def layDown(self):
		pass

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
		return self.hand

	def getMelds(self):
		return self.melds
	
	def displayPlayerInfo(self):
		print('Hand: {}'.format(self.hand))
		print('Melds: {}'.format(self.melds))

	def checkGoOut(self):
		if (len(self.hand) == 0 and self.foot != None):
			print('going to foot!')
			self.hand = self.foot.copy()
			self.foot = None
		elif (len(self.hand) == 0 and self.foot == None):
			print('you are going out')
		
