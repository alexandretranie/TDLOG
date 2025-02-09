[English version below]

# TDLOG : quatrième séance

Ce fichier présente les exercices pour la quatrième séance du module. L'objectif
de cette séance est de terminer l'implémentation d'une version simplifiée du jeu
"Carcassonne". Il s'agit de l'édition pour enfants, "Mon premier Carcassonne",
dont les règles sont disponibles en ligne sur le
[site de l'éditeur](http://www.zmangames.com/en/products/my-first-carcassonne/)
et [dans ce dépôt](./rules.pdf).


## Première étape

Avec les éléments déjà programmés, il est possible d'implémenter le calcul au
cœur du jeu : la détermination des chemins clos. Un chemin est clos dans deux
cas : il s'agit d'une boucle ou ses deux extrémités sont sans lien vers une
autre tuile.

Exercice : implémenter les éléments nécessaires pour déterminer les pions à
placer lorsque l'ajout d'une tuile clôt un ou plusieurs chemins.


## Deuxième étape

L'un des derniers éléments manquants à la modélisation du jeu est la capacité à
produire les coups possibles. Un joueur ne peut placer une tuile qu'à une
position où elle serait voisine par au moins un côté d'une tuile déjà placée. De
plus, lorsqu'un joueur place une tuile, étant donnée la représentation des
tuiles choisie, il peut décider d'une rotation.

Exercice : implémenter les éléments nécessaires pour représenter les positions
et coups possibles, ainsi que le code permettant de produire les coups possibles
à partir de l'état de la partie.


## Troisième étape

Pour implémenter le comportement des joueurs, on peut par exemple ajouter une
méthode `play` qui reçoit la liste des coups possibles et renvoie le coup
choisi. Les différents types de joueurs ont des implémentations différentes :

- pour le joueur "aléatoire", un coup est choisi au hasard dans la liste ;
- pour le joueur "humain", la liste des coups est affichée avec des indices,
  et l'utilisateur entre au clavier l'indice du coup choisi (typiquement en
  utilisant la fonction ``input``) ;
- pour un joueur "IA", le coup choisi est le coup qui permet au joueur de placer
  le maximum de pions (pour différencier entre les deux niveaux de difficulté,
  on peut de surcroît minimiser le nombre de pions adverses placés pour le
  niveau "difficile").

Exercice : ajouter à chaque classe héritant de `player.Player` une méthode
`play`.


## Quatrième étape

La dernière étape consiste à implémenter la boucle principale du jeu. Il s'agit,
de manière répétée, d'afficher le plateau de jeu et de faire jouer un joueur
jusqu'à atteindre la fin de la partie (soit parce qu'un joueur a placé tous ses
pions, soit parce qu'il ne reste plus de tuiles).

Exercice : ajouter une méthode `play` à la classe `game.Game` qui implémente la
boucle principale du jeu, et retourne la liste du ou des vainqueurs, et adapter
le point d'entrée du programme (dans `mfc.py`) en conséquence.


# TDLOG: fourth session

This file contains the exercises for the fourth session of the course. The goal
of this session is to finish the implementation of a slightly simplified version
of the game named "Carcassonne". The version we are interested in is "My First
Carcassonne"; the rules are available on the
[editor's website](http://www.zmangames.com/en/products/my-first-carcassonne/)
and [in this repository](./rules.pdf).


## First step

With the elements already programmed, it is possible to implement the
computation at the heart of the game: determining when roads are closed. A road
is closed in two cases: it is a loop or both extremities have no links to
another tile.

Exercise: implement the elements needed to determine the pawns that should be
placed when the addition of a tile closes one or several roads.


## Second step

One of the missing pieces in terms of modelling is the ability to generate the
list of all possible moves. A player can play a tile only at a position where it
would share at least one side with an already-placed tile. Moreover, when a
player places a tile, given the representation of tiles we chose, it can decide
to rotate it arbitrarily.

Exercise: implement the elements needed to represent and generate the legal
positions and moves, given the state of the game


## Third step

In order to implement the behaviors of the player, we can for instance add a
`play` method that receives the list of possible moves and return the chosen
move. The different kinds of players have different implementations:

- for a "random" player, the move is chosen randomly;
- for a "human" player, the list of moves is displayed with indices, and the
  user input the index of the chose move using the keyboard (for instance, using
  the ``input`` function);
- for an "AI" player, the chosen move is the one maximizing the number of pawns
  placed by the player (to distinguish the two difficulty levels, the "hard" level
  may in addition minimize the number of pawns placed by the other players).

Exercise: add a `play` method to each class inheriting from `player.Player`.


## Fourth step

The final step is to implement the main loop of the game. The goal is to repeatedly
print the board and make the player choose its move until the end of the game is
reached (either a player has placed all its pawns, or there are no tiles left).

Exercise: add a `play` method to the `game.Game` class to implement the game loop
and return a list with the winner(s), and update the entry point of the program
(in `mfc.py`) accordingly.
