# Notebooks Jupyter

## Projet et Livrables

Ce dépôt git contient principalement les fichiers:

  - [🗒️ `README.md`](README.md): description du projet (ce document)

  - [📁 `samples`](samples): notebooks de référence (encodés en UTF-8)

  - trois squelettes de programme (avec documentation et tests)
    - [🐍 `notebook_v0.py`](notebook_v0.py)
    - [🐍 `notebook_v1.py`](notebook_v1.py)
    - [🐍 `notebook_v2.py`](notebook_v2.py)


- [⚙️ `environment.yml`](environment.yml): fichier décrivant l'environnement
  conda `python-advanced-eval` associé à ce projet

--------------------------------------------------------------------------------

Votre clone de ce dépôt (votre rendu) devra au final comporter les fichiers :

  - 🐍 `notebook_v0.py`, `notebook_v1.py`  et `notebook_v2.py` : les programmes
    finalisés.

  - 📘 `rapport.ipynb` : un rapport (un notebook) documentant votre démarche

Le projet est exigible le **20 Janvier 2022 à minuit.**

Le barême affecte :

  - 10 points à la première partie (v0)
  
  - 5 points pour la seconde partie (v1)
  
  - 5 points pour la troisième partie (v2)

Seront pris en compte :

  - Le bon fonctionnement des programmes (notamment, leur capacité à passer
    les tests qui sont fournis).

  - La lisibilité et l'organisation du code (choix des noms (variables,
    fonctions, classes), commentaires aux endroits critiques,
    respect des standards de formatage, etc.).

  - L'usage que vous faites des concepts du langage.

  - La capacité du rapport à retracer et expliquer la démarche 
    exploratoire qui est la vôtre (avant la phase de rédaction du programme),
    à présenter les problèmes rencontrés, les options qui sont les vôtres, 
    à expliquer vos décisions (quelle option choisir), à démontrer les
    résultats (si/comment ça a fonctionné). 

**Recommandation.** Il est important que vous validiez (et
éventuellement déverminiez) votre code, en le lançant interactivement. 
Cette démonstration de bon fonctionnement est typiquement à fournir dans 
le notebook de rapport.
Cette étape devra précéder la validation par les tests automatiques qui ne
constituent qu'un filet minimal de sécurité.

## Prélude

Pour créer l'environnement conda:

    conda env create -f environment.yml

Dans l'environnement conda `python-advanced-eval` :

  - Pour produire la documentation de par exemple `notebook_v0.py` :

        python -m pydoc notebook_v0

  - Pour tester les exemples de code contenus dans un fichier :

        python -m doctest notebook_v0.py

    Évidemment au tout début, le squelette qu'on vous fournit ne contient aucune
    implémentation, et à ce stade de nombreux tests échouent 😭.
    (Prenez garde à ne pas modifier les docstrings qui sont présents dans
    les squelettes de programmes si vous voulez que les tests restent
    pertinents.)

## Format des notebooks (iypnb)

