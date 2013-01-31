#!/bin/python

class Board:
	
	def __init__(self, size = 5):
		self._board = [None for i in range(size ** 2)]
		self._size = size
	
	def piece_at(self, position):
		return self._board[position._as_array_index()]
		
	def remove_piece(self, position):
		piece = self.piece_at(position)
		self._board[self._position_as_index(position)] = None
		return piece
		
	def place_piece(self, position, piece):
		if piece is None:
			raise TypeError("Cannot place a piece of type 'None'")
		else if self.piece_at(position) is None:
			raise ValueError("A piece is already present at " + piece)
		else:
			self._board[self._position_as_index(position)] = piece
			
	def _position_as_index(self, position):
		return position.x() * self._size + position.y()
