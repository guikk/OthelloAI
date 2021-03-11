import sys
import copy
from time import time
sys.path.append('..')
from common import board


def make_move(the_board, color_str):
    """
    Returns the next move
    :return: (int, int)
    """
    color = board.Board.WHITE if color_str == 'white' else board.Board.BLACK
    opponent_color = board.Board.BLACK if color_str == 'white' else board.Board.WHITE
    legal_moves = the_board.legal_moves(color)

    if len(legal_moves) > 0:

        max_value = 0
        max_choice = (-1,-1)

        for max_move in legal_moves:
            max_board = copy.deepcopy(the_board)
            max_board.process_move(max_move, color)
  
            next_value = max_board.piece_count[color]
            
            min_value = 65
            for min_move in max_board.legal_moves(opponent_color):
                min_board = copy.deepcopy(max_board)
                min_board.process_move(min_move, opponent_color)

                if min_board.piece_count[opponent_color] < min_value:
                    min_value = min_board.piece_count[opponent_color]
                    next_value = min_board.piece_count[color]

            print(f"Move: {max_move} | Next value: {next_value}")
            if next_value > max_value:
                move_choice = max_move
                max_value = next_value

        print(f"Chose move {move_choice}")
        return move_choice
    else:
        return (-1, -1)


if __name__ == '__main__':
    start = time()
    b = board.from_file(sys.argv[1])
    f = open('move.txt', 'w')
    f.write('%d,%d' % make_move(b, sys.argv[2]))
    f.close()
    print(f"Time elapsed = {time()-start:.2f}s")
