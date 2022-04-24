import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""
# from lecture
# | Adv V NP | V Det NP | V Conj VP  NP
# | NP VP Conj NP VP
# AdjN -> Adj | Adj AdjN
# AdvV -> Adv | Adv AdvV
# DetN -> Det | Det AdjP
NONTERMINALS = """
S -> NP VP | S Conj S | S Conj VP NP

AdjP -> Adj | Adj AdjP
AdvV -> Adv | Adv AdvV | VAdv Adv | VAdv
PP -> P NP
NP -> N | Det NP | AdjP NP | N PP | N VP | NAdv
VP -> V | AdvV | V NP | VP PP | V NP PP | V NP VP | V DetN | Conj V

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # # If filename specified, read sentence from file
    # if len(sys.argv) == 2:
    #     with open(sys.argv[1]) as f:
    #         s = f.read()
    #
    # # Otherwise, get sentence as input
    # else:
    #     s = input("Sentence: ")
    #
    # # Convert input into list of words
    # s = preprocess(s)
    #
    # # Attempt to parse sentence
    # try:
    #     print(grammar.productions())
    #     trees = list(parser.parse(s))
    # except ValueError as e:
    #     print(e)
    #     return
    # if not trees:
    #     print("Could not parse sentence.")
    #     return
    #
    # # Print each tree with noun phrase chunks
    # for tree in trees:
    #     tree.pretty_print()
    #
    #     print("Noun Phrase Chunks")
    #     for np in np_chunk(tree):
    #         print(" ".join(np.flatten()))

    #-----------------------------
    print(grammar.productions())
    sentences = open("C:/Users/sykri/PycharmProjects/CSCI_80/Week_6/parser/sentences.txt", 'r')
    print(sentences)
    for i, s in enumerate(sentences.readlines()):
        # Convert input into list of words
        print(f"Sentence {i+1}")
        s = preprocess(s)

        # Attempt to parse sentence
        try:
            trees = list(parser.parse(s))
        except ValueError as e:
            print(e)
            return
        if not trees:
            print(f"Could not parse sentence {i+1}.")
            return

        # Print each tree with noun phrase chunks
        for tree in trees:
            tree.pretty_print()
        #
        #     print("Noun Phrase Chunks")
        #     for np in np_chunk(tree):
        #         print(" ".join(np.flatten()))

    #-----------------------------



def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = remove_punc(sentence)

    words = list()
    print("input: ", sentence.split(" "))
    for word in sentence.split(" "):
        word = word.strip()
        if word.isalnum():
            words.append(word)
    print("output: ", words)

    return words

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    raise NotImplementedError

def remove_punc(sentence):
    # initializing punctuations string
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    # Removing punctuations in string
    # Using loop + punctuation string
    for c in sentence:
        if c in punc:
            sentence = sentence.replace(c, "")

    return sentence


if __name__ == "__main__":
    main()
