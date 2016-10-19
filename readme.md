# PyTikZ
## Description

This project contains a simple tikz code generator in Python.

## Getting started

A couple examples can be found in [examples/](examples/).  The
workflow consists of creating a tikz code generator object and
constructing objects in [tikz/wrappers.py](tikz/wrappers.py) through
the generator object.

## Adding wrappers

If a desired tikz object is not already wrapped, just add a class in
[tikz/wrappers.py](tikz/wrappers.py) and inherit from the wrapper
class.
