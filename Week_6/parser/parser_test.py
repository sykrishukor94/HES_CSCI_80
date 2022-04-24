import parser

def main():

    # # If filename specified, read sentence from file
    # if len(sys.argv) == 2:
    #     with open(sys.argv[1]) as f:
    #         s = f.read()
    #
    # # Otherwise, get sentence as input
    # else:
    #     s = input("Sentence: ")




    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        print(grammar.productions())
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


if __name__ == "__main__":
    main()