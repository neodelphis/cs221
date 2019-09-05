# -*- coding: utf-8 -*-
import shell
import util
import wordsegUtil

SENTENCE_BEGIN = '-BEGIN-'


############################################################
# Problem 1b: Solve the segmentation problem under a unigram model

# n         : nb de caractères dans `query`
# state     : position du curseur sur la chaîne de caractères
# successor : nouvelle position du curseur
# coût de passage u(mot entre [state, successor])

class SegmentationProblem(util.SearchProblem):
    def __init__(self, query, unigramCost):
        self.query = query
        self.unigramCost = unigramCost
        self.n = len(self.query)

    def startState(self):
        # start state = position initiale du curseur sur la chaîne de caractères
        return 0 


    def isEnd(self, state):
        # Fin si le curseur est sur n
        return state == self.n


    def succAndCost(self, state):
        result = []
        # result: une liste de tuples (action, newState, cost)

        # Indice de la lettre à laquelle on se trouve : state
        # action = on se place à la lettre d'indice compris entre ]state, n]
        # on évalue le coût du mot entre state et action

        # On parcourt toutes les lettres restantes à la recherche de nouveaux mots
        for action in range(state+1, self.n+1):
            word = self.query[state:action]
            # word est dans le corpus? En fait ici tous les mots n'appartenant pas au corpus ont 
            # un coût très élévé, donc on ne gère pas particulièrement ce point
            cost = self.unigramCost(word)
            result.append((action, action, cost))  # (action, new_state, cost), et ici new_state = action

        return result


def segmentWords(query, unigramCost):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(SegmentationProblem(query, unigramCost))

    # Reconstruction des mots à partir de l'historique des positions de coupes stockées dans `actions`
    words = []
    init_position = 0
    for end_position in ucs.actions:
        words.append(query[init_position:end_position])
        init_position = end_position
    text = ' '.join(words)

    # Debug
    print('-'*80)
    print query
    print (ucs.actions)
    print(words)
    print text
    print('-'*80)

    return text


############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost
# Insertion de voyelles selon un coût de type bigramme
# state     : position, previous_word
#             position : position dans la liste des mots sans voyelles
#             previous_word
# action    : le mot selectionné pour les consonnes considérées
# coût      : b(previous_word, nouveau mot trouvé dans possibleFills)


class VowelInsertionProblem(util.SearchProblem):
    def __init__(self, queryWords, bigramCost, possibleFills):
        self.queryWords = queryWords
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        return 0, SENTENCE_BEGIN
        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        # Fin si on est positionné juste après le dernier mot de la liste words
        position, _ = state
        return position == len(self.queryWords)
        # END_YOUR_CODE

    def succAndCost(self, state):
        """
        output:
            result: une liste de tuples (action, newState, cost)
        """
        position, previous_word =  state
        result = []

        consonants = self.queryWords[position]
        possible_words = self.possibleFills(consonants)

        if len(possible_words) == 0:
            action = consonants
            newState = (position+1, consonants)
            cost = self.bigramCost(previous_word, consonants)
            result.append((action, newState, cost))
        else:
            for word in possible_words:
                action = word
                newState = (position+1, word)
                cost = self.bigramCost(previous_word, word)
                result.append((action, newState, cost))

        return result


        # END_YOUR_CODE

def insertVowels(queryWords, bigramCost, possibleFills):
    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    if len(queryWords) == 0:
        return ''    


    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve( VowelInsertionProblem(queryWords, bigramCost, possibleFills) )
    

    # Reconstruction des mots à partir de l'historique des mots stockés dans `actions`
    words = []
    for word in ucs.actions:
        words.append(word)
    text = ' '.join(words)

    # Debug
    print('-'*80)
    print queryWords
    print (ucs.actions)
    print text
    print('-'*80)

    return text


    # END_YOUR_CODE




############################################################
# Problem 2b: Solve the vowel insertion problem under a bigram cost

# n         : nb de caractères dans `query`
# state     : (position, previous_word) 
#             position du curseur sur la chaîne de caractères
#             précédent mot trouvé pour l'usage du bi-gramme
# successor : nouveau mot, nouvelle position du curseur
# action    : (new_position, chosen_word) 
#           : nouvelle position du curseur, mot choisi parmis ceux possibles
# coût de passage b(previous_word,chosen_word)

