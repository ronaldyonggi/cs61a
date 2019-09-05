import sys
from max_parse import *
from ucb import main

def words(t):
    """ Yield the words in t"""
    if type(t) == Leaf: # if t is a leaf
        yield t.word# Then the words in that tree are just the word at the leaf
    else: # Otherwise
        for b in t.branches: # Go through all the branches
            for w in words(b): # For every result of calling the words function on every branch
                yield w # Yield that result

def extract_modal(t):
    """ Delete and return the arg of a modal verb phrase"""
    if type(t) == Leaf: # If t is a leaf, then there's no `MD`
        return None
    # Recursively searches t to find when t has 2 branches where the left branch is tagged 'MD'
    if len(t.branches) == 2 and t.branches[0].tag == 'MD':
        modal, clause = t.branches # Grab the modal verb and the clause modified by the modal verb
        t.branches = modal # replace t.branches with the first branch 
        return clause # return the second branch, which is going to be moved to the front of the tree
    # If it's neither leaf nor a branch where the left branch is `MD`,
    # then recurse through all the branches in t
    for b in t.branches:
        clause = extract_modal(b)
        #If we find a clause that contains argument to a modal verb, then return it
        if clause is not None:
            return clause
    return None #Otherwise, return None

def yoda_transform(t):
    """ Place the clause of a modal verb at the front """
    # First get the clause, the argument of the modal verb phrase, by calling extract_modal on the original tree
    clause = extract_modal(t)
    if clause is not None: # If clause is not None, there's a modal verb present!
        return Tree(t.tag, [clause, Leaf(',', ',')] + t.branches)
    else: # If there's no modal verb
        return t # Then we don't do anything

@main
def run():
    for line in sys.stdin:
        tree = parse(line, 1, list)[0] # parse the tree from the line
        print_tree(tree)
        yoda = yoda_transform(tree) # perform the Yoda transform
        print_tree(yoda) # print the transformed tree
        transformed = ' '.join(words(yoda)) # Join the words of that tree together
        print('Yoda would say, "{}"'.format(transformed))