
class Game:
	players = list()
	deck = None
	discardPile = list()
	socks = list()

	def __init__(self):
		socks = self.create_sockets()
		deck = self.create_deck()
		pass

	def end(self):
		pass

	def play(self):
		while(true):

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

	def create_deck(self):
	    params = {'jokers_enabled':True, 'deck_count':5}
	    response = requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/', params=params)
	    
	#    print(response.json())
	    deck_id = response.json()['deck_id']
	#    print(deck_id)

	    return deck_id

