#searchBiDir.py
#CPOFFWEBSTER



from display import Displayable, visualize


class BidirectionalSearcher(Displayable):
    """returns a searcher for a problem.
    Paths can be found by repeatedly calling search().
    This does depth-first search unless overridden
    """

    def __init__(self, problem):
        """creates a searcher from a problem
        """
        self.problem = problem
        self.initialize_frontier()
        self.initialize_f_frontier()
        self.initialize_b_frontier()  # frontier for the bidirectional (back starting)
        self.num_f_expanded = 0
        self.num_b_expanded = 0
        self.add_to_f_frontier(Path(problem.start_node()))
        self.add_to_b_frontier(Path(problem.goal_node()))  # start state is the goal node
        super().__init__()
        self.max_display_level
        self.f_closed = set()
        self.b_closed = set()
        self.new_path = []

    def initialize_frontier(self):
        self.frontier = []

    def initialize_f_frontier(self):
        self.f_frontier = []

    def initialize_b_frontier(self):
        self.b_frontier = []

    def empty_f_frontier(self):
        return self.f_frontier == []

    def empty_b_frontier(self):
        return self.b_frontier == []

    def add_to_f_frontier(self, path):
        self.f_frontier.append(path)

    def add_to_b_frontier(self, b_path):
        self.b_frontier.append(b_path)

    def merge_path(self, f_path, b_path):
        forward = Path.arcs(f_path)
        backward = Path.arcs_reversed(b_path)
        for x in forward:
            self.new_path.append(x)
        for x in backward:
            self.new_path.append(x)
        return self.new_path

    @visualize
    def search(self):
        """returns (next) path from the problem's start node
        to a goal node.
        Returns None if no path exists.
        """
        while not self.empty_f_frontier() and not self.empty_b_frontier():
            path = self.f_frontier.pop(0)
            if path.end() in self.b_closed:
                # print("intersect beforehand")
                path.list = self.merge_path(path, b_path)
                self.solution = path.list
                return path.list

            b_path = self.b_frontier.pop(0)
            if path.end() == b_path.end():
                # print("intersection on")
                path.list = self.merge_path(path, b_path)
                self.solution = path.list
                return path.list

            if path.end() not in self.f_closed:
                self.display(2, "Expanding:", path, "(cost:", path.cost, ")")

                self.f_closed.add(path.end())  # add path to the visited list
                self.num_f_expanded += 1

                if self.problem.is_goal(path.end()):  # solution found
                    self.display(1, self.num_f_expanded, "paths have been expanded and",
                                 len(self.f_frontier + self.b_frontier), "paths remain in the frontier")
                    self.solution = path  # store the solution found
                    return path
                else:
                    neighs = self.problem.neighbors(path.end())
                    self.display(3, "Neighbors are", neighs)
                    for arc in reversed(neighs):
                        self.add_to_f_frontier(Path(path, arc))
                    self.display(3, "Frontier:", self.f_frontier)

            if b_path.end() not in self.b_closed:
                self.display(2, "Expanding:", b_path, "(cost:", b_path.cost, ")")
                self.b_closed.add(b_path.end())  # add path to the visited list
                self.num_b_expanded += 1

                if self.problem.is_start(b_path.end()):  # solution found
                    self.display(1, self.num_b_expanded, "paths have been expanded and",
                                 len(self.b_frontier + self.f_frontier), "paths remain in the frontier")
                    self.solution = b_path
                    return b_path
                else:
                    neighs = self.problem.neighbors(b_path.end(), True)
                    self.display(3, "Neighbors are", neighs)
                    for arc in reversed(neighs):
                        self.add_to_b_frontier(Path(b_path, arc))
                    self.display(3, "Frontier:", self.f_frontier)

        self.display(1, "No (more) solutions. Total of",
                     self.num_f_expanded, "paths expanded.")


import heapq  # part of the Python standard library
from searchProblem import Path