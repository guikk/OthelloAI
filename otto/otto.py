import sys
import copy
from time import time
from estruturas import NoMax
sys.path.append('..')
from common import board


def make_move(the_board, color_str):
    """
    Returns the next move
    :return: (int, int)
    """
    color = board.Board.WHITE if color_str == 'white' else board.Board.BLACK

    raiz = NoMax(0, color, None, the_board, None)
    raiz.valor_max()
    no = raiz
    while no != None:
        print(no.altura, no.move, no.color, no.valor)
        no = no.next
    print("choice:", raiz.next.move)
    return raiz.next.move


if __name__ == '__main__':
    start = time()
    b = board.from_file(sys.argv[1])
    f = open('move.txt', 'w')
    f.write('%d,%d' % make_move(b, sys.argv[2]))
    f.close()
    print(f"Time elapsed = {time()-start:.2f}s")
