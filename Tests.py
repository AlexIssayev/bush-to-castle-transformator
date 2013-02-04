import unittest
import pieces, simulator
from pieces import Piece
from simulator import Position, Queue, Board, View, CurrentView

class Bar(Piece):
	name = "bar"
	value = 10

class Foo(Piece):
	name = "foo"
	value = 5
	next_piece = Bar

class PieceTest(unittest.TestCase):

	def test_sanity(self):
		x = Foo()
		self.assertEqual(x.get_name(), "foo")
		self.assertEqual(x.get_value(), 5)
		self.assertEqual(x.next_piece, Bar)

	def test_piece_can_match_with_same_type(self):
		x = Foo()
		y = Foo()
		self.assertTrue(x.can_match_with(y))

	def test_piece_can_match_with_same_type_but_advanced(self):
		x = Foo()
		y = Foo(is_advanced = True)
		self.assertTrue(x.can_match_with(y))

	def test_piece_can_not_match_with_different_type(self):
		x = Foo()
		y = Bar()
		self.assertFalse(x.can_match_with(y))

	def test_piece_can_not_match_if_no_next_piece(self):
		x = Bar()
		y = Bar()
		self.assertFalse(x.can_match_with(y))

	def test_piece_can_match_with_non_pieces_raises_error(self):
		x = Foo()
		with self.assertRaises(TypeError):
			x.can_match_with(2)

	def test_piece_has_double_score_if_advanced(self):
		x = Foo(is_advanced = True)
		self.assertEqual(x.get_value(), 10)

	def test_make_next_piece(self):
		x = Foo()
		y = x.make_next_piece()
		self.assertIs(type(y), Bar)

	def test_make_next_piece_advanced(self):
		x = Foo()
		y = x.make_next_piece(is_advanced = True)
		self.assertTrue(y.is_advanced())

	def test_make_next_piece_fails_if_no_next_piece(self):
		x = Bar()
		with self.assertRaises(TypeError):
			x.make_next_piece()

	def test_triple_castle(self):
		triple_castle = pieces.FloatingCastle(is_advanced = True)
		self.assertEqual(triple_castle.get_name(), "Triple Castle")
		self.assertEqual(triple_castle.get_value(), 500000)

class PositionTest(unittest.TestCase):

	def test_position_shift(self):
		origin = Position(0, 0)
		diagonal_down_right = origin.shift(1, 1)
		self.assertTrue(origin is not diagonal_down_right)
		self.assertEqual(diagonal_down_right.x(), 1)
		self.assertEqual(diagonal_down_right.y(), 1)

	def test_position_adjacent(self):
		origin = Position(0, 0)
		cardinals = [Position(0,1),
		             Position(1,0),
		             Position(-1, 0),
		             Position(0, -1)]
		self.maxDiff = None
		self.assertItemsEqual([p for p in origin.adjacent()], cardinals)

if __name__ == '__main__':
    unittest.main()