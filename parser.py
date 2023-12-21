import nltk
import sys
import re

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

# The NONTERMINALS global variable should be replaced with a set of context-free grammar rules
# that, when combined with the rules in TERMINALS, allow the parsing of all sentences in the sentences/ directory.
# Each rules must be on its own line. Each rule must include the -> characters to denote which symbol is
# being replaced, and may optionally include | symbols if there are multiple ways to rewrite a symbol.
# You do not need to keep the existing rule S -> N V in your solution, but your first rule must begin with
# S -> since S (representing a sentence) is the starting symbol.
# You may add as many nonterminal symbols as you would like.
# Use the nonterminal symbol NP to represent a “noun phrase”, such as the subject of a sentence.

NONTERMINALS = """
S -> NP VP
CP -> S Conj S
AP -> A | A AP
PP -> P NP
NP -> N | D NP | AP NP | NP PP | N Adv
VP -> V | V NP | V NP PP | V Adv | V PP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():
    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    print(f"s={s}")

    # Attempt to parse sentence
    try:
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

        # print("Noun Phrase Chunks")
        # for np in np_chunk(tree):
        #     print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    return [
        w.lower()
        for w in nltk.word_tokenize(sentence)
        if bool(re.search("[a-zA-Z]", w))
    ]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
