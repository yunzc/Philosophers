import threading 
import time 

# synchronized with locks [basic] 

class Writer(threading.Thread):
	# create numbers in sequence 
	# 1, 2, 3, 4, 5, 6, 7, 8
	def __init__(self):
		super(Writer, self).__init__()
		self.currentChar = -1
		self.g = GuardClass(2)
		self.charQueue = []

	def generateNum(self):
		newchar = self.currentChar + 1
		newchar = newchar % 8
		self.currentChar = newchar
		self.charQueue.append(newchar)

	def getChar(self):
		q = self.charQueue
		self.charQueue = []
		return q

	def run(self):
		count = 0
		while count < 30:
			self.g.startWriting()
			self.generateNum()
			print(self.currentChar)
			count += 1
			self.g.stopWriting()


class Translator(threading.Thread):
	# if maps 1 to 'a' and 2 to 'b' etc 
	def __init__(self, writer):
		super(Translator, self).__init__()
		self.alph = ['a','b','c','d','e','f','g','h']
		self.queue = []
		self.writer = writer

	def addChar(self):
		recv = self.writer.getChar()
		for c in recv: 
			char = self.alph[c]
			self.queue.append(char)

	def printChar(self):
		print(self.queue)
		self.queue = []

	def run(self):
		count = 0
		while count < 15:
			self.writer.g.startTranslate()
			self.addChar()
			self.printChar()
			count += 1
			self.writer.g.stopTranslate()

class GuardClass(object):
	# synchronization 
	def __init__(self, qSize=3):
		#  queueSize specifies how many written before translating 
		self.lock = threading.Lock()
		self.runScript = threading.Condition(self.lock)
		self.numWrite = qSize
		self.Translated = True
		self.qSize = qSize 

	def startWriting(self):
		self.runScript.acquire()
		while not self.Translated:
			self.runScript.wait()
		self.runScript.release()

	def stopWriting(self):
		self.runScript.acquire()
		self.numWrite -= 1
		if self.numWrite == 0:
			self.Translated = False
			self.runScript.notify()
		self.runScript.release()

	def startTranslate(self):
		self.runScript.acquire()
		while self.numWrite != 0:
			self.runScript.wait()
		self.runScript.release()

	def stopTranslate(self):
		self.runScript.acquire()
		self.Translated = True
		self.numWrite += self.qSize 
		self.runScript.notify()
		self.runScript.release()

if __name__ == '__main__':
	w = Writer()
	t = Translator(w)
	t.start()
	w.start()
	# t.start() # observe what happens when order switched 
	t.join()
