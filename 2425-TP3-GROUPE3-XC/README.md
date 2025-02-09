[English version below]

# TDLOG : troisième séance

Ce fichier présente les exercices pour la troisième séance du module. L'objectif
de cette séance, et de la prochaine, est de continuer à implémenter une version
simplifiée du jeu "Carcassonne". Il s'agit de l'édition pour enfants, "Mon
premier Carcassonne", dont les règles sont disponibles en ligne sur le
[site de l'éditeur](http://www.zmangames.com/en/products/my-first-carcassonne/)
et [dans ce dépôt](./rules.pdf).


## Première étape

La première étape consiste à modifier la manière dont la pile de tuiles est
construite. Au lieu de définir la liste des tuiles dans le code Python, on
souhaite charger cette liste depuis un fichier au format texte. Le fichier
correspondant à la liste de tuiles par défaut est [default.deck](./default.deck).

La spécification du format est la suivante :

- le format est *orienté ligne*, ce qui signifie que chaque ligne est
  interprétée indépendamment ;
- le caractère `%` marque le début d'un commentaire, qui prend fin en fin de
  ligne ;
- les commentaires sont ignorés ;
- les lignes composées uniquement de caractères espaces sont ignorées (cela
  inclut les lignes qui commencent par un ou plusieurs caractères espaces et se
  terminent par un commentaire) ;
- il existe 3 types de lignes *utiles*, respectivement introduites par les
  directives `NO_LINKS`, `ONE_LINK` et `TWO_LINKS` ;
- la directive `NO_LINKS` apparaît seule sur la ligne (en ignorant d'éventuels
  caractères espaces et commentaires), et représente une tuile sans lien ;
- la directive `ONE_LINK` est seulement suivie d'une spécification de lien (en
  ignorant d'éventuels caractères espaces et commentaires), et représente une
  tuile avec un seul lien ;
- la directive `TWO_LINKS` est suivie d'une première spécification de lien, du
  caractère `&` et d'une seconde spécification de lien (en ignorant d'éventuels
  caractères espaces et commentaires), et représente une tuile avec deux liens ;
- une spécification de lien a la forme *côté* `-` *côté* `:` *couleur*, où les
  valeurs possibles pour les côtés sont : `north`, `east`, `south`, `west`, et
  les valeurs possibles pour les couleurs sont : `blue`, `purple`, `red`,
  `yellow`.

Exercice : écrire une fonction `deck.load_tiles` qui lit depuis un fichier dont
le nom est passé en paramètre une liste de tuiles suivant la spécification
ci-dessus. Cette fonction doit lever une exception si le fichier ne suit pas la
spécification ci-dessus.

Exercice : mettre à jour le constructeur de `game.Game`, et éventuellement
d'autres éléments du programme, pour utiliser cette fonction.


## Deuxième étape

La deuxième étape consiste à passer en revue les différents fichiers Python afin
d'ajouter le traitement des erreurs et des *docstrings* au niveau des classes,
méthodes et fonctions lorsque nécessaire. Par exemple, il ne devrait pas être
possible de créer une tuile avec un lien ne portant que sur un seul côté.

Si une fonction ou méthode ne peut échouer, placer un commentaire à cet effet
(par exemple, `# no error handling needed`), pour indiquer ce fait. Il ne s'agit
pas d'une pratique standard de développement et n'est demandé ici qu'à des fins
d'évaluation.

Exercice : augmenter les fichiers Python avec les commentaires et la gestion
d'erreurs nécessaires.


# TDLOG: third session

This file contains the exercises for the third session of the course. The goal
of this session, and the next one, is to continue the implementation of a
slightly simplified version of the game named "Carcassonne". The version we are
interested in is "My First Carcassonne"; the rules are available on the
[editor's website](http://www.zmangames.com/en/products/my-first-carcassonne/)
and [in this repository](./rules.pdf).


## First step

The first step is to change the way the deck of tiles is built. Instead of
specifying the list of tiles in the Python code, we wish to load this list from
a text file. The file corresponding to the default deck is
[default.deck](./default.deck).

The specification of the format is as follows:

- the format is *line-oriented*, which means that each line is interpreted
  independently;
- the `%` character marks the start of a comment, which ends at the end of the
  line;
- the comments are ignored;
- the lines with only space characters are ignored (this includes the lines
  starting with one or several space characters and ending with a comment);
- there are 3 kinds of *useful* lines, introduced by one of the following
  directives: `NO_LINKS`, `ONE_LINK` and `TWO_LINKS`;
- the `NO_LINKS` directive appears alone on the line (ignoring spaces and
  comments), and represents a tile with no links;
- the `ONE_LINK` directive is followed by a single link specification (ignoring
  spaces and comments), and represents a tile with one link;
- the `TWO_LINKS` directive is followed by a first link specification, the `&`
  character, and a second link specification (ignoring spaces and comments), and
  represents a tile with two links;
- a link specification has the following form: *side* `-` *side* `:` *color*,
  where the possible values for the sides are `north`, `east`, `south`, `west`,
  and the possible values for the color are `blue`, `purple`, `red`, `yellow`.

Exercise: write a function (`deck.load_tiles`) that reads from a file whose name
is passed as a parameter a list of tiles following the specification given
above. This function must raise an exception if the file does not follow the
specification.

Exercise: update the `game.Game` constructor, as well as everything else that
might be need to be tweaked, to use this function.


## Second step

The second step is to review all the Python files of the repository to add the
error handling logic, as well as *docstring* comments to classes, methods and
functions where needed. For instance, it should not be possible to create a tile
with a link referring to a single side.

If a function or method cannot fail, add a comment saying so (for instance, `#
no error handling needed`). This is not a standard development practice, and is
required here only for evaluation purposes.

Exercise: augment the Python files with the needed comments and error handling
logic.
