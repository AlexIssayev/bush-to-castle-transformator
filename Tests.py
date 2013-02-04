import unittest
import pieces, simulator
from pieces import Piece

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
		self.assertEquals(x.get_name(), "foo")
		self.assertEquals(x.get_value(), 5)
		self.assertEquals(x.next_piece, Bar)

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
		self.assertEquals(x.get_value(), 10)

	def test_make_next_piece(self):
		x = Foo()
		y = x.make_next_piece()
		self.assertTrue(y.__class__ is Bar)

	def test_make_next_piece_advanced(self):
		x = Foo()
		y = x.make_next_piece(is_advanced = True)
		self.assertTrue(y.is_advanced())

	def test_make_next_piece_fails_if_no_next_piece(self):
		x = Bar()
		with self.assertRaises(TypeError):
			x.make_next_piece()

if __name__ == '__main__':
    unittest.main()