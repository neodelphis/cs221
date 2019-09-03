# -*- coding: utf-8 -*-
import shell
import util
import wordsegUtil

############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

# n         : nb de caractères dans query
# state     : position du curseur sur la chaîne de caractères
#
# state     : liste de mots comme sous ensemble des segmentations possibles de query jsuqu'à la lettre 
#            d'indice k <= n
# successeur: liste incluant un nouveau mot du corpus dans [l_k, ..., l_n], commençant à l_k
# coût de passage u(nouveau mot)

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost
        self.minCost = unigramCost(self.query)
        self.n = len(self.query)

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # start state = position initiale du curseur sur la chaîne de caractères
        return 0 

        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)

        # # Fin si le total des longueurs des mots de state est n
        # length = sum([len(word) for word in state])

        # Fin si le curseur est sur n
        return state == self.n

        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 7 lines of code, but don't worry if you deviate from this)
        result = []
        # Ce sera une liste de tuples (action, newState, cost)

        # Coût payé jusqu'à maintenant ## Pas calculé ici
        #past_cost = sum([self.unigramCost(word) for word in state])

        # Indice de la lettre à laquelle on se trouve : state
        i_init = state

        # On parcourt toutes les lettres restantes à la recherche de nouveaux mots
        for i_end in range(i_init+1, self.n+1):
            action = i_end
            word = self.query[i_init:i_end]
            # word est dans le corpus? En fait ici tous les mots n'appartenant pas au corpus ont 
            # un coût très élévé, donc on ne gère pas particulièrement ce point
            new_state = i_end
            cost = self.unigramCost(word)
            result.append((action, new_state, cost))
        return result


def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=3)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    
    print('-'*80)
    print (ucs.actions)
    words = []
    init_position = 0
    for end_position in ucs.actions:
        words.append(query[init_position:end_position])
        print(words)
        init_position = end_position
    print('-'*80)
    return ' '.join(words)

    #raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem

class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

    def succAndCost(self, state):
        # BEGIN_YOUR_CODE (our solution is 14 lines of code, but don't worry if you deviate from this)
        raise Exception("Not implemented yet")
        # END_YOUR_CODE

def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################

if __name__ == '__main__':
    shell.main()