class VowelInsertionProblem__plutot_pb_3b(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        self.n = len(self.query)

    def startState(self):
        # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
        # start state = position initiale du curseur sur la chaîne de caractères
        return 0, SENTENCE_BEGIN

        # END_YOUR_CODE

    def isEnd(self, state):
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)
        # Fin si le curseur `position` est sur n
        position, _ = state
        return position == self.n
        # END_YOUR_CODE

    def succAndCost(self, state):


        # BEGIN_YOUR_CODE (our solution is 8 lines of code, but don't worry if you deviate from this)
        position, previous_word = state
        result = []
        # result: une liste de tuples (action, newState, cost)

        # Indice de la lettre à laquelle on se trouve : position
        # action.new_position = on se place à la lettre d'indice compris entre ]state, n]
        # on évalue le coût du mot chosen_word choisi dans le set renvoyé par possibleFills

        # On parcourt toutes les lettres restantes à la recherche de nouveaux mots
        for new_position in range(position+1, self.n+1):
            letters = self.query[position:new_position]
            # word est dans le corpus? En fait ici tous les mots n'appartenant pas au corpus ont 
            # un coût très élévé, donc on ne gère pas particulièrement ce point
            # Cas d'un set vide
            set_words = self.possibleFills(letters)
            if len(set_words) == 0:
                cost = self.bigramCost(previous_word, letters)
                result.append((action, (new_position, letters), cost))  # (action, new_state, cost)
            else:
                for chosen_word in self.possibleFills(letters):
                    cost = self.bigramCost(previous_word, chosen_word)
                    result.append((action, (new_position, chosen_word), cost))  # (action, new_state, cost)

        return result        # END_YOUR_CODE

def insertVowels__plutot_pb_3b(queryWords, bigramCost, possibleFills):
    if len(queryWords) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(VowelInsertionProblem(queryWords, bigramCost, possibleFills))

    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    # Reconstruction des mots à partir de l'historique des positions de coupes stockées dans `actions`
    words = []
    for _, chosen_word in ucs.actions:
        words.append(chosen_word)
    text = ' '.join(words)

    # Debug
    print('-'*80)
    print query
    print (ucs.actions)
    print(words)
    print text
    print('-'*80)

    return text    # END_YOUR_CODE

############################################################
# Problem 3b: Solve the joint segmentation-and-insertion problem
# n         : nb de caractères dans `query`
# state     : (position, previous_word) 
#             position du curseur sur la chaîne de caractères
#             précédent mot trouvé pour l'usage du bi-gramme
# successor : nouveau mot, nouvelle position du curseur
# action    : (new_position, chosen_word) 
#           : nouvelle position du curseur, mot choisi parmis ceux possibles
# coût de passage b(previous_word,chosen_word)


class JointSegmentationInsertionProblem(util.SearchProblem):
    def __init__(self, query, bigramCost, possibleFills):
        self.query = query
        self.bigramCost = bigramCost
        self.possibleFills = possibleFills
        self.n = len(self.query)

    def startState(self):
        # start state = position initiale du curseur sur la chaîne de caractères
        #               + mot précédent = symbole de début de phrase
        return 0, SENTENCE_BEGIN

    def isEnd(self, state):
        # Fin si le curseur `position` est sur n
        position, _ = state
        return position == self.n

    def succAndCost(self, state):
        position, previous_word = state
        result = []
        # result: une liste de tuples (action, newState, cost)

        # Indice de la lettre à laquelle on se trouve : position
        # new_position = on se place à la lettre d'indice compris entre ]state, n]
        # on évalue le coût du mot chosen_word choisi dans le set renvoyé par possibleFills
        # action: on stocke le mot chosen_word

        # On parcourt toutes les lettres restantes à la recherche de nouveaux mots
        for new_position in range(position+1, self.n+1):

            consonants = self.query[position:new_position]
            possible_words = self.possibleFills(consonants)

            # Cas d'un set vide de mots possibles
            if len(possible_words) == 0:
                action   = consonants
                newState = (new_position, consonants)
                # Nécessité de mettre un coût élévé sinon (-BEGIN-, ensemble des consonnes)
                # a un coût trop faible et est toujours considéré comme la meilleure solution
                cost     = 60000  
                result.append((action, newState, cost))
            else:
                for chosen_word in possible_words:
                    action   = chosen_word
                    newState = (new_position, chosen_word)
                    cost     = self.bigramCost(previous_word, chosen_word)
                    result.append((action, newState, cost))
        # print('='*80)
        # print position, previous_word
        # for item in result:
        #     action, newState, cost = item
        #     print '> ', action
        #     print '  ', newState
        #     print '  ', cost
        return result


def segmentAndInsert(query, bigramCost, possibleFills):
    if len(query) == 0:
        return ''

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(JointSegmentationInsertionProblem(query, bigramCost, possibleFills))

    # BEGIN_YOUR_CODE (our solution is 3 lines of code, but don't worry if you deviate from this)
    # Reconstruction des mots à partir de l'historique des positions de coupes stockées dans `actions`
    words = []
    for chosen_word in ucs.actions:
        words.append(chosen_word)
    text = ' '.join(words)

    # Debug
    print('-'*80)
    print query
    print (ucs.actions)
    print (ucs.totalCost)
    print(words)
    print text
    print('-'*80)

    return text

############################################################

if __name__ == '__main__':
    shell.main()
