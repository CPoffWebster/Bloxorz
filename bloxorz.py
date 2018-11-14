#Bloxorz

import io
from searchProblem import Path


class Board(object):
    """
    Simple representation of a Bloxorz board.

    """

    def __init__(self, rows):
        """
        Construction is done with a sequence of sequences; they must all be the
        same length.
        """
        valid_board_chars = ('S', 'X', 'G', 'W', 'O')
        y_dim = len(rows)
        assert y_dim != 0, str(y_dim)
        x_dim = len(rows[0])
        assert x_dim != 0, str(x_dim)
        self.rows = list()
        start_count = goal_count = 0
        for y, row in enumerate(rows):
            assert len(row) == x_dim, str((x_dim, len(row)))
            for x, tile in enumerate(row):
                if tile not in valid_board_chars:
                    raise ValueError('expected tile in %s, got %s' % (valid_board_chars, tile))
                if tile == 'G':
                    goal_count += 1
                    self.goal = x, y
                elif tile == 'S':
                    start_count += 1
                    self.start = x, y
            self.rows.append(tuple(row))
        self.x_dim, self.y_dim = x + 1, y + 1
        if goal_count != 1:
            raise ValueError('expected exactly one goal tile')
        if start_count != 1:
            raise ValueError('expected exactly one start tile')

    def on_board(self, square):
        """
        Determine if *square* (x, y) is on the board, which means also not on a
        void position.

        """
        x, y = square
        return x >= 0 and y >= 0 and x < self.x_dim and y < self.y_dim and self.rows[y][x] != 'O'

    def legal_position(self, pos):
        """
        Determine whether *pos* is a legal position on this board.
        A position is a pair of pairs.
        """
        # Unpacking like this will also check that pos has the right structure
        ((ax, ay), (bx, by)) = a_pos, b_pos = pos
        # Off board
        if not (self.on_board(a_pos) and self.on_board(b_pos)): return False

        # Upright on weak square
        if (ax, ay) == (bx, by) and self.rows[ay][ax] == 'W': return False

        return True

    HEADER_STRING = 'BLOX'
    CURRENT_VERSION = '1'
    SUPPORTED_VERSIONS = (CURRENT_VERSION,)

    @staticmethod
    def read_board(file):
        """
        Read a board from a file.  The format is show below; whitespace is used to separate tokens.
        Note that the first line in the file must be a header line with a supported version number.
        """

        header_info = file.readline().split()
        if len(header_info) != 2 or header_info[0] != Board.HEADER_STRING or header_info[
            1] not in Board.SUPPORTED_VERSIONS:
            raise ValueError("expected valid board file header, but got %s" % (header_info,))

        dimensions = file.readline().split()
        if len(dimensions) != 2:
            raise ValueError("expected 2 board dimensions, but got %s" % (dimensions,))
        # This conversion will raise an error if either string cannot be converted to an int
        x_dim, y_dim = int(dimensions[0]), int(dimensions[1])
        if x_dim <= 0 or y_dim <= 0:
            raise ValueError("expected positive board dimensions, but got %s" % ((x_dim, y_dim),))

        rows = list()
        for row_idx, line in enumerate(file):
            tiles = line.split()
            if len(tiles) != x_dim:
                raise ValueError("expected row with %d tiles, but got %s in row %d" % (x_dim, tiles, row_idx))
            rows.append(tiles)
        if row_idx != y_dim - 1:
            raise ValueError("expected %d rows but got %d" % (y_dim, row_idx))
        return Board(rows)
    # End class Board


ACTIONS = tuple(('U', 'D', 'L', 'R'))

reverse_action_dict = {'U': 'D', 'D': 'U', 'L': 'R', 'R': 'L'}


def next_position(pos, action, forward=True):
    """
    Given a position *pos* for the 1x2 block in the form of a pair of pairs and
    and *action* from the set of legal actions, return the resulting position.

    >>> up0 = ((0, 0), (0, 0))
    >>> [(action, next_position(up0, action)) for action in ACTIONS]  #doctest:
    [('U', ((0, -2), (0, -1))), ('D', ((0, 1), (0, 2))), ('L', ((-2, 0), (-1, 0))), ('R', ((1, 0), (2, 0)))]

    >>> vert0 = ((0, 0), (0, 1))
    >>> [(action, next_position(vert0, action)) for action in ACTIONS]  #doctest:
    [('U', ((0, -1), (0, -1))), ('D', ((0, 2), (0, 2))), ('L', ((-1, 0), (-1, 1))), ('R', ((1, 0), (1, 1)))]

    >>> horiz0 = ((0, 0), (1, 0))
    >>> [(action, next_position(horiz0, action)) for action in ACTIONS]  #doctest:
    [('U', ((0, -1), (1, -1))), ('D', ((0, 1), (1, 1))), ('L', ((-1, 0), (-1, 0))), ('R', ((2, 0), (2, 0)))]

    >>> horiz1 = ((1, 1), (2, 1))
    >>> [(action, next_position(horiz1, action)) for action in ACTIONS]  #doctest:
    [('U', ((1, 0), (2, 0))), ('D', ((1, 2), (2, 2))), ('L', ((0, 1), (0, 1))), ('R', ((3, 1), (3, 1)))]

    >>> horiz1 = ((1, 1), (2, 1))
    >>> [(action, next_position(horiz1, action, False)) for action in ACTIONS]  #doctest:
    [('U', ((1, 2), (2, 2))), ('D', ((1, 0), (2, 0))), ('L', ((3, 1), (3, 1))), ('R', ((0, 1), (0, 1)))]

    """
    # Note, if we want to allow blocks to split up, we will have to rework this
    # function completely

    # 1. Start standing strait (as a boolean)
    # 2. If it moves in any direction then change boolean to right_left or up_down
    # 3. Depending on where it goes activate another boolean to figure out up/down left/right movement
    # 4. Do all this within if loops

    # **If strait - one block is moved over one, one block is moved over two
    # strait:
    #     U - (x, y-2), (x, y-1)
    #     D - (x, y+1), (x, y+2)
    #     L - (x-2, y), (x-1, y)
    #     R - (x+1, y), (x+2, y)

    # **if sideways - Either stay sideways or stand up strait
    # sideways(right/left):
    #     U - (x, y-1), (x, y-2)  to strait
    #     D - (x, y+2), (x, y+1)  to strait
    #     L - (x-1, y), (x-1, y)
    #     R - (x+1, y), (x+1, y)

    # **if sideways - Either stay sideways or stand up strait
    # sideways(up/down):
    #     U - (x, y-1), (x, y-1)
    #     D - (x, y+1), (x, y+1)
    #     L - (x-1, y), (x-2, y)  to strait
    #     R - (x+2, y), (x+1, y)  to strait

    act = action  # if the action is backwards than switch the action
    if forward is False:
        if act is 'U':
            act = 'D'
        elif act is 'D':
            act = 'U'
        elif act is 'R':
            act = 'L'
        elif act is 'L':
            act = 'R'

    if act is 'U':  # up
        x1, y1 = pos[0]
        x2, y2 = pos[1]

        if x1 == x2 and y1 == y2:  # strait: both points(blocks) are equal
            # up for strait
            # (x, y-2), (x, y-1)
            newy1, newy2 = int(y1-2), int(y2 - 1)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition

        elif x1 == x2 and y1 != y2:  # right/left: xs not equal but ys are
            # up for right/left
            # (x, y-1), (x, y-2)  to strait
            newy1, newy2 = int(y1 - 1), int(y2 - 2)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition

        elif x1 != x2 and y1 == y2:  # up/down: ys not equal but xs are
            # up for up/down
            # (x, y-1), (x, y-1)
            newy1, newy2 = int(y1 - 1), int(y2 - 1)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition


    if act is 'D':  # down
        x1, y1 = pos[0]
        x2, y2 = pos[1]

        if x1 == x2 and y1 == y2:  # strait: both points(blocks) are equal
            # down for strait
            # (x, y+1), (x, y+2)
            newy1, newy2 = int(y1+1), int(y2+2)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition

        elif x1 == x2 and y1 != y2:  # right/left: xs not equal but ys are
            # up for right/left
            # (x, y+2), (x, y+1)  to strait
            newy1, newy2 = int(y1 + 2), int(y2 + 1)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition

        elif x1 != x2 and y1 == y2:  # up/down: ys not equal but xs are
            # up for up/down
            # (x, y+1), (x, y+1)
            newy1, newy2 = int(y1 + 1), int(y2 + 1)
            newPosition = ((x1, newy1), (x2, newy2))

            return newPosition


    if act is 'L':  # left
        x1, y1 = pos[0]
        x2, y2 = pos[1]

        if x1 == x2 and y1 == y2:  # strait: both points(blocks) are equal
            # left for strait
            # (x-2, y), (x-1, y)
            newx1, newx2 = int(x1-2), int(x2-1)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition

        elif x1 == x2 and y1 != y2:  # right/left: xs not equal but ys are
            # up for right/left
            # (x-1, y), (x-1, y)
            newx1, newx2 = int(x1 - 1), int(x2 - 1)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition

        elif x1 != x2 and y1 == y2:  # up/down: ys not equal but xs are
            # up for up/down
            # (x-1, y), (x-2, y)  to strait
            newx1, newx2 = int(x1 - 1), int(x2 - 2)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition


    if act is 'R':  # right
        x1, y1 = pos[0]
        x2, y2 = pos[1]

        if x1 == x2 and y1 == y2:  # strait: both points(blocks) are equal
            # right for strait
            # (x+1, y), (x+2, y)
            newx1, newx2 = int(x1+1), int(x2+2)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition

        elif x1 == x2 and y1 != y2:  # right/left: xs not equal but ys are
            # up for right/left
            # (x+1, y), (x+1, y)
            newx1, newx2 = int(x1 + 1), int(x2 + 1)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition

        elif x1 != x2 and y1 == y2:  # up/down: ys not equal but xs are
            # up for up/down
            # (x+2, y), (x+1, y)  to strait
            newx1, newx2 = int(x1 + 2), int(x2 + 1)
            newPosition = ((newx1, y1), (newx2, y2))

            return newPosition
