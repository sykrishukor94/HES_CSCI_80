import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    # allows using == to compare class objects https://www.pythontutorial.net/python-oop/python-__eq__/
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    # allows us to print class objects (not defining __str__ only prints pointer to the object)
    def __str__(self):
        return f"{self.cells} = {self.count}"

    # since __eq__ is implemented, we can use hash
    def __hash__(self):
        return hash(self.count)

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # we know all cells are mines if len(cell) == count
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # Cells are safe if count == 0
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Remove cell containing mine (leaving it unmarked) and decrement count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # a safe cell can be removed from consideration
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark move made as safe since runner will inform of loss
        self.mark_safe(cell)
        self.moves_made.add(cell)

        # Appends neighbors as sentences and updates this into self.knowledge
        sentence = self.neighbors(cell, count)
        self.knowledge.append(sentence)

        # Loop through updated self.knowledge to mark mines and safes
        for sentence in self.knowledge:

            if sentence.known_mines():
                for cells in sentence.known_mines().copy():
                    self.mark_mine(cells)

            if sentence.known_safes():
                for cells in sentence.known_safes().copy():
                    self.mark_safe(cells)

        # compare one sentence to other sentences in self.knowledge
        for i in self.knowledge.copy():
            for j in self.knowledge.copy():
                superset, count_1 = i.cells, i.count
                subset, count_2 = j.cells, j.count

                # ignore the same sentences
                if subset == superset:
                    continue

                # if a superset contains a subset, update the difference
                if subset.issubset(superset):
                    updated_sentence = Sentence(
                        superset.difference(subset), count_1 - count_2)
                    self.knowledge.append(updated_sentence)

        # clean duplicate sentences
        self.knowledge = list(set(self.knowledge))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # look into safe cells
        for move in self.safes:
            # if move hasn't been used
            if move not in self.moves_made:
                return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # initialize variable
        available_moves = set()

        # traverse through all cells and mark ALL unexplored mines that are NOT mines
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.mines and (i, j) not in self.moves_made:
                    available_moves.add((i, j))

        # No moves left
        if len(available_moves) == 0:
            return None

        # Return random available cells
        move = random.choice(tuple(available_moves))
        return move


    def neighbors(self, cell, count):

        # initialize variable
        neighbor_cells = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the given cell itself
                if (i, j) == cell:
                    continue
                # Add undetermined cells only within the board
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        count -= 1
                        continue

                    if (i, j) not in self.safes or (i, j) not in self.moves_made:
                        neighbor_cells.add((i, j))

        return Sentence(neighbor_cells, count)
