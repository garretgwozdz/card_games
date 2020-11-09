
class Player:
	hand = list()
	foot = list()
	melds = list()
	sock = None
	addr = None
	game = None


	def __init__(sock, addr, self, game):
		self.sock = sock
		self.addr = addr
		self.game = game

	def turn(self):
		pass

	def layDown(self):
		pass

	def draw(self):
		pass

	def discard(self):
		pass

	def pickUpPile(self):
		pass

	def checkValidLayDown(self):
		pass

	def checkValidPickUp(self):
		pass

	def getHand(self):
		return self.hand