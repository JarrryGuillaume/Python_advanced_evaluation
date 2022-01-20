#!/usr/bin/env python
# coding: utf-8

# Rapport
# =======
# 
#      
#          
# 
# C'est dans ce rapport que l'on répertorie tous les tests des Notebooks v0, v1 et v2.   
# Pour cela, importons d'abord nos notebook 

# In[1]:


import notebook_v0 as v0
import notebook_v1 as v1 
import notebook_v2 as v2 

import numpy as np 
import pprint 
import base64
import io


# # Notebook_v0    
# 
# Voici les tests des fonctions du notebook_v0

# **Question 1** Le but était de coder les fonctions `load_ipynb` et `save_ipynb`

# Pour cette fonction il était essentiel d'ajouter l'argument ```encoding='utf-8' ```car sinon les fichiers `errors` et `streams`affichaient des erreurs d'encodage en raison de l'utilisation des smileys, comme on peut le voir dans l'exemple ci-dessous. 

# In[2]:


test = "samples/streams.ipynb"
ipynb = v0.load_ipynb(test)
ipynb 


# In[3]:


ipynb = v0.load_ipynb(test)
v0.save_ipynb(ipynb, "samples/test-save-load.ipynb")


# **Question 2** Le but était de coder les fonctions `get_format_version`, `get_metadata` et `get_cells`

# Pour `get_format_version`il s'agissait juste de lire les clées `nbformat`et `nbformat_minor`. On l'a déduit de la documentations des notebooks. De même pour les fonctions `get_metadata` et `get_cells` c'est de la lecture simple de dictionnaire. Il n'y a pas de difficultés particulières ici, les tests marchent pour tous les notebooks. 

# **Question 3** Le but était de coder la fonction `to_percent`   
# 
# On a rajouté une ligne de test de saut de ligne 
# ```python 
#         if to_percent[-2] != '\n':
#             to_percent += '\n'
# ````
# car le code source de chacune des cells pouvait contenir ou ne pas contenir le passage de ligne. Si la source ne contenait qu'une ligne en particulier, il fallait l'ajouter nous-mêmes. D'où la nécessité de cette ligne qui n'est pas un alourdissement du code mais est nécessaire compte tenu de la structure des données que l'on traite. 
# 
# Le test suivant montre que la fonction saute des lignes pour du code source ne contenant qu'une seule ligne. 

# In[4]:


ipynb = v0.load_ipynb("samples\errors.ipynb")
print(v0.to_percent(ipynb)) 


# In[5]:


ipynb = v0.load_ipynb("samples\images.ipynb")
print(v0.to_percent(ipynb)) 


# **Question 4** Le but de la question était de coder la fonction `to_stardom`     
# 
# Pour la fonction `to_starboard`on a réutilisé le code de la question suivante et adapté aux exigence du format. 

# In[6]:


ipynb = v0.load_ipynb("samples/errors.ipynb")
html = v0.to_starboard(ipynb)  
print(html) 


# In[7]:


html = v0.to_starboard(ipynb, html=True)
print(html)

notebook_files = Path(".").glob("samples/*.ipynb")
for notebook_file in notebook_files:
    ipynb = v0.load_ipynb(notebook_file)
    starboard_html = v0.to_starboard(ipynb, html=True)
    with open(notebook_file.with_suffix(".html"), "w", encoding="utf-8") as output:
        print(starboard_html, file=output)


# **Question 5** Le but de la question était de coder la fonction `clear_output`

# Comme seul les cellules python peuvent renvoyer une output, on teste d'abord le type de la cellule, puis on affecte au clées des dictionnaires les valeurs choisies. Cela raccourci beaucoup les dictionnaires obtenues ! Les tests fonctionnent pour tous les Notebooks ici, par exemple ici `streams`

# In[10]:


ipynb = v0.load_ipynb("samples/streams.ipynb")
pprint.pprint(ipynb)

print('\n \n cleared\n \n')

v0.clear_outputs(ipynb)
pprint.pprint(ipynb)


# **Question 6** Le but de la question était de coder la fonction `get_stream`

# En regardant le contenu des cellules du fichiers `streams`, on a compris que `name` contenait le type d'outputs que l'on souhaitait acquérir par cette fonction. Il était alors judicieux d'utliser les connecteurs logiques pour vérifier la concordance des attributs entre chaques cellules. 
# 
# Il est important de noter que cette fonction ne renvoie rien avec des outputs orginal comme des images (fichier`images`) ou des erreurs (fichier `errors`) car les clées utilisés dans le dictionnaire des outputs sont différentes. Ce n'est plus `name`mais `ename`pour les erreurs par exemple. 
# 
# On a également du faire attention lorsque les listes outputs étaient vides (fichiers `minimal`, `images`, ou après `clear_outputs` par exemple), à implémenter un test qui ne renvoie pas d'IndexError mais simplement rien, puisqu'il n'y a pas d'outputs. D'où l'ajout d'un test 
# ```python 
# if cell['outputs']:
# ```
# qui teste si la liste est vide et permet alors de ne pas avoir d'IndexError lorsque la liste est vide. Cela peut sembler superflue pour l'exemple `streams`mais c'est essentiel pour d'autres données. 

# In[8]:


ipynb = v0.load_ipynb("samples/images.ipynb")
print(v0.get_stream(ipynb))
print(v0.get_stream(ipynb, stdout=False, stderr=True))
print(v0.get_stream(ipynb, stdout=True, stderr=True))


# In[9]:


ipynb = v0.load_ipynb("samples/errors.ipynb")
print(v0.get_stream(ipynb))
print(v0.get_stream(ipynb, stdout=False, stderr=True))
print(v0.get_stream(ipynb, stdout=True, stderr=True))


# **Question 7** Le but de la question était de coder la fonction `get_exceptions`   
# 
# Ici, il fallait encore s'assurer que la fonction ne plante pas pour des notebooks qui contiennent des outputs vide ou alors simplement qui ne contiennent pas d'erreurs. On a donc recyclé le tests de la question précédente. On a également adapté les clées à lire dans le dictionnaires au type de données (ici la clé à utiliser était `ename`)

# In[ ]:


ipynb = v0.load_ipynb("samples/images.ipynb")
errors = v0.get_exceptions(ipynb)
all(isinstance(error, Exception) for error in errors)
for error in errors:
        print(repr(error))


# **Question 8** Le but de la question était de coder la fonction `get_images`    
# 
# La parte la plus dur de la question était de trouver comment savoir si un notebook contenait une image. Pour cela, j'ai choisi de considérer que le Notebook contenait une image si son code source contenait l'appel `imread`de matplotlib, puisque c'est à partir de ce moment qu'on peut vértablement exploiter l'image, et détecter lire l'image et savoir que l'outputs n'est pas un `np.array` comme les autre. De plus, détecter l'ouverture d'un fichier `.jpg`était plus difficile. On inspecte donc le code source des cellules python.

# In[ ]:


ipynb = v0.load_ipynb("samples/images.ipynb")
ipynb


# # Notebook_v1 et Notebook_v2   
# 

# ### Classe Cell, MarkdownCell et CodeCell
# 
# **Remarque générale** Il semblerait que certains des fichiers d'exemples contiennent des cellules qui ne possèdent pas d'attribut id, par exemple le fichiers 'streams' mas aussi le fichiers 'errors'. 

# In[ ]:


ipynb = v0.load_ipynb("samples/streams.ipynb")
cells = v0.get_cells(ipynb)
pprint.pprint(cells)


# On a alors eu l'idée dans chaque classe d'essayer si les cellules que l'on cherchait à initialiser ont bien une `id`. Dans le cas contraire, on a alors atribué l'id ```no documented id``` à la cellule. C'est pour cela que l'on verra apparaitre régulièrement le code (ou une variante):
# 
# ```python 
# try: 
#     self.id = ipynb['id']
# except KeyError:
#     self.id = 'no documented id'
# ```
# Ainsi avec cette nouvelle classe, voici le rendu de l'Outline du notebook test `errors`, qui sans l'ajout des test `try\except` retournerait une `KeyError`. 
# 

# In[ ]:


nb = v2.NotebookLoader("samples/errors.ipynb").load()
nb2 = v2.MarkdownLesser(nb).remove_markdown_cells()
print(v1.Outliner(nb2).outline())


# On a bien un outline correct de cette façon. 

# ### Classe Outliner  et Serializer
# 
# De plus, pour que les classes `Outliner` et `Serializer` fonctionnent pour les deux classes CodeCell et MarkdownCell du Notebook v1 et v2, 
# on est obligé d'ajouter un attribut type à chacune des cellules. C'est un peu lourd, puisqu'on dispose déjà de la méthode ``Isinstance``. Cependant, celle-ci génère des problèmes car elle teste les classe du notebook v1 et pas celle de v2. On a donc pas d'interopérabilité de la classe ``Outliner``. Finalement, l'attribut ``type`` est en fait le moins contraignant.    
# Pour le notebook_v1, on a bien: 

# In[ ]:


nb = v1.Notebook.from_file("samples/hello-world.ipynb")
o = v1.Outliner(nb)
print(o.outline())


# Et pour le notebook_v2, on a exactement le même rendu. 

# In[ ]:


nb = v2.NotebookLoader("samples/hello-world.ipynb").load()
print(v2.Outliner(nb).outline())


# Pour la classe `Serializer` on s'en rend compte au moment de l'appel de la classe Markdownizer. Le fichier était crée mais n'était pas accessible à la lecture avec la méthode `Isinstance`

# In[14]:


nb = v2.NotebookLoader("samples/hello-world.ipynb").load()
nb2 = v2.Markdownizer(nb).markdownize()
print(nb2.version)
for cell in nb2:
     print(cell.id)
print(isinstance(nb2.cells[1], v2.MarkdownCell))
v1.Serializer(nb2).to_file("samples/hello-world-markdown.ipynb")

