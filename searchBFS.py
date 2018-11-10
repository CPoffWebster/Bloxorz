# BFS.SEARCHER
#CPOFFWEBSTER



from display import Displayable, visualize


class BFSSearcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """

    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.problem = problem
        self.initialize_frontier()
        self.num_expanded = 0
        self.add_to_frontier(Path(problem.start_node()))
        super().__init__()

    def initialize_frontier(self):
        self.frontier = []

    def empty_frontier(self):
        return self.frontier == []

    def add_to_frontier(self, path):
        self.frontier.append(path)

    @visualize
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node.
        Returns None if no path exists.
        """
        while not self.empty_frontier():
            path = self.frontier.pop(0)  # dir([])    pop
            self.display(2, "Expanding:", path, "(cost:", path.cost, ")")
            self.num_expanded += 1
            if self.problem.is_goal(path.end()):  # solution found
                self.display(1, self.num_expanded, "paths have been expanded and",
                             len(self.frontier), "paths remain in the frontier")
                self.solution = path  # store the solution found
                return path
            else:
                neighs = self.problem.neighbors(path.end())
                self.display(3, "Neighbors are", neighs)
                for arc in reversed(neighs):
                    self.add_to_frontier(Path(path, arc))
                self.display(3, "Frontier:", self.frontier)
        self.display(1, "No (more) solutions. Total of",
                     self.num_expanded, "paths expanded.")


import heapq  # part of the Python standard library
from searchProblem import Path