
class Meld:
	cards = list()
	canasta = False
	mixed = False
	wild = False
	cardType = str

	def __init__(self, cards):
		self.cards = cards
		if len(cards) > 7:
			self.canasta = True
		self.wild = True
		self.cardType = '2'
		for card in self.cards:
			if card['code'][0] != '2' or card['code'][0] != 'X':
				self.wild = False
				self.cardType = card['value']
				break
		if not self.wild:
			for card in cards:
				if card['code'][0] == '2' or card['code'][0] == 'X':
					self.mixed = True
					break

	def add(self, card):
		self.cards.append(card)
		if len(self.cards) > 7:
			self.canasta = True
		if not self.mixed and (card['code'][0] == 'X' or card['code'][0] == '2'):
			self.mixed = True

	def getCanasta(self):
		return self.canasta

	def getCardType(self):
		return self.cardType

	def displayCards(self):
		cards = []
		for card in self.cards:
			cards.append(card['code'])
		return cards


