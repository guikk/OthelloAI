import sys
import copy
sys.path.append('..')
from common import board

class No:
  count = 0
  def __init__(self, altura, color, move, current_board, pai):
    self.altura = altura
    self.color = color
    self.move = move
    self.current_board = current_board
    self.pai = pai
    self.legal_moves = []
    self.explored = {}
    self.next = None
    No.count += 1


  def size(self):
    size = sys.getsizeof(self)
    size += sys.getsizeof(self.altura)
    size += sys.getsizeof(self.color)
    size += sys.getsizeof(self.move)
    size += sys.getsizeof(self.current_board)
    size += sys.getsizeof(self.legal_moves)
    return size

  def count_value(self, color):
    v = self.current_board.piece_count[color]

    if self.current_board.tiles[0][0] == color:
      v += 2
    if self.current_board.tiles[0][7] == color:
      v += 2
    if self.current_board.tiles[7][0] == color:
      v += 2
    if self.current_board.tiles[7][7] == color:
      v += 2

    for i in range(8):
      if self.current_board.tiles[i][0] == color:
        v += 2
      if self.current_board.tiles[i][7] == color:
        v += 2
      if self.current_board.tiles[0][i] == color:
        v += 2
      if self.current_board.tiles[7][i] == color:
        v += 2
      
      if self.current_board.tiles[i][1] == color:
        if i>0 and self.current_board.tiles[i-1][0] == board.Board.EMPTY:
          v -= 1
        if self.current_board.tiles[i][0] == board.Board.EMPTY:
          v -= 1
        if i<7 and self.current_board.tiles[i+1][0] == board.Board.EMPTY:
          v -= 1
      
      if self.current_board.tiles[i][6] == color:
        if i>0 and self.current_board.tiles[i-1][7] == board.Board.EMPTY:
          v -= 1
        if self.current_board.tiles[i][7] == board.Board.EMPTY:
          v -= 1
        if i<7 and self.current_board.tiles[i+1][7] == board.Board.EMPTY:
          v -= 1
          
      if self.current_board.tiles[1][i] == color:
        if i>0 and self.current_board.tiles[0][i-1] == board.Board.EMPTY:
          v -= 1
        if self.current_board.tiles[0][i] == board.Board.EMPTY:
          v -= 1
        if i<7 and self.current_board.tiles[0][i+1] == board.Board.EMPTY:
          v -= 1
      
      if self.current_board.tiles[6][i] == color:
        if i>0 and self.current_board.tiles[7][i-1] == board.Board.EMPTY:
          v -= 1
        if self.current_board.tiles[7][i] == board.Board.EMPTY:
          v -= 1
        if i<7 and self.current_board.tiles[7][i+1] == board.Board.EMPTY:
          v -= 1
    return v

class NoMax(No):
  def valor_max(self, alfa, beta, max_height):
    
    if len(self.legal_moves) == 0:
      self.legal_moves = self.current_board.legal_moves(self.color)
    
    if self.altura >= max_height or len(self.legal_moves) == 0:
      alfa = self.count_value(self.color)
      return alfa
    
    alfa = -10000

    for index, move in enumerate(self.legal_moves):
      
      next_min = None
      if move in self.explored:
        next_min = self.explored[move]
      else:
        next_board = copy.deepcopy(self.current_board)
        next_board.process_move(move, self.color)
        next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
        next_min = NoMin(self.altura+1, next_color, move, next_board, self)
        del next_board
        self.explored[move] = next_min

      v = next_min.valor_min(alfa, beta, max_height)
      if v > alfa:
        self.legal_moves.pop(index)
        self.legal_moves.insert(0,move)
        alfa = v
        self.next = next_min
      
      if beta < alfa:
        return alfa

    return alfa
    

class NoMin(No):
  def valor_min(self, alfa, beta, max_height):
    
    if len(self.legal_moves) == 0:
      self.legal_moves = self.current_board.legal_moves(self.color)

    if self.altura >= max_height or len(self.legal_moves) == 0:
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      beta = self.count_value(next_color)
      return beta

    beta = 10000

    for index, move in enumerate(self.legal_moves):
      
      next_max = None
      if move in self.explored:
        next_max = self.explored[move]
      else:
        next_board = copy.deepcopy(self.current_board)
        next_board.process_move(move, self.color)
        next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
        next_max = NoMax(self.altura+1, next_color, move, next_board, self)
        del next_board
        self.explored[move] = next_max

      v = next_max.valor_max(alfa, beta, max_height)
      if v < beta:
        self.legal_moves.pop(index)
        self.legal_moves.insert(0,move)
        beta = v
        self.next = next_max

      if alfa > beta:
        return beta

    return beta