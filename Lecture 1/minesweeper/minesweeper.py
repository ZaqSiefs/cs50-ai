import copy
import itertools
import random

# 19/25 solution, could not do better in an evening. Might come back to this.
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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        known_mines = set()

        if self.count == len(self.cells):
            known_mines.update(copy.deepcopy(self.cells))
        
        return known_mines

    def known_safes(self):
        known_safes = set()

        if self.count == 0:
            known_safes.update(copy.deepcopy(self.cells))
        
        return known_safes

    def mark_mine(self, cell):
        if cell in self.cells:
            self.count -= 1
            self.cells.discard(cell)

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.discard(cell)


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
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        cells = set()
        touching_cells = set()
        current_count = copy.deepcopy(count)

        # Iterate through all the cells touching the given cell, and add the ones that are not included in moves_made OR the cell itself to touching_cells
        for i in range(0, 3):
            for j in range (0, 3):
                y = i + cell[0] - 1
                x = j + cell[1] - 1
                if x >= 0 and x < self.width and y >=0 and y < self.height and (y, x) != cell and (y, x) not in self.moves_made:
                    touching_cells.add((y, x))
        
        for touching in touching_cells:
            if touching in self.mines:
                current_count -= 1
            if touching not in self.mines | self.safes:
                cells.add(touching)

        sentence = Sentence(touching_cells, current_count)

        self.knowledge.append(sentence)

        # 4)
        for s in self.knowledge:
            mines = s.known_mines()
            safes = s.known_safes()
            if mines:
                for mine in mines:
                    self.mark_mine(mine)
            
            if safes:
                for safe in safes:
                    self.mark_safe(safe)
        
        # 5)
        # travel through each sentence in the knowledge base and compare each one to eachother.  
        for i, sentencei in enumerate(self.knowledge):
            for j, sentencej in enumerate(self.knowledge):
                # if one sentence is a subset of another AND they are not the same sentence, create and append a new sentence that contains only the cells NOT within the subset, and subtract the subset count. 
                # This is following the logic from the final inference shown in the project's background.
                if sentencei.cells in sentencej.cells and i != j:
                    newSentence = Sentence(set(sentencej.cells - sentencei.cells), sentencej.count - sentencei.count)
                    self.knowledge.append(newSentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if self.safes:
            for cell in self.safes:
                if cell not in self.moves_made:
                    return copy.deepcopy(cell)
            
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        if not self.moves_made: 
            return (random.randint(0, self.height - 1), random.randint(0, self.width - 1))

        board = set()
        for i in range(0, self.height):
            for j in range(0, self.width):
                board.add((i, j))
        
        uncertain_cells = (board - self.moves_made) - self.mines

        if uncertain_cells:
            return uncertain_cells.pop()
        
        return None
                