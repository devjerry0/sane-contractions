sane-contractions
=================

.. image:: https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml/badge.svg
   :target: https://github.com/devjerry0/sane-contractions/actions/workflows/commit.yml

.. image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT

A fast and comprehensive Python library for expanding English contractions and slang.

**This is an enhanced fork of the original** `contractions <https://github.com/kootenpv/contractions>`_ **library by Pascal van Kooten, with significant improvements in performance, testing, type safety, and maintainability.**

Features
--------

- ⚡ **Fast**: 50x faster than version 0.0.18 (uses efficient Aho-Corasick algorithm)
- 📚 **Comprehensive**: Handles standard contractions, slang, and custom additions
- 🎯 **Smart**: Preserves case and handles ambiguous contractions intelligently
- 🔧 **Flexible**: Easy to add custom contractions on the fly
- 🐍 **Modern**: Supports Python 3.10+

Installation
------------

.. code-block:: bash

    pip install sane-contractions

Quick Start
-----------

.. code-block:: python

    import contractions

    contractions.fix("you're happy now")
    # "you are happy now"

    contractions.fix("I'm sure you'll love it!")
    # "I am sure you will love it!"

Usage Examples
--------------

Basic Contraction Expansion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import contractions

    text = "I'm sure you're going to love what we've done"
    expanded = contractions.fix(text)
    print(expanded)
    # "I am sure you are going to love what we have done"

Case Preservation
~~~~~~~~~~~~~~~~~

.. code-block:: python

    contractions.fix("you're happy")    # "you are happy"
    contractions.fix("You're happy")    # "You are happy"
    contractions.fix("YOU'RE HAPPY")    # "YOU ARE HAPPY"

Adding Custom Contractions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    contractions.add('myword', 'my word')
    contractions.fix('myword is great')
    # "my word is great"

    custom_contractions = {
        "ain't": "are not",
        "gonna": "going to",
        "wanna": "want to"
    }
    contractions.add_dict(custom_contractions)

API Reference
-------------

fix(text, leftovers=True, slang=True)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Expands contractions in the given text.

add(key, value)
~~~~~~~~~~~~~~~

Adds a single custom contraction.

add_dict(dictionary)
~~~~~~~~~~~~~~~~~~~~

Adds multiple custom contractions at once.

preview(text, flank)
~~~~~~~~~~~~~~~~~~~~

Preview contractions in text before expanding.

Requirements
------------

- Python 3.10 or higher
- textsearch >= 0.0.21

License
-------

MIT License

Credits
-------

**Original Author:** Pascal van Kooten (@kootenpv)

**Fork Maintainer:** Jeremy Bruns

**Original Repository:** https://github.com/kootenpv/contractions

This project would not exist without Pascal's excellent foundation.
