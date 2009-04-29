import viz

#viz.go()

class LatinSquare:
	
	def __init__(self, size):
		self.n = size
		inc = 2
		dec = self.n - 1
		self.square = []
		self.square.append([])
		self.square[0].append(0)
		self.square[0].append(1)
		for i in range(2,self.n/2 + 1):
			self.square[0].append(dec)
			self.square[0].append(inc)
			dec -= 1
			inc += 1
		
		for i in range(1,self.n):
			self.square.append([])
			for j in range(0,self.n):
				self.square[i].append((self.square[i-1][j] + 1)%(self.n))
				
	def getOrder(self, participantNum):
		return self.square[participantNum + 1]
		
	def printSquare(self):
		print self.square
			
a = LatinSquare(10)

a.printSquare()