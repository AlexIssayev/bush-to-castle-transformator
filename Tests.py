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

	def test_position_equality(self):
		x = Position(0, 0)
		y = Position(0, 0)
		self.assertEqual(x, y)

	def test_position_x_differs(self):
		x = Position(0, 1)
		y = Position(1, 1)
		self.assertLess(x, y)
		self.assertGreater(y, x)
		self.assertNotEqual(x, y)

	def test_position_y_differs(self):
		x = Position(1, 0)
		y = Position(1, 1)
		self.assertLess(x, y)
		self.assertGreater(y, x)
		self.assertNotEqual(x, y)

class BoardTest(unittest.TestCase):

	#Brittle
	def test_board_piece_at(self):
		board = Board(size = 2)
		foo = Foo()
		board._board[0] = foo
		self.assertEqual(board.piece_at(Position(0, 0)), foo)

	def test_board_creation(self):
		board = Board(size = 2)
		self.assertEqual(board.size(), 2)
		positions = [Position(0, 0), Position(0, 1), Position(1, 0), Position(0, 0)]
		for p in positions:
			self.assertIsNone(board.piece_at(p))

	def test_board_place_piece(self):
		board = Board(size = 2)
		origin = Position(0, 0)
		foo = Foo()
		board.place_piece(position = origin, piece = foo)
		self.assertEqual(board.piece_at(origin), foo)

	def test_board_place_piece_when_piece_present(self):
		board = Board(size = 2)
		origin = Position(0, 0)
		foo = Foo()
		foo2 = Foo()
		board.place_piece(origin, foo)
		with self.assertRaises(ValueError):
			board.place_piece(origin, foo2)

	def test_board_remove_piece(self):
		board = Board(size = 2)
		origin = Position(0,0)
		foo = Foo()
		board.place_piece(origin, foo)
		self.assertEqual(board.remove_piece(origin), foo)
		self.assertIsNone(board.piece_at(origin))

	def test_board_positions(self):
		board = Board(size = 2)
		expected_positions = [Position(0, 0), 
		                      Position(0, 1), 
		                      Position(1, 0), 
		                      Position(1, 1)]
		actual_positions = [p for p in board.positions()]
		self.assertItemsEqual(actual_positions, expected_positions)

	def test_board_open_positions(self):
		board = Board(size = 2)
		board.place_piece(Position(0, 0), Foo())
		board.place_piece(Position(1, 1), Foo())
		expected_positions = [Position(0, 1),
		                      Position(1, 0)]
		actual_positions = [p for p in board.open_positions()]
		self.assertItemsEqual(actual_positions, expected_positions)

	def test_board_is_valid_position(self):
		board = Board(size = 3)
		origin = Position(0, 0)
		center = Position(1, 1)
		bottom_right = Position(2, 2)
		self.assertTrue(board.is_valid_position(origin))
		self.assertTrue(board.is_valid_position(center))
		self.assertTrue(board.is_valid_position(bottom_right))

	def test_boad_is_valid_position_out_of_bounds(self):
		board = Board(size = 3)
		oob_top_left = Position(-1, -1)
		oob_bottom_right = Position(3, 3)
		self.assertFalse(board.is_valid_position(oob_top_left))
		self.assertFalse(board.is_valid_position(oob_bottom_right))

	def test_board_adjacent_positions(self):
		board = Board(size = 3)
		expected_positions = [Position(1, 0),
		                      Position(0, 1),
		                      Position(2, 1),
		                      Position(1, 2)]
		actual_positions = [p for p in board.adjacent_positions(Position(1, 1))]
		self.assertItemsEqual(actual_positions, expected_positions)

	def test_board_adjacent_positions_on_corner(self):
		board = Board(size = 2)
		expected_positions = [Position(1, 0),
		                      Position(0, 1)]
		actual_positions = [p for p in board.adjacent_positions(Position(1, 1))]
		self.assertItemsEqual(actual_positions, expected_positions)

	def test_board_eq_same_board(self):
		board = Board(size = 2)
		board.place_piece(Position(0, 0), Foo())
		self.assertEqual(board, board)

	def test_board_eq_same_pieces(self):
		board = Board(size = 2)
		board.place_piece(Position(0, 0), Foo())
		board.place_piece(Position(0, 1), Bar())
		other_board = Board(size = 2)
		other_board.place_piece(Position(0, 0), Foo())
		other_board.place_piece(Position(0, 1), Bar())
		self.assertEqual(board, other_board)

	def test_board_neq_diff_size(self):
		board = Board(size = 2)
		board.place_piece(Position(0, 0), Foo())
		board.place_piece(Position(0, 1), Bar())
		other_board = Board(size = 3)
		other_board.place_piece(Position(0, 0), Foo())
		other_board.place_piece(Position(0, 1), Bar())
		self.assertNotEqual(board, other_board)

	def test_board_neq_diff_placing(self):
		board = Board(size = 2)
		board.place_piece(Position(0, 0), Foo())
		board.place_piece(Position(0, 1), Bar())
		other_board = Board(size = 3)
		other_board.place_piece(Position(0, 1), Foo())
		other_board.place_piece(Position(1, 1), Bar())
		self.assertNotEqual(board, other_board)

	def test_copy_of(self):
		board = Board(size = 3)
		board.place_piece(Position(0, 0), Foo())
		board.place_piece(Position(1, 1), Foo())
		board.place_piece(Position(2, 2), Foo())
		other_board = board.copy_of()
		self.assertFalse(other_board is board)
		self.assertEqual(board, other_board)

if __name__ == '__main__':
    unittest.main()