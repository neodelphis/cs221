import numpy as np

phi = np.array([[1,0], [1,2], [3,0], [2,2]], dtype='f') # D_train = ensemble des phi(x)[i]
n = len(phi)

# We are looking for:
# Final cluster assignments z
# cluster centers mu

# Choix d'une position arbitraire des centroïdes
mu = np.array([[2,3], [2,-1]], dtype='f')
# mu = np.array([[0,1], [3,2]], dtype='f')

# mu = np.array([[-5.9,-6.2], [-6.3,-5.4]])
# Entraîne des div par 0 car aucun pt n'est associé au centroïde le plus loin
# Ca n'a peut être pas trop de sens de le placer si loin
# Un placament initial aléatoire devrait se faire "dans" l'espace défini par les points phi
# Reste quand même que si on a des clusters vides,
# il faudrait s'arranger pour mettre arbitrairement un point

# Nombre de centroïdes
K = len(mu)

# z liste des associations
# z_i associe le point phi_i à un centroïde k dans [1,K]
z = np.zeros(n)

t=0
T=2
while (t<T):

	# Etape 1: Choix de le meilleure association des points phi(x)_i à chaque centroïde
	for i in range(n):
		# centroïde qui minimise la distance L2 avec le pt considéré
		z[i] = np.argmin( [np.linalg.norm(phi[i]-mu[k]) for k in range(K)] )
        # on prend pas le carré, mais ça ne doit pas changer car **2 est croissante sur R+
	#print (z)

	# Etape 2: pour chaque cluster on définit un nouveau centroïde
	for k in range(K):
		# Ensemble des points dans le cluster k
		#for i in range(N):
		#	if z[i] ==  k: # Le point phi[i] appartient au cluster k, via l'association z
		cluster = [i for i in range(n) if z[i] == k] # va servir de masque pour phi
		mu[k] = np.sum(phi[cluster], axis=0) / len(cluster) 

	t+=1

print(mu)
print(z)
