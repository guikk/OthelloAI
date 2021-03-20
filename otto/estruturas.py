import sys
import copy
import random
sys.path.append('..')
from common import board

MAX_HEIGHT = 4

class No:
  def __init__(self, altura, color, move, current_board, pai):
    self.altura = altura
    self.color = color
    self.move = move
    self.current_board = current_board
    self.valor = 0
    self.pai = pai
    self.legal_moves = []
    self.next = None
    #print(self.altura, self.move, self.color, self.valor)

class NoMax(No):
  def valor_max(self):
    self.legal_moves = self.current_board.legal_moves(self.color)
    
    if self.altura >= MAX_HEIGHT or len(self.legal_moves) == 0:
      self.valor = self.current_board.piece_count[self.color]
      return self
    
    self.valor = -10000

    for move in self.legal_moves:
      next_board = copy.deepcopy(self.current_board)
      next_board.process_move(move, self.color)
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      next_min = NoMin(self.altura+1, next_color, move, next_board, self)
      next_min.valor_min()
      if self.valor <= next_min.valor:
        self.valor = next_min.valor
        self.next = next_min

    return self
    

class NoMin(No):
  def valor_min(self):
    self.legal_moves = self.current_board.legal_moves(self.color)

    if self.altura >= MAX_HEIGHT or len(self.legal_moves) == 0:
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      self.valor = self.current_board.piece_count[next_color]
      return self

    self.valor = 10000

    for move in self.legal_moves:
      next_board = copy.deepcopy(self.current_board)
      next_board.process_move(move, self.color)
      next_color = board.Board.WHITE if self.color == board.Board.BLACK else board.Board.BLACK
      next_max = NoMax(self.altura+1, next_color, move, next_board, self)
      next_max.valor_max()
      if self.valor >= next_max.valor:
        self.valor = next_max.valor
        self.next = next_max

    return self