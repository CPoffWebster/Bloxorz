##############################################################################
#
# File:         driver.py
# Date:         Tue 11 Sep 2018  11:33
# Author:       Ken Basye
# Description:  Driver for testing bloxorz algorithms
#
##############################################################################

"""
Driver for testing bloxorz algorithms

"""

from bloxorz_problem import BloxorzProblem
from bloxorz import Board
import searchGeneric
from searchGeneric import AStarMultiPruneSearcher
import searchBFS
import BFSMultiPruneSearcher
import searchBiDir
import os
import glob

if __name__ == "__main__":
    # board_names = glob.glob("charliePW/*.blx")  # glob.glob("boards/*.blx")
    board_names = glob.glob("boards/*.blx")
    for board_name in board_names:
        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)
        bp0 = BloxorzProblem(board)
        # A*, BFS with multipath pruning, A* with multipath pruning, and bidirectional search with multipath pruning
        # searcher = searchBFS.BFSSearcher(bp0)
        # searcher = searchGeneric.AStarSearcher(bp0)  # A*
        # searcher = BFSMultiPruneSearcher.BFSMultiPruneSearcher(bp0)  # BFSMultiPrune
        # searcher = searchGeneric.AStarMultiPruneSearcher(bp0)  # A*MultiPrune
        searcher = searchBiDir.BidirectionalSearcher(bp0)  # BiDirectional
        result = searcher.search()
        if result is None:
            print("For board %s, found no solution!" % (board_name,))
            continue

        sequence = [arc.action for arc in result]  # for bidirectional searcher
        # sequence = [arc.action for arc in result.arcs()]
        print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_f_expanded + searcher.num_b_expanded))  # for bidirectional seracher
        # print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))

    print(); print()


