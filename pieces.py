from common import CommonEqualityMixin

class Piece(CommonEqualityMixing):
	
	value = 0
	name = ""
	next_piece = None
	
	def __init__(self,  is_advanced = False):
		self._is_advanced = is_advanced
		if (is_advanced):
			self.value *= 2
		
	def get_value(self):
		return self.value
		
	def get_name(self):
		return self.name
		
	def make_next_piece(self, is_advanced = False):
		return self.next_piece(is_advanced) if self.next_piece is not None else None
		
	def is_advanced(self):
		return self._is_advanced
		
class Grass(Piece):
	
	value = 5
	name = "Grass"
	next_piece = Bush
	
class Bush(Piece):
	
	value = 20
	name = "Bush"
	next_piece = Tree
	
class Tree(Piece):
	
	value = 100
	name = "Tree"
	next_piece = Hut
	
class Hut(Piece):
	
	value = 500
	name = "Hut"
	next_piece = House
	
class House(Piece):
	
	value = 1500
	name = "House"
	next_piece = Mansion
	
class Mansion(Piece):
	
	value = 5000
	name = "Mansion"
	next_piece = Castle
	
class Castle(Piece):
	
	value = 20000
	name = "Castle"
	next_piece = FloatingCastle
	
class FloatingCastle(Piece):
	
	value = 100000
	name = "Floating Castle"
	next_piece = None
	
	def __init__(self, is_special = false):
		super(FloatingCastle, self).__init__(is_special)
		if (is_special):
			self.name = "Triple Castle"
			self.value = 500000