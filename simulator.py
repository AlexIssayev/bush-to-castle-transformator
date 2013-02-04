#!/bin/python

from common import CommonEqualityMixin
from pieces import Piece

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
		elif self.piece_at(position) is None:
			raise ValueError("A piece is already present at " + position)
		else:
			self._board[self._position_as_index(position)] = piece
			
	def _position_as_index(self, position):
		return position.x() * self._size + position.y()
	
	def _index_as_position(self, index):
		return Position(index // self._size, index % self._size)
		
	def get_size(self):
		return self._size
	
	def is_valid_space(self, position):
		index = self._position_as_index(position)
		return 0 <= index < len(self._board)
		
	def adjacent_spaces(self, position):
		for p in position.adjacent():
			if self.is_valid_space(p):
				yield p
	
	def is_match(self, position, piece):
		if piece is None:
			raise TypeError("Cannot place a piece of type 'None'")
		visited = set([position])
		res = [position] + self._visit(position, piece, visited)
		return res
	
	def _visit(self, position, piece, visited):
		res = []
		for p in self.adjacent_spaces(position):
			if p not in visited:
				visited.add(p)
				if self.piece_at(p).can_match_with(piece):
					res += [p]
					res += self._visit(p, piece, visited)
		return res
			
	def copy_of(self, mask = set()):
		board_copy = Board(self._size)
		for i in range(len(self_board)):
			if self._index_as_position(i) not in mask:
				board_copy._board[i] = self._board[i]
		return board_copy

class Position(CommonEqualityMixin):

	def __init__(self, x, y):
		self._x = x
		self._y = y

	def x(self):
		return self._x

	def y(self):
		return self._y
	
	def shift(self, dx = 0, dy = 0):
		return Position(self._x + dx, self._y + dy)
	
	def up(self, dx = 1):
		return self.shift(dx = -dx)
		
	def down(self, dx = 1):
		return self.shift(dx = dx)
		
	def left(self, dy = 1):
		return self.shift(dy = -dy)
	
	def right(self, dy = 1):
		return self.shift(dy = dy)
		
	def adjacent(self):
		for p in self.up(), self.down(), self.right(), self.left():
			yield p

class Queue:
	
	def __init__(self):
		pass
		
	def current_piece():
		return None
		
	def next_piece():
		pass

class View:
	
	def __init__(self, board, score):
		self._board = board
		self._score = score
		
	def board(self):
		return self._board
	
	def score(self):
		return self._score
		
	def simulate_move(self, position, piece):
		new_board, delta, new_piece = self._simulate_place_piece(position, piece)
		new_view = View(board, self._score + delta)
		if new_piece is not None:
			return new_view.simulate_move(position, new_piece)
		else:
			return new_view
		
	def _simulate_place_piece(self, position, piece):
		if self._board.piece_at(position) is not None:
			raise ValueError("A piece is already present at " + position)
		delta = piece.value
		pos_match = self._board.is_match(position, piece)
		
		if len(pos_match) < 3 or piece.next_piece is None:
			new_board = self._board.copy_of()
			new_board.place_piece(position, piece)
			return new_board, delta, None
		else:
			new_piece = piece.make_next_piece(len(pos_match) >= 3)
			new_board = self._board.copy_of(set(pos_match))
			delta += new_piece._value
			return new_board, delta, new_piece
	
class CurrentView(View):
	
	def __init__(self, board, score, current_piece):
		super(CurrentView, self).__init__(board, score)
		self._current_piece = current_piece
	
	def current_piece(self):
		return self._current_piece
		
	def move_with_current_piece(self, position):
		return super(CurrentView, self).simulate_move(self, self._current_piece, position)