import nltk
import sys
from nltk.tokenize import word_tokenize
from nltk.tree import *
'''
 Notice that Adj is a nonterminal symbol that generates adjectives, 
 Adv generates adverbs, 
 Conj generates conjunctions, 
 Det generates determiners, 
 N generates nouns (spread across multiple lines for readability), 
 P generates prepositions, and 
 V generates verbs.
 '''
# Conj -> 'and' | 'as' | 'because' | 'but' | 'for' | 'just as' | 'or'
# Conj -> 'neither' | 'or' | 'not only' | 'so' | 'whether' | 'yet'

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

'''    
Subject–Verb                -> N-V       (She is playing)
Subject–Verb–Object         -> N-V-N     (She is playing a piano.)
Subject–Verb–Adjective      -> N-V-Adj    (He is very handsome)
Subject–Verb–Adverb         -> (Det)N-V-Adv  (The girl walked away)
Subject–Verb–Noun           -> N-V-N     (The professor at the university is an intelligent woman
'''
# S -> NP VP
# AP -> A | A AP  # A = Adj
# NP -> N | D NP | AP NP | N PP # D = Det
# PP -> P NP
# VP -> V | V NP | V NP PP

NONTERMINALS = """
S -> NP VP | NP VP Adv | NP VP Adj

PP -> P NP 
NP ->  N | Det Adj N | Adj NP | N PP | Conj NP  | NP VP | Det NP
VP -> V | V NP | V NP PP | Conj VP


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

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    words = word_tokenize(sentence)
    # print(words)

    list_to_return = []

    for word in words:
        word = word.lower()
        if word.islower():
            list_to_return.append(word)

    # print(list_to_return)
    return list_to_return


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    # sent = tree.pos()
    """

    returning = []
    for s in tree.subtrees(lambda tree: tree.height() <= 3):
        if s.label() == "NP":
            returning.append(s)

    return returning


if __name__ == "__main__":
    main()
