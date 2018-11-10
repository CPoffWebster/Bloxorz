##############################################################################
#
# File:         bloxorz_problem.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz search problem
#
##############################################################################

import cs210_utils
from searchProblem import Arc, Search_problem
import searchGeneric
import searchBFS
import searchBiDir
import BFSMultiPruneSearcher
# import searchBranchAndBound
import io
from bloxorz import Board
from bloxorz import next_position


class BloxorzProblem(Search_problem):
    """
    >>> board_string = (
    ... '''BLOX 1
    ... 5 3
    ... X X X O O
    ... S X G X O
    ... W W W W X
    ... ''')

    >>> fake_file = io.StringIO(board_string)
    >>> board0 = Board.read_board(fake_file)
    >>> bp0 = BloxorzProblem(board0)
    >>> bp0.start
    ((0, 1), (0, 1))

    >>> searcher = searchBFS.BFSSearcher(bp0)
    >>> path = searcher.search()  #doctest: +SKIP
    2507 paths have been expanded and 2399 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> a_pos, b_pos = path.end()   #doctest: +SKIP
    >>> a_pos == b_pos == board0.goal   #doctest: +SKIP
    True

    >>> searcher = BFSMultiPruneSearcher.BFSMultiPruneSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    16 paths have been expanded and 1 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    1259 paths have been expanded and 1880 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))


    >>> bp0.heuristic = bp0.heuristic1  #doctest: +SKIP
    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    845 paths have been expanded and 1369 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> bp0.heuristic = bp0.heuristic  #doctest: +SKIP
    >>> searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
    >>> path = searcher.search()   #doctest: +SKIP
    15 paths have been expanded and 1 paths remain in the frontier

    >>> path   #doctest: +SKIP
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

"""

    def __init__(self, board, heur=0):
        """
        Build a problem instance from a board
        """
        self.board = board
        self.start = (board.start, board.start)
        self.goal = (board.goal, board.goal)

    def start_node(self):
        """Returns start node"""
        return self.start

    def is_start(self, node):
        """Returns True if node is the start"""
        return node == self.start

    def goal_node(self):
        """Returns goal node"""
        return self.goal

    def is_goal(self, node):
        """Returns True if node is a goal"""
        return node == self.goal

    def neighbors(self, node, forward=True):
        """
        Given a node, return a sequence of Arcs usable
        from this node.

        append list of arcs that are possible, use already built code in bloxorz.py
        as well as look at what is "possible"
        """
        arcs = []

        ACTIONS = tuple(('U', 'D', 'L', 'R'))
        for x in range(0, 4):
            new_node = next_position(node, action=ACTIONS[x], forward=True)
            if self.board.legal_position(new_node):
                new_arc = Arc(node, new_node)
                arcs.append(new_arc)

        return arcs


    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        pos1, pos2 = node
        ((cx, cy), (cx2, cy2)) = pos1, pos2
        pos = self.goal
        (gx, gy) = pos[0]
        dx = abs(cx - gx)
        dy = abs(cy - gy)
        dx2 = abs(cx2 - gy)
        dy2 = abs(cy2 - gy)
        if dx + dy > dx2 + dy2:
            dist = dx + dy
        else:
            dist = dx2 + dy2
        heuristic = dist*(1.0 + 1/1000)
        return heuristic



if __name__ == '__main__':
    cs210_utils.cs210_mainstartup()