Le format standard décrivant les notebooks Jupyter est le format ipynb
(pour [IPython](https://ipython.org/) notebook);
les fichiers dans ce format utilisent l'extension `.ipynb`.
Dans ce projet, nous vous suggérons pour comprendre ce format d'étudier
quelques notebooks élementaires, disponibles dans le dossier [📁 `samples`](samples).

Si plus de détails sont nécessaires, [le format est documenté
ici](https://nbformat.readthedocs.io/en/latest/format_description.html) :

[![nbformat](images/nbformat.png)](https://nbformat.readthedocs.io/en/latest/format_description.html)

## Une version sans classe `notebook_v0.py`

### **Question 1**: Chargement du fichier JSON (`.ipynb`)

Le format ipynb est un dialecte du format [JSON](https://www.json.org/json-fr.html).
Voilà un exemple de fichier JSON valide :

``` js
{
  "id": 984549706549166055,
  "text": "🔥 This is fine. 🔥",
  "isRetweet": false,
  "isDeleted": false,
  "favorites": 49,
  "retweets": 255,
  "date":"2011-08-02 18:07:48",
  "isFlagged": true,
  "meta": null
}
```

Le module standard `json` de Python permet de faire la conversion
entre de tels contenus textuels et les objets natifs de Python (dictionnaires,
lists, chaînes de caractères, etc.). L'exemple JSON précédent serait par exemple
converti dans le dictionnaire Python :

``` python
{'id': 984549706549166055, 'text': '🔥 This is fine. 🔥', 'isRetweet': False, 'isDeleted': False, 'favorites': 49, 'retweets': 255, 'date': '2011-08-02 18:07:48', 'isFlagged': True, 'meta': None}
```

Pour faciliter la manipulation de notebooks Jupyter en Python :

  - 🚀 **Développez les fonctions `load_ipynb` et `save_ipynb`.**

### **Question 2**: À la racine des notebooks

Etudiez la structure de haut-niveau des notebooks ipynb, puis :

  - 🚀 **Développez les fonctions `get_format_version`, `get_metadata` et `get_cells`.**

### **Question 3**: Format percent

Le [format
percent](https://jupytext.readthedocs.io/en/latest/formats.html#the-percent-format)
est une variante du format standard `.ipynb` pour décrire les notebooks Jupyter.
Les notebooks sont alors représentés comme du code source Python avec le contenu
Markdown en commentaire ; le résultat de l'exécution des cellules n'est pas pris
en compte. Par exemple, le notebook contenu dans `samples/hello-world.ipynb`
serait représenté dans ce format par le texte :

``` python
# %% [markdown]
# Hello world!
# ============
# Print `Hello world!`:

# %%
print("Hello world!")

# %% [markdown]
# Goodbye! 👋
```

Ce format permet de manipuler les notebooks comme du code Python classique avec
les avantages afférents. Certains environnements de développement, dont VS Code,
fournissent de plus un support spécifique pour ce format. Quand la bibliothèque
python `jupytext` est installée, l'application Jupyter notebook devient aussi
capable de lire ce format (ce qu'on a utilisé en cours tout au long du semestre)

  - 🚀 **Développez la fonction `to_percent`.**

🗝️ Pour valider le code, on pourra convertir les notebook Jupyter de reférence en
fichiers source Python au format percent, puis les valider avec VS Code ou
le Jupyter notebook avec l'extension jupytext.


### **Question 4**: Notebooks Starboard

[Starboard](https://starboard.gg/about) est une plate-forme open-source de
notebooks s'exécutant intégralement dans le navigateur web,
où peuvent être utilisés les langages Python et Javascript.

Les notebooks Starboard sont décrits dans une variante du [format
percent](https://jupytext.readthedocs.io/en/latest/formats.html#the-percent-format),
stockés dans des fichiers d'extensions `.nb` et exportés comme des fichiers HTML
pour être exploités dans un navigateur.

![Starboard Python notebook](images/starboard.png)

ℹ️ Vous pouvez [essayer ce système ici][starboard-python] sur un notebook
intitulé "🐍 Python support in Starboard notebook" qui illustre ce qu'on peut
faire.

Pour voir ce notebook au format `.nb`, ouvrez le notebook puis
cliquez sur le très discret bouton "Source" dans le pied de page du document.

De là, pour voir ce notebook au format HTML, cherchez un bouton 'Export HTML'

  - 🚀 **Développez la fonction `to_starboard`.**

🗝️ Pour valider ce code, on pourra convertir les notebooks Jupyter de reférence
(dans le dossier `samples`) en fichiers Starboard HTML, puis vérifier en les
ouvrant dans un navigateur Web que la conversion est valide.

[starboard-python]: https://starboard.gg/#python

### Exploitation des résultats

Dans toute cette partie on suppose que le notebook a été au préalable exécuté
par ailleurs

#### **Question 5**: 🧹 Nettoyage

Pour nettoyer un notebook de toute trace d'exécution :

  - 🚀 **Développez la fonction `clear_outputs`.**

#### **Question 6**: 📝 Flux de texte

Capturez le résultat des appels à `print` :

  - 🚀 **Développez la fonction `get_stream`.**

#### **Question 7**: 🚨 Erreurs

L'exécution d'une cellule de code peut engendrer des erreurs; pour les analyser :

  - 🚀 **Développez la fonction `get_exceptions`.**

#### **Question 8**: 📊 Images

Pour capturer les images générées par matplotlib :

  - 🚀 **Développez la fonction `get_images`.**

🗝️ On pourra utiliser la fonction [`imshow` de Matplotlib][imshow] pour valider
les résultats.

[imshow]: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html

## Un code orienté objet `notebook_v1.py`

Le code produit précédemment est parfaitement fonctionnel, mais il manque
fondamentalement de structure. En particulier, nous devons passer le gros
dictionnaire contenant tout le contenu du notebook initial, ce format étant peu
expressif et non spécifique à notre domaine d'étude.

Cette partie vous propose donc de créer une représentation objet du contenu du
notebook, qui permettra d'améliorer sensiblement le code:

- en le rendant plus lisible
- en ne gardant en mémoire que les données qui nous sont réellement utiles (en
  supprimant par exemple les "meta-datas")
- en permettant de découpler le chargement du notebook de l'exploitation de ces
  données

Dans la suite de ce sujet, nous allons développer deux versions
"orientées-objet" (c'est à dire avec des `class`es) de notre code initial":

1. une version qui construit un `Notebook` en prenant en argument le contenu du
   fichier `.ipynb`
2. une autre version qui construit un `Notebook` en prenant directement le
   contenu des cellules; ce sera l'objet de la section suivante

Pour la première version, les développements demandés doivent être réalisés dans
le fichier `notebook_v1.py`.

Vous êtes évidemment invités à utiliser vos travaux précédents comme références,
ainsi que les tests fournis, pour guider votre réalisation.
#### **Question 9**: Chargement

Le fichier `notebook_v0.py` contient le squelette de la classe `Notebook`
représentant le notebook Jupyter ainsi que deux classes `CodeCell` et
`MarkdownCell` représentant les différentes cellules.

Remplissez tous les constructeurs (méthodes `__init__`) des classes proposées:

  - 🚀 **Développez la méthode `__init__` de la classe `Notebook`.**
  - 🚀 **Développez la méthode `__init__` de la classe `CodeCell`.**
  - 🚀 **Développez la méthode `__init__` de la classe `MarkdownCell`.**

Le fonctionnement attendu est le suivant:

- la classe Notebook se construit à partir du contenu du fichier chargé
- elle contient un numéro de version (attribut `version`)
- et une liste de cellules (`cells`) contenant soit des instances de `CodeCell`
  (pour les cellules Python) ou de `MarkdownCell` (pour les cellules Markdown)

on aura donc un fonctionnement que l'on peut illustrer ainsi:

```
┌─────────────────────────┐
│        Notebook         │
├─────────────────────────┤
│                         │
│ version                 │       ┌────────────────────┐
│                         │       | liste de CodeCell  │
│ cells ─────────┐        │       │  ou MarkdownCell   │
│                ▼        │       └────────────────────┘
│ ┌─────┬─────┬─────┬─────┼─────┬─────┬─────┬─────┬─────┐
│ │     │     │     │     │     │     │     │     │     │
│ │     │     │     │     │     │     │     │     │     │
│ └─────┴─────┴─────┴─────┼─────┴─────┴─────┴─────┴─────┘
│                         │
└─────────────────────────┘
```

Nous ne chargerons pas les `metadata` ni les `outputs` dans cette partie, les
classe `CodeCell` et `MarkdownCell` aurons donc les propriétés suivantes:

```
┌─────────────────────────┐  ┌─────────────────────────┐
│        CodeCell         │  │       MarkdownCell      │
├─────────────────────────┤  ├─────────────────────────┤
│ id                      │  │ id                      │
│ type                    │  │ type                    │
│ execution_count         │  │ source                  │
│ source                  │  └───▲─────────────────────┘
└─────▲───────────────────┘      │
      │                          │
      │                          │  source est une
      └──────────────────────────┴─  liste de str
                                    (1 par ligne)
```

  - 🚀 **(BONUS, Optionnel) Développez une classe `Cell` parente de `CodeCell`
    et `MarkdownCell` pour factoriser le code commun.**

#### **Question 10**: Chargement depuis un fichier

On rajoute ensuite une méthode statique (= de classe) pour faciliter le
chargement d'un fichier dans un Notebook:

  - 🚀 **Développez la méthode statique `from_file` de la classe `Notebook`.**
#### **Question 11**: Itération des cellules d'un Notebook

On peut itérer un `Notebook`, ce qui revient à parcourir ses cellules dans
l'ordre avec une boucle `for`:

  - 🚀 **Développez la méthode `__iter__` de la classe `Notebook`.**

#### **Question 12**: Sauvegarde

De même, nous pouvons créer une classe `Serializer` qui permet de sauvegarder un
`Notebook` sur le disque.

Attention cependant:

- il faudra rajouter un objet vide `metadata` au notebook au format JSON
- de même il faudra rajouter un objet vide `metadata` aux cellules

vous pouvez vous laisser guider par les tests pour valider votre implémentation.

- 🚀 **Développez les méthodes de la classe `Serializer`.**

#### **Question 13**: Sauvegarde (py-percent)

Nous pouvons aussi utiliser ce format `Notebook` "objet" pour réaliser des
transformations de format, par exemple le transformer au format "py-percent":

- 🚀 **Développez les méthodes de la classe `PyPercentSerializer`.**

#### **Question 14**: Mise en forme personnalisée

Nous proposons également d'afficher le contenu du notebook dans le terminal, de
façon personnalisée:

- 🚀 **Développez les méthodes de la classe `Outliner`.**

## Code objet `notebook_v2.py`

Nous allons maintenant modifier la façon dont les objets `Notebook`, `CodeCell`
et `MarkdownCell` sont construits.

L'idée est de découpler complètement note code représentant les notebooks de la
façon dont ils sont enregistrés dans les fichiers `.ipynb`.

**💡 Si vous faites correctement votre travail, les classes `
PyPercentSerializer`, ` Serializer`  et `Outliner` développées précedemment
doivent fonctionner avec cette nouvelle version de la classe `Notebook` !**
C'est une illustration de l'intérêt de l'encapsulation !
#### **Question 15**: Construction des Notebooks

Ouvrez désormais le fichier `notebook_v2.py`.

  - 🚀 **Développez la méthode `__init__` simplifiée pour la classe `Notebook`.**
  - 🚀 **Développez la méthode `__init__` simplifiée pour la classe `CodeCell`.**
  - 🚀 **Développez la méthode `__init__` simplifiée pour la classe `MarkdownCell`.**

vous pourrez évidemment vous inspirer de ce que vous aviez fait pour la version
précédente.

### **Question 16**: Chargement depuis un fichier

Notre classe `Notebook` ne comprenant plus le format `.ipynb`, nous devons
extraire la logique de chargement dans une classe dédiée:

  - 🚀 **Développez les méthode de la class `NotebookLoader`.**

### **Question 17**: Transformation en pure Markdown

On se propose de transformer le notebook en Markdown.

Pour cela:

- nous générons un nouveau notebook
- les cellules de type "code" seront transformées en cellules de type "markdown".

En pratique la transformation en markdown se fera en "entourant" le code de
délimiteurs spéciaux, ainsi:

```python
print("Hello world")
```

devient:

<pre>
``` python
print("Hello world")
```
</pre>

  - 🚀 **Développez les méthode de la class `Markdownizer`.**

### **Question 18**: Élimination des cellules Markdown

Une autre transformation possible est la suppression des cellules
`MarkdownCell`, pour ne garder que le code:

  - 🚀 **Développez les méthode de la class `MarkdownLesser`.**

### **Question 19**: Re-chargement depuis le format Py-Percent

Enfin, comme nous avons découplé `Notebook` de la structure JSON des fichiers
`.ipynb`, on peut désormais faire le code nécessaire pour _recharger_ les
fichiers au format py-percent:

  - 🚀 **Développez les méthode de la class `PyPercentLoader`.**
