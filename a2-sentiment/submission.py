#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import collections
import math
import sys
from util import *
from pprint import pprint
import numpy as np

############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction

def extractWordFeatures(x):
    """
    Extract word features for a string x. Words are delimited by
    whitespace characters only.
    @param string x: 
    @return dict: feature vector representation of x.
    Example: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # BEGIN_YOUR_CODE (our solution is 4 lines of code, but don't worry if you deviate from this)

    # phi: feature vector
    phi = collections.defaultdict(float)
    
    for word in x.split():
        phi[word] += 1
    return phi

    # END_YOUR_CODE

############################################################
# Problem 3b: stochastic gradient descent

def learnPredictor(trainExamples, testExamples, featureExtractor, numIters, eta):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''
    w = collections.defaultdict(float)  # feature => weight
    # BEGIN_YOUR_CODE (our solution is 12 lines of code, but don't worry if you deviate from this)

    features = []
    for x, y in trainExamples:  # x: text, y: notation +/- 1
        phi = featureExtractor(x)
        features += [feature for feature in phi]

    # Initialisation des poids
    for feature in set(features):
        w[feature] = 0.

    # Choix du prédicteur: classifieur linéaire
    # score = w.phi(x)
    # linear classifier +1 si score > 0, -1 sinon
    def linearClassifier(w):
        def predictor(x):
            phi = featureExtractor(x)
            if dotProduct(w, phi) > 0:
                y = 1
            else:
                y=-1
            return y
            # possiblité de l'écrire de manière plus compacte:
            # mais un peu plus lent...
            #return (1 if dotProduct(featureExtractor(x), w) > 0 else -1)
        return predictor



    # Fonction de coût
    # Hinge Loss sans L2 regularisation (SVM: +L2)
    def loss(x, y, w):
        phi = featureExtractor(x)
        margin = dotProduct(w, phi) * y
        return max( 1 - margin, 0)

    # Apprentissage 
    # Stochastic Gradient Descent
    for iter in range(numIters):
        for x, y in trainExamples:

            # dL/dw = -phi*y si margin<1, 0 sinon
            phi = featureExtractor(x)
            margin = dotProduct(w, phi) * y
            if margin < 1:
                increment(w, y*eta, phi)
            # print "-"*80
            # print "> iter       = " , iter
            # print "> loss       = " , loss(x,y,w)
    print "> train error  = " ,evaluatePredictor(trainExamples, linearClassifier(w))
    print "> test error   = " ,evaluatePredictor(testExamples , linearClassifier(w))


    # END_YOUR_CODE
    return w

############################################################
# Problem 3c: generate test case

def generateDataset(numExamples, weights):
    '''
    Return a set of examples (phi(x), y) randomly which are classified correctly by
    |weights|.
    '''
    random.seed(42)
    # Return a single example (phi(x), y).
    # phi(x) should be a dict whose keys are a subset of the keys in weights
    # and values can be anything (randomize!) with a nonzero score under the given weight vector.
    # y should be 1 or -1 as classified by the weight vector.
    def generateExample():
        # BEGIN_YOUR_CODE (our solution is 2 lines of code, but don't worry if you deviate from this)

        phi = {}

        # Génération d'un sous ensemble de l'ensemble des clés contenues dans `weights`
        sample_size = random.randint(1,len(weights))
        # Indices des clés dans l'échatillon choisi
        chosen_features = random.sample([key for key in weights], sample_size)
        for feature in chosen_features:
            phi[feature] = 1 

        score = dotProduct(weights, phi)  #w.phi
        y = 1 if (score > 0) else -1

        # w[feature] est différent de 0 par construction
        # Donc pour que le score soit nul, il faut au moins qu'il y ait au moins 2 features
        # Dans ce cas là on en retire 1 de phi pour que le score soit différent de zéro
        if score == 0:
            phi.popitem()
            score = dotProduct(weights, phi)  #w.phi
            y = 1 if (score > 0) else -1


        # print phi
        # print y
        # print score

        # END_YOUR_CODE
        return (phi, y)

    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3e: character features

def extractCharacterFeatures(n):
    '''
    Return a function that takes a string |x| and returns a sparse feature
    vector consisting of all n-grams of |x| without spaces.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    You may assume that n >= 1.
    '''
    def extract(x):
        # BEGIN_YOUR_CODE (our solution is 6 lines of code, but don't worry if you deviate from this)
        phi = collections.defaultdict(float)

        x = x.replace(' ', '')
        chunks, chunk_size = len(x), n
        ngrams = set([ x[i:i+chunk_size] for i in range(0, chunks-chunk_size+1, 1) ])
        for ngram in ngrams:
            phi[ngram] = 1
        return phi

        # END_YOUR_CODE
    return extract

############################################################
# Problem 4: k-means
############################################################

# La fonction distance donne un temps de calcul trop long

def distance(x,y):
    """
    Donne le carré de la distance (norme L2) entre deux vecteurs épars x et y
    input:
        x : string-to-double dictionary
        y : string-to-double dictionary
    output:
        distance: réél (L2**2)
    """

    # Sets des clés pour x et y
    x_keys = set(x.keys())
    y_keys = set(y.keys())
    # Clés communes
    intersection = x_keys.intersection(y_keys)

    distance = 0
    # Clés seulement dans x
    for key in x_keys.difference(intersection):
        distance += x[key]**2

    # Clés seulement dans y
    for key in y_keys.difference(intersection):
        distance += y[key]**2

    # Clés dans les deux vecteurs (dict)
    for key in intersection:
        distance += (x[key]-y[key])**2

    return distance


def kmeans(x, K, maxIters):
    '''
    x: list of examples, each example is a string-to-double dict representing a sparse vector.
    K: number of desired clusters. Assume that 0 < K <= |examples|.
    maxIters: maximum number of iterations to run (you should terminate early if the algorithm converges).
    Return: (length K list of cluster centroids,
            list of assignments (i.e. if examples[i] belongs to centers[j], then assignments[i] = j)
            final reconstruction loss)
    '''
    # BEGIN_YOUR_CODE (our solution is 32 lines of code, but don't worry if you deviate from this)

    # Nombre de centroïdes = K

    # Initialisation de chacun des centroïdes mu[k] à un élément de x pris au hasard sans répétition
    # random.seed()  # Sinon on a toujours le même ensemble
    # mask = random.sample(range(len(x)), K)
    # mu = [x[i] for i in mask]
    # Ces lignes peuvent être rassemblées en une seule:
    mu = random.sample(x, K)

    # n: nombre d'exemples
    n = len(x)

    # Debug
    # print ("-"*80)
    # print 'K    = ',(K)

    # Utilsation de la décompostion du carré pour le calcul de la distance
    xx = [dotProduct(x[i], x[i]) for i in range(n)]
    mumu = []
    # Pas encore assez rapide...


    def cluster_assignment():
        """
        output: 
            z : nouvelle liste d'association des points x à chaque centroïde
        """
        z = []
        for i in range(n):
            # indice du centroïde qui minimise la distance L2 avec le pt considéré
            # [distance(x[i],mu[k]) for k in range(K)] # Trop lent...
            z.append( np.argmin( [xx[i] - 2 * dotProduct(x[i],mu[k]) + mumu[k] for k in range(K)]  ) )
        # print 'z    = ',(z)
        return z

    def centroid():
        """
        output: 
            mu : nouvelle liste de centroïdes
        """
        mu = []
        for k in range(K):
            # Ensemble des points dans le cluster k
            cluster = [i for i in range(n) if z[i] == k]
            # taille du cluster
            n_cluster = len(cluster)

            mu.append({})
            if n_cluster != 0:
                scale = 1./n_cluster
                for i in cluster:
                    increment( mu[k], scale, x[i] )
                # il faudrait éventuellement modifier K si n_cluster == 0

        # print 'mu[',k,'] = ',(mu[k])
        return mu


    t=0
    while (t<maxIters):
    # while (t<10):

        # print ("-"*80)
        # print 't    = ',(t)

        mumu = [dotProduct(mu[k], mu[k]) for k in range(K)]

        # Etape 1: Choix de le meilleure association des points x à chaque centroïde
        # z liste des associations
        # z_i associe le point x_i à un centroïde k dans [1,K]
        z = cluster_assignment()

        # Etape 2: pour chaque cluster on définit un nouveau centroïde
        new_mu = centroid()

        if new_mu != mu:
            mu = new_mu
        else:
            break

        # Passage à l'itération suivante
        t+=1

    # Loss final
    loss = 0
    for i in range(n):
    #     loss += distance(x[i],mu[z[i]])
        loss += xx[i] - 2 * dotProduct(x[i],mu[z[i]]) + mumu[z[i]]


    # Debug
    # print ("-"*80)
    # print 'loss = ', loss
    # print 'z    = ', z
    # print 'mu   = ', mu
    # print ("-"*80)

    return (mu, z, loss)

    # END_YOUR_CODE














