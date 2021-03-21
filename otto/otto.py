import sys
import copy
from time import time
from estruturas import NoMax
from util import estimate_size
sys.path.append('..')
from common import board


def make_move(the_board, color_str):
    """
    Returns the next move
    :return: (int, int)
    """
    color = board.Board.WHITE if color_str == 'white' else board.Board.BLACK

    raiz = NoMax(0, color, None, the_board, None)

    start = time()
    for max_height in range(3,12,2):
        raiz.valor_max(-10000,10000, max_height)
        
        print("choice:", raiz.next.move, f"altura {max_height}, {raiz.count} nós explorados;", f"{time()-start:.2f}s")
        print("estimate size", estimate_size(raiz))

        f = open('move.txt', 'w')
        f.write('%d,%d' % raiz.next.move)
        f.close()

    move = raiz.next.move
    return move


if __name__ == '__main__':
    start = time()
    b = board.from_file(sys.argv[1])
    f = open('move.txt', 'w')
    f.write('%d,%d' % make_move(b, sys.argv[2]))
    f.close()
    print(f"Time elapsed = {time()-start:.2f}s")
