# DM 2 Optimisation

##Première méthode : force brute

On a résolu le problème en se restreignant à des positions discrétisées pour les caméras.
Notre programme permet de prendre un pas variable pour ces positions, de sorte à pouvoir explorer diverses discrétisations de la grille.

On restreint également le nombre de variables à considérer en prenant seulement celles contenues dans des cercles de rayon r (4 pour les caméras de type 1, 8 pour les caméras de type 2). 

Une première résolution avec un pas de 1 donne une solution avec un résultat de 3322 en 13s (il semble que le résultat devrait être de 2680, cependant nous ne trouvons pas l'erreur s'il y en a une...)

Avec un pas de 0,5 nous obtenons 3315 en 75s.


#Deuxième méthode : recherche locale


La recherche locale consiste à partir d'une solution admissible et aléatoirement modifier certains de ses composantes. Si la modification améliore la solution on enregistre la nouvelle solution, sinon on essaie de nouveau.

Dans notre cas nous pouvons par exemple ajouter une caméra et supprimer toutes les caméras qui insersectent cette caméra. On complète ensuite de manière gloutonne si des objets ne sont plus couverts.
Si la solution est meilleur on la garde, sinon on ajoute une nouvelle caméra ailleurs.

L'algorithme de recherche locale s'arrête au bout d'un temps que l'on aura fixé préalablement. 

