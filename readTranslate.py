import threading 
import time 

# synchronized with locks [basic] 

class Writer(threading.Thread):
	# create numbers in sequence 
	# 1, 2, 3, 4, 5, 6, 7, 8
	def __init__(self):
		super(Writer, self).__init__()
		self.currentChar = -1
		self.wlock = threading.Lock()
		self.tlock = threading.Lock()
		self.translated = True
		self.writed = 0
		self.write = threading.Condition(self.wlock)
		self.translate = threading.Condition(self.tlock)

	def generateNum(self):
		newchar = self.currentChar + 1
		newchar = newchar % 8
		self.currentChar = newchar

	def getChar(self):
		return self.currentChar

	def run(self):
		count = 0
		while count < 30:
			self.write.acquire()
			while not self.translated: # The condition to write next char is that previous char has been translated 
				self.write.wait() # wait 
			self.write.release()
			self.translate.acquire() # call acquire on the translate lock to block the translate process 
			self.generateNum()
			print(self.currentChar)
			count += 1
			self.writed += 1
			self.translated = False # the translation is no longer up to date
			self.translate.notify()
			self.translate.release()


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
			self.writer.translate.acquire()
			while self.writer.writed != 1: # keep track if the writer has writed (can be easily modified to multiple writers)
				self.writer.translate.wait()
			self.writer.translate.release()
			self.writer.write.acquire() 
			self.addChar()
			self.printChar()
			count += 1
			self.writer.translated = True 
			self.writer.writed -= 1 # has ran 
			self.writer.write.notify()
			self.writer.write.release()


if __name__ == '__main__':
	w = Writer()
	t = Translator(w)
	t.start()
	w.start()
	# t.start() # observe what happens when order switched 
	t.join()
