# challenge_robotique
## La super stratégie
Pour aborder notre problème, nous avons, dans un premier temps, utilisé la méthode de Monte-Carlo par chaînes de Markov qui nous donnait un chemin relativement court en passant par les cylindres. Nous avons fixé le point de départ pour qu’il corresponde au point de départ du robot. Et nous avons retiré l’obligation de l’algorithme à revenir à son point de départ pour mieux correspondre à notre problème.

Nous avons également utilisé la méthode du recuit simulé pour plus de précision dans nos calculs.

Nous avons alors établi une distance “perçue” entre deux points qui prenait en compte à la fois la distance réelle, mais également le poids du prochain point et sa valeur de manière à savoir si le point valait le coup d’être récupéré.

Par la suite, nous nous sommes dit que le robot, dans tous les cas, ne pourrait pas récupérer tous les cylindres donc nous avons modifié notre méthode de calcul pour qu’il renvoi un chemin avec uniquement un certain nombre de cylindres récupérés, de manière à ce qu’il n’aille pas chercher un point éloigné et sans intérêt.

Pour déterminer quel est le bon nombre de cylindres à récupérer, nous simulons nous-même le parcours avec les limitations données pour savoir si un itinéraire est faisable. À ce moment-là, nous utilisons une approche dichotomique pour, à la fois, avoir un chemin faisable, mais aussi un maximum de cylindres ramassés.

Une fois notre chemin final calculé, avec les coordonnées des différents points, nous calculons les distances à parcourir et les angles avec lesquels tourner, avec la fonction atan2, pour récupérer tous les cylindres, et nous inscrivons ces instructions dans un fichier texte.


## Les super membres
Eliot SHAW

Clarice Goulet

Camille Forest

##


[sujet](https://partage.imt.fr/index.php/s/morx7iCSEnpRKKJ)
[map](https://partage.imt.fr/index.php/s/BwXS9fkE95CxxMf)
[script pour voir](https://partage.imt.fr/index.php/s/CQ9bt2dmzt4efoN)
[API](https://partage.imt.fr/index.php/s/wbbfNLm3y4peL7k)
[maps de test](https://partage.imt.fr/index.php/s/B8rASYoAY5DDHDo)


## Methodologie

Données de base : 
temps 600s
carburant 10000
vmax 10m/s
6.93*10**-2
