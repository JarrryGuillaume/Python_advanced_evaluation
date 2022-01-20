#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pour git 
from black import re
import notebook_v0 as toolbox
import pprint
import json

"""
an object-oriented version of the notebook toolbox
"""

class Cell:
    def __init__(self, ipynb): 
        try: 
            self.id = ipynb['id']
        except KeyError:
            self.id = 'no documented id'
            
        self.source = ipynb['source']


class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    def __init__(self, ipynb):
        super().__init__(ipynb)
        self.execution_count = ipynb['execution_count']
        self.type = 'CodeCell'


class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    def __init__(self, ipynb): 
        super().__init__(ipynb)
        self.type = 'MarkdownCell'

class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """

    def __init__(self, ipynb):
        self.version = toolbox.get_format_version(ipynb)
        cells = []
        for cell in toolbox.get_cells(ipynb):
            if cell['cell_type'] == 'markdown':
                cells.append(MarkdownCell(cell))
            elif cell['cell_type'] == 'code':
                cells.append(CodeCell(cell))
        self.cells = cells
        

    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        return Notebook(toolbox.load_ipynb(filename))

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        return iter(self.cells)


# +
    
class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'metadata': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'metadata': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'metadata': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def serialize(self):
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """        
        # On a été obligé de réécrire tous les dictionnaires pour garder les clées dans le bon ordre.
        # Ajoutons un objet metadata aux cellules
        serie = self.notebook
        cells = []
        for cell in serie.cells:
            JSON_cell = {}
            if cell.type == 'CodeCell':
                JSON_cell = {'cell_type': 'code',
                         'id': cell.id,
                         'metadata': {},
                         'execution_count': cell.execution_count,
                         'outputs': [],
                         'source': cell.source}
            elif cell.type == 'MarkdownCell':
                JSON_cell = {'cell_type': 'markdown',
                         'id': cell.id,
                         'metadata': {},
                         'source': cell.source}
        
            cells.append(JSON_cell)
        
        # On peut alors créer le notebook avec son objet metadata 
        JSON = {'cells': cells, 
               'metadata': {}, 
               'nbformat': int(serie.version[0]), 
               'nbformat_minor': int(serie.version[-1])} 
        
        return JSON 

        

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        JSON = Serializer.serialize(self)
        toolbox.save_ipynb(JSON, filename)


# -

class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    
    
    
    def __init__(self, notebook):
        self.notebook = notebook

    def to_py_percent(self):
        r"""Converts the notebook to a string in py-percent format.
        """
        # Utilisons la classe Serialize pour obtenir un ipynb (dict) valide 
        series = Serializer(self.notebook)
        ipynb = series.serialize()        
        percent = toolbox.to_percent(ipynb)
    
        # Ajoutons maintenant les <BLANKLINE> 
        lines = percent.split('\n')
        res = [lines[0]]
        for k, line in enumerate(lines[1:]): # Attention à l'indice de k. Correspond à l'indice k - 1 de lines
            if '# %%' == line or '# %% [markdown]' == line: # On vérifie le saut de cellule 
                res.extend(['', line])
            else:
                res.append(line)
                
        # Et reconvertissons la liste de ligne en str 
        res = '\n'.join(res)
            
        return res

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        content = PyPercentSerializer.to_py_percent(self)
        with open(filename, 'w', encoding = 'utf-8') as percent_file:
            percent_file.write(content)


class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def outline(self):
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        nb = self.notebook
        res = f'Jupyter Notebook v{nb.version}\n'
        for cell in nb: 
            
            if cell.type == 'MarkdownCell':
                res += f'└─▶ Markdown cell #{cell.id}' + '\n'
            elif cell.type == 'CodeCell':
                res += f'└─▶ Code cell #{cell.id} ({cell.execution_count})' + '\n'
            
            if len(cell.source) == 1: # Attention, il faut formater la parenthèse qui contient la source
                res += '    | ' + cell.source[0] + '\n'
            else: 
                for s, line in enumerate(cell.source): # ce qui requiert une myriade de test 
                    if s == 0: 
                        res += '    ┌ ' + line 
                    elif s == len(cell.source)-1:
                        res += '    └ ' + line + '\n'
                    else: 
                        res += '    | ' + line 
                
        return res
