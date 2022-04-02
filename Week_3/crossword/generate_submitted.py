import sys
import random
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        # for i in self.domains:
        #     print(f"{i}: {self.domains[i]}")
        self.ac3()
        # for i in self.domains:
        #     print(f"{i}: {self.domains[i]}")
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        """
        # iterate through every variable in self.domains
        for var in self.domains:
            # iterate through COPIED dict for every key's values. NOTE: iteration error if dict not copied
            for word in self.domains[var].copy():
                # keep words with correct lengths from ORIGINAL dictionary
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.

        :param Variable x : Variable that needs to be made arc consistent in reference to y
        :param Variable y : Variable with values to be cross-checked against by x
        :return True if self.domain revise, False otherwise

        """

        # return False unless there are overlaps
        if self.crossword.overlaps[x, y]:

            # get x, y overlaps, copy of x's domain values, and letters at y's overlaps
            i, j = self.crossword.overlaps[x, y]
            var_x = self.domains[x].copy()
            d_y = [s[j] for s in self.domains[y]]

            # Loop through every word in x.domain's copy - error if not copied
            for word in var_x:
                # if letters at x[i], y[j] don't overlap, remove word in x's domain
                if word[i] not in set(d_y):
                    self.domains[x].remove(word)

            # only return True if words were deleted (original != copy), False otherwise
            if len(self.domains[x]) != len(var_x):
                return True

        # return bool value
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        :param arcs : list containing tuples (x, y) of overlapping variables
        :return True : if arc consistency is enforced and no domains are empty;
        :return False : if one or more domains end up empty.
        """

        # get all arcs in the problem if None, otherwise, use one provided
        if arcs is None:
            q = list()
            for x in self.crossword.variables:
                for y in self.crossword.variables:
                    if x == y or self.crossword.overlaps[x, y] is None:
                        continue
                    q.append((x, y))
        else:
            q = list(arcs)

        # main loop updating all arcs until binary constraints updated
        while len(q) >= 1:
            x, y = q.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    q.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        :return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); False otherwise.
        """
        # assignment is complete if all variables are assigned a value
        for i in self.crossword.variables:
            if i not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        :param dict() assignment : contains {Variable() : str(words)}
        :return True or False
        """

        # helper function check for conflicting char overlaps
        def overlapping_chars(this_var):
            # iterate through var.neighbors in assignment (if it exists)
            for other_var in assignment:
                if other_var == this_var:
                    continue

                # returns False for conflicting chars at overlaps
                if other_var in self.crossword.neighbors(this_var):
                    x, y = self.crossword.overlaps[this_var, other_var]
                    s_x = assignment[this_var]
                    s_y = assignment[other_var]

                    if s_x[x] != s_y[y]:
                        return False

            return True

        # initialize dict of assignment's {word: var}
        checked = dict()

        for var in assignment:
            # returns false if assignment {var: word}
            #   1)word isn't unique OR
            #   2)word has wrong length OR
            #   3)word has contradicting char
            if assignment[var] in checked \
                    or len(assignment[var]) != var.length \
                    or not overlapping_chars(var):
                return False

            # update dictionary with assignment's {word: var}
            checked[assignment[var]] = var

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.

        :param Variable() var : Variable obj with values to sort
        :param dict() assignment : assigned {variable: value}
        :return list() of var ordered values

        """

        # helper function to score least constraining values of overlapping neighbors
        def get_lcv(val):
            # TODO: queue vars in entire crossword (e.g count multiple degrees of separation)
            # initialize count
            count = 0

            # iterate through neighbors, excluding ones in assignment
            for nb in self.crossword.neighbors(var):
                if nb not in assignment:
                    # get overlap coordinates and increment score for non-overlaps
                    x, y = self.crossword.overlaps[var, nb]
                    for word in self.domains[nb]:
                        if val[x] != word[y]:
                            count += 1

            return count

        # initialize list of values from var domains
        values = list(self.domains[var])

        # sort by LCV score in ascending order of most neighbor choices eliminated
        if len(values) > 1:
            values.sort(key=lambda k: get_lcv(k))

        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.

        :param assignment: to skip neighbors already assigned a value
        :return list() values: words ordered by least-constraining-value (LCV) heuristic

        """
        # list unassigned variables
        unassigned = list()
        for var in self.domains:
            if var not in assignment:
                unassigned.append(var)

        # only sort if there are multiple unassigned variables
        if len(unassigned) == 1:
            return unassigned[0]

        elif len(unassigned) > 1:
            # sort dictionary in desc order of neighbors, then in asc order of value length
            unassigned.sort(key=lambda k: len(self.crossword.neighbors(k)), reverse=True)
            unassigned.sort(key=lambda k: len(self.domains[k]))

            # assuming first item in unassigned is the best
            min_domains = len(self.domains[unassigned[0]])
            max_neighbors = len(self.crossword.neighbors(unassigned[0]))

            # keep variables with least values in domains
            for i, var in enumerate(unassigned):
                if len(self.domains[var]) > min_domains:
                    unassigned.remove(var)

            # keep variables with most neighbors
            for i, var in enumerate(unassigned):
                if len(self.crossword.neighbors(var)) < max_neighbors:
                    unassigned.remove(var)

            # return the final filtered list
            return random.choice(unassigned)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        :param: dict() assignment : a partial assignment for crossword
        :return None : if no assignment is possible
        :return result : breaks recursive loop
        :return dict() assignment : return completed assignment
        """

        # returns completed assignment once all variables in assignment
        if self.assignment_complete(assignment):
            return assignment

        # loop through {var : values} and recursively call backtrack to update assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                # interleave ac3 to make algorithm efficient
                self.ac3([(other_var, var) for other_var in self.crossword.neighbors(var)])
                # for i in new_assignment:
                #     print(i, new_assignment[i])
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        # result is none if assignment value is inconsistent or backtrack is None
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
