import sys
import copy
import random
sys.path.append('..')
from common import board

MAX_HEIGHT = 3

class No:
  count = 0
  def __init__(self, altura, color, move, current_board, pai):
    self.altura = altura
    self.color = color
    self.move = move
    self.current_board = current_board
    self.valor = 0
    self.pai = pai
    self.legal_moves = []
    self.next = None
    No.count += 1
    #print(self.altura, self.move, self.color, self.valor)

  def count_value(self, color):
    v = self.current_board.piece_count[color]
    for i in range(8):
      if self.current_board.tiles[i][0] == color:
        v += 1
      if self.current_board.tiles[i][7] == color:
        v += 1
      if self.current_board.tiles[0][i] == color:
        v += 1
      if self.current_board.tiles[7][i] == color:
        v += 1
    return v

class NoMax(No):
  def valor_max(self, alfa, beta, max_height):
    #print(alfa, beta)
    self.legal_moves = self.current_board.legal_moves(self.color)
    
    if self.altura >= max_height or len(self.legal_moves) == 0:
      self.valor = self.count_value(self.color)
      alfa = self.valor
      return alfa
    
    self.valor = -10000

    for move in self.legal_moves:
      next_board = copy.deepcopy(self.current_board)
      next_board.process_move(move, self.color)
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      next_min = NoMin(self.altura+1, next_color, move, next_board, self)
      v = next_min.valor_min(alfa, beta, max_height)
      alfa = max(alfa,v)
      #print("alfa",alfa)

      if self.valor <= next_min.valor:
        self.valor = next_min.valor
        self.next = next_min
      
      if beta < alfa:
        self.valor = alfa
        return alfa

    return alfa
    

class NoMin(No):
  def valor_min(self, alfa, beta, max_height):
    #print(alfa, beta)
    self.legal_moves = self.current_board.legal_moves(self.color)

    if self.altura >= max_height or len(self.legal_moves) == 0:
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      self.valor = self.count_value(next_color)
      beta = self.valor
      return beta

    self.valor = 10000

    for move in self.legal_moves:
      next_board = copy.deepcopy(self.current_board)
      next_board.process_move(move, self.color)
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      next_max = NoMax(self.altura+1, next_color, move, next_board, self)
      v = next_max.valor_max(alfa, beta, max_height)
      beta = min(beta,v)
      #print("beta",beta)

      if self.valor >= next_max.valor:
        self.valor = next_max.valor
        self.next = next_max

      if alfa > beta:
        self.valor = beta
        return beta

    return beta