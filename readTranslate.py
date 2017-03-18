import threading 
import time 

# synchronized with locks [basic] 

class Writer(threading.Thread):
	# create numbers in sequence 
	# 1, 2, 3, 4, 5, 6, 7, 8
	def __init__(self):
		super(Writer, self).__init__()
		self.currentChar = 1
		self.lock = threading.Lock()

	def generateNum(self):
		newchar = self.currentChar + 1
		newchar = newchar % 8
		self.currentChar = newchar

	def getChar(self):
		return self.currentChar

	def run(self):
		count = 0
		while count < 30:
			self.lock.acquire()
			print(self.currentChar)
			self.lock.release()
			self.generateNum()
			count += 1


class Translator(threading.Thread):
	# if maps 1 to 'a' and 2 to 'b' etc 
	def __init__(self, writer):
		super(Translator, self).__init__()
		self.alph = ['a','b','c','d','e','f','g','h']
		self.queue = []
		self.writer = writer

	def addChar(self):
		recv = self.writer.getChar()
		char = self.alph[recv]
		self.queue.append(char)

	def printChar(self):
		print(self.queue)
		self.queue = []

	def run(self):
		count = 0
		while count < 30:
			self.addChar()
			self.writer.lock.acquire()
			self.printChar()
			self.writer.lock.release()
			count += 1


if __name__ == '__main__':
	w = Writer()
	t = Translator(w)
	t.start()
	w.start()
	# t.start() # observe what happens when order switched 
	t.join()
