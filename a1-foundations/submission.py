import collections
import math

############################################################
# Problem 3a

def findAlphabeticallyLastWord(text):
    """
    Given a string |text|, return the word in |text| that comes last
    alphabetically (that is, the word that would appear last in a dictionary).
    A word is defined by a maximal sequence of characters without whitespaces.
    You might find max() and list comprehensions handy here.
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    return max(text.split())
    # raise Exception("Not implemented yet")
    # END_YOUR_CODE

############################################################
# Problem 3b

def euclideanDistance(loc1, loc2):
    """
    Return the Euclidean distance between two locations, where the locations
    are pairs of numbers (e.g., (3, 5)).
    """
    # BEGIN_YOUR_CODE (our solution is 1 line of code, but don't worry if you deviate from this)
    x1, y1 = loc1
    x2, y2 = loc2
    return math.sqrt((x1-x2)**2  + (y1-y2)**2)
    # END_YOUR_CODE

############################################################
# Problem 3c

def completeSentences(sentences_list, dict_authorized):
    """
    input:
    sentences_list  : liste de phrases de longueur n
    dict_authorized : dictionnaire indiquant pour chaque mot les mots autorisés ensuite

    output:
    new_list        : liste de phrases différentes de longueur n+1
                      On devrait toujours au moins retourner la phrase de base
    """
    new_list = []

    for sentence in sentences_list:
        words = sentence.split()
        n = len(words)
        if words[n-1] in dict_authorized:
            for new_word in dict_authorized[words[n-1]]:
                new_sentence = sentence + " " + new_word
                if new_sentence not in new_list:
                    new_list.append(new_sentence)
    return new_list

def mutateSentences(sentence):
    """
    Given a sentence (sequence of words), return a list of all "similar"
    sentences.
    We define a sentence to be similar to the original sentence if
      - it as the same number of words, and
      - each pair of adjacent words in the new sentence also occurs in the original sentence
        (the words within each pair should appear in the same order in the output sentence
         as they did in the orignal sentence.)
    Notes:
      - The order of the sentences you output doesn't matter.
      - You must not output duplicates.
      - Your generated sentence can use a word in the original sentence more than
        once.
    Example:
      - Input: 'the cat and the mouse'
      - Output: ['and the cat and the', 'the cat and the mouse', 'the cat and the cat', 'cat and the cat and']
                (reordered versions of this list are allowed)
    """
    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)

    words = sentence.split()
    n = len(words)

    # Détermination des paires de mots valides:
    pair_list = []
    for i in range(n-1):
        pair = [words[i], words[i+1]]
        if pair not in pair_list:
            pair_list.append(pair)

    # Ensemble des mots utilisés
    unique_words = sorted(set(words))

    # dictionnaire des continuations possibles
    dict_authorized = {} 
    # dict_authorized[word] = [list of accepted words] = accepted_continuation
    accepted_continuation = []

    for word in unique_words:
        for i in range(len(pair_list)):
            if pair_list[i][0] == word:
                if pair_list[i][1] not in accepted_continuation:
                    accepted_continuation.append(pair_list[i][1])
        if accepted_continuation:
            dict_authorized[word] = accepted_continuation
        accepted_continuation = [] # clear supprime aussi les listes du dictionnaire...
    #print('dict_authorized', dict_authorized)
    # On aurait pu utiliser `defaultdict, qui semble faire proprement le travail, cf doc

    # Initialisation de la liste des phrases envisageables avec un premier mot
    sentences_list  = unique_words

    for i in range(n-1):
        sentences_list = completeSentences(sentences_list, dict_authorized)
    
    print('sentences_list ' , sentences_list)

    return sentences_list


    # END_YOUR_CODE

############################################################
# Problem 3d

def sparseVectorDotProduct(v1, v2):
    """
    Given two sparse vectors |v1| and |v2|, each represented as collections.defaultdict(float), return
    their dot product.
    You might find it useful to use sum() and a list comprehension.
    A list comprehension consists of brackets containing an expression followed by a for clause, then zero or more for or if clauses
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    
    dot_product = 0
    
    for key in v1.keys():                      # On parcourt la liste des clés de v1
        if key in v2:                          # Si la clé est aussi dans v2
            dot_product += v1[key] * v2[key]   # On met à jour le produit sclaire

    return dot_product



    # END_YOUR_CODE

############################################################
# Problem 3e

def incrementSparseVector(v1, scale, v2):
    """
    Given two sparse vectors |v1| and |v2|, perform v1 += scale * v2.
    This function will be useful later for linear classifiers.
    """
    # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)

    v = v1
    for key in v2.keys():
        v[key] += scale * v2[key]

        # test superflu, mais peut être un changement de type des données ci dessus
        #if key in v:
        #    v[key] += scale * v2[key] 
        #else:
        #    v[key] = scale * v2[key]
    #print(v)
    
    return v
    
    # END_YOUR_CODE

############################################################
# Problem 3f

def findSingletonWords(text):
    """
    Splits the string |text| by whitespace and returns the set of words that
    occur exactly once.
    You might find it useful to use collections.defaultdict(int). Bah non pourquoi faire?
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)
    
    singleton = []
    
    text = text.split()
    unique_words = sorted(set(text))

    singleton = [ word  for word in unique_words if text.count(word) == 1 ]

    return set(singleton)

    # END_YOUR_CODE

############################################################
# Problem 3g

def computeLongestPalindromeLength(text):
    """
    A palindrome is a string that is equal to its reverse (e.g., 'ana').
    Compute the length of the longest palindrome that can be obtained by deleting
    letters from |text|.
    For example: the longest palindrome in 'animal' is 'ama'.
    Your algorithm should run in O(len(text)^2) time.
    You should first define a recurrence before you start coding.
    """
    # BEGIN_YOUR_CODE (our solution is 19 lines of code, but don't worry if you deviate from this)


    # On suppose qu'il n'y a pas d'espaces dans `text`
    count = 0          # Compteur pour le plus long palindrome
    odd_flag = False   # On prend en compte une seule lettre dont le nb d'occurences est impair


    dictionary = collections.defaultdict(int)
    # permet de compter le nombre d'occurence de chaque lettre
    # est initialisé à 0 par la fonction int la première fois qu'elle est rencontrée

    for letter in text:
        dictionary[letter] += 1


    while len(dictionary) > 0:
        # On supprime une lettre pour toutes les occurences impaires
        # On enlève 2 lettres pour les occurences paires >0 et on incrémente le compteur
        for letter in dictionary:
            if dictionary[letter]%2 : # vrai si impair
                dictionary[letter] -= 1
                if not odd_flag:
                    count += 1
                    odd_flag = True
            else:                     #cas pair
                if dictionary[letter] > 0 :    # On devrait pouvoir virer ce if
                    dictionary[letter] -= 2
                    count += 2

        # Suppression des lettres avec 0 occurences
        letters_tbd = [letter for letter in dictionary if dictionary[letter] == 0]

        for letter in letters_tbd:
            del dictionary[letter]

    # tests dev
    #print('dictionary :', sorted(dictionary.items()))
    #print('count :', count)
    
    return count


    # END_YOUR_CODE



















