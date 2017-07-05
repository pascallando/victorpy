---
title: Installation
description: Learn how to install VictorPy.
position: 100
tags:
    - pip
---

{% prog_name %} is a Python lib: installation is just done as any other Python lib.

## Pip

To install {% prog_name %}, just type:

```bash
$ pip3 install victorpy
```

### Checking your installation

Installation process creates a `victorpy` command for you.

Open a terminal, and check everything works:

```bash
$ victorpy -h

INFO VictorPy
usage: victorpy [-h] [serve] [build]

A simple yet powerful static site generator

positional arguments:
  serve       Launch live server on local directory
  build       Generate site files in build directory

optional arguments:
  -h, --help  show this help message and exit
```

## Requirements

- Python 3