from generate_submitted import *

def test_0():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure0.txt"
    words = path + r"\words0.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test0: ")
    creator.print(assignment)

def test_1():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure1.txt"
    words = path + r"\words1.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test1: ")
    creator.print(assignment)

def test_2():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure2.txt"
    words = path + r"\words2.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test2: ")
    creator.print(assignment)

# 3 spaces, 1 unconnected
def test_3():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure3.txt"
    words = path + r"\words2.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test3: ")
    creator.print(assignment)

def test_4():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure4.txt"
    words = path + r"\words2.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test3: ")
    creator.print(assignment)

def test_5():
    path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    structure = path + r"\structure0.txt"
    words = path + r"\words3.txt"
    output = path + r"\results"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    print("test5: ")
    creator.print(assignment)


def main():
    # test_0()
    test_1()
    test_2()
    test_3()
    test_5()

    # path = r"C:\Users\sykri\PycharmProjects\CSCI_80\Week_3\crossword\data"
    # structure = path + r"\structure2.txt"
    # words = path + r"\words2.txt"
    # output = path + r"\results"
    #
    # # Generate crossword
    # crossword = Crossword(structure, words)
    # creator = CrosswordCreator(crossword)
    # assignment = creator.solve()
    # creator.print(assignment)
    #
    # print("final assignment")
    # for i in assignment:
    #     print(i, assignment[i])


    # TESTING_____________________________________

    # # Test enforce_node_consistency
    # print(creator.domains)
    # creator.enforce_node_consistency()
    # for i in creator.domains:
    #     print(f"{i}: {creator.domains[i]}")

    # for i in crossword.variables:
    #     print(f"var i: {i}")
    #     for j in crossword.variables:
    #         if i == j:
    #             continue
    #         print(f"    var j: {j} : {crossword.overlaps[i, j]}")


    # # Test ac3

    # print(creator.ac3(None))
    # for i in creator.domains:
    #     print(f"{i}: {creator.domains[i]}")



    # for i in crossword.variables:
    #     print(crossword.neighbors(i))
    #     print(crossword.neighbors(i) - {Variable(0, 1, 'across', 3)})

    # # Test revise
    # x, y = Variable(0, 1, 'across', 3), Variable(0, 1, 'down', 5)
    # print(crossword.overlaps[x, y])
    #
    # creator.revise(x, y)
    # print(creator.domains)

    # print(crossword.neighbors(y))

    # # Test select_unassigned_variable(assignment)
    # d = {Variable(0, 1, 'down', 5) : {'EIGHT', 'SEVEN', 'THREE'}}
    # print(creator.select_unassigned_variable(dict()))

    # # Test order_domain_variable(var, assignment)
    # Structure0
    # var = Variable(0, 1, 'down', 5)
    # d = dict()
    # Structure1
    # var = Variable(2, 1, 'down', 5)
    # d = {Variable(2, 1, 'across', 12) : {'SATISFACTION', 'DISTRIBUTION', 'INTELLIGENCE', 'OPTIMIZATION'}}
    # print(creator.order_domain_values(var, dict()))
    # print(var.length)

    # # Test consistent(assignment)
    # empty dict
    # print(creator.consistent(dict()))




    # print(f"board dimension is {crossword.height} x {crossword.width} (H x W) \n")

    # Printing variables
    # vars = list(crossword.variables)
    # for v in vars: # turns set into list
    #     print(v)
    # print(list(vars)[0]) # Variable(row, col, direction, len) # gotta turn set into list

    # print specific overlaps
    # print(crossword.overlaps[vars[0], vars[1]])
    # print(crossword.neighbors(vars[1]))



    # END TESTING________________________________

if __name__ == "__main__":
    main()