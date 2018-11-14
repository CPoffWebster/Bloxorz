from searchProblem import Arc, Search_problem
import searchBFS
import searchBiDir
import BFSMultiPruneSearcher
import io
from bloxorz import Board
from bloxorz import next_position


class BloxorzProblem(Search_problem):

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
