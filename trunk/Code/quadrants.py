import viz
import random
import viztask
#viz.go()


class quadrant:
	next_to = []
	
	def __init__(self, x1, x2, y1, y2):
		self.x1 = x1
		if x1 < 0:
			self.x1_walk = x1 + 2
		else:
			self.x1_walk = x1 + 2
			
		self.x2 = x2
		if x2 < 0:
			self.x2_walk = x2 - 2
		else:
			self.x2_walk = x2 - 2
			
		self.y1 = y1
		if y1 < 0:
			self.y1_walk = y1 + 2
		else:
			self.y1_walk = y1 + 2
			
		self.y2 = y2
		if y2 < 0:
			self.y2_walk = y2 - 2
		else:
			self.y2_walk = y2 - 2
	
	def contains(self, point):
		##print point
		#print [self.x1, self.x2]
		#print [self.y1, self.y2]
		if self.x1 <= point[0] and self.x2 > point[0]:
			if self.y1 <= point[2] and self.y2 > point[2]:
				return True
		return False
		
	def get_random_walk(self):
		return self.next_to[random.randrange(0, len(self.next_to))].get_random_within()
		
	def get_random_within(self):
		return [random.uniform(self.x1_walk, self.x2_walk), 0, random.uniform(self.y1_walk, self.y2_walk)]

class QuadrantSet:
	real_room_x = 8
	room_x = real_room_x + 2
	real_room_y = 6
	room_y = real_room_y + 2
	max_x = 25
	max_y = 25
	max_walk_x = max_x + 2
	max_walk_y = max_y + 2

	quadrants = [ quadrant(-max_x, -room_x, room_y, max_y), quadrant(-room_x, room_x, room_y, max_y), quadrant(room_x, max_x, room_y, max_y), quadrant(room_x, max_x, -room_y, room_y), quadrant(room_x, max_x, -max_y, -room_y), quadrant(-room_x, room_x, -max_y, -room_y), quadrant(-max_x, -room_x, -max_y, -room_y), quadrant(-max_x, -room_x, -room_y, room_y)]

	quadrants[0].next_to = [quadrants[0], quadrants[1], quadrants[2], quadrants[7], quadrants[6]]
	quadrants[1].next_to = [quadrants[1], quadrants[0], quadrants[2]]
	quadrants[2].next_to = [quadrants[2], quadrants[1], quadrants[0], quadrants[3], quadrants[4]]
	quadrants[3].next_to = [quadrants[3], quadrants[2], quadrants[4]]
	quadrants[4].next_to = [quadrants[4], quadrants[3], quadrants[2], quadrants[5], quadrants[6]]
	quadrants[5].next_to = [quadrants[5], quadrants[4], quadrants[6]]
	quadrants[6].next_to = [quadrants[6], quadrants[5], quadrants[4], quadrants[7], quadrants[0]]
	quadrants[7].next_to = [quadrants[7], quadrants[6], quadrants[0]]


	for q in quadrants:
		print str(q.x1)+" "+str(q.x2)+" "+str(q.y1)+" "+str(q.y2)
		print str(q.x1_walk)+" "+str(q.x2_walk)+" "+str(q.y1_walk)+" "+str(q.y2_walk)
		print ""

	def get_random_point(self):
		return self.quadrants[random.randrange(0, len(self.quadrants))].get_random_within()


	def get_quadrant2(self, current_point, shouldbe ):
		for quad in self.quadrants:
			if quad.contains(current_point):
				#print [current_point, shouldbe]
				return quad
		print "Error not in a quadrant!!!!!!!!!!!!!!"
		print [current_point, shouldbe]
		return self.quadrants[0]


	def get_quadrant(self, current_point ):
		for quad in self.quadrants:
			if quad.contains(current_point):
				return quad
		print "Error not in a quadrant!!!!!!!!!!!!!!"
		print current_point
		return -1
		#return quadrants[0]
		
		