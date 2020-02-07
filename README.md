[![Build Status](https://travis-ci.com/jcs-workspace/swagger-it.svg?branch=master)](https://travis-ci.com/jcs-workspace/swagger-it)
[![Unity Engine](https://img.shields.io/badge/python-%3E=_3.6-green.svg)](https://www.python.org/downloads/)
[![Release Tag](https://img.shields.io/github/tag/jcs-workspace/swagger-it.svg?label=release)](https://github.com/jcs-workspace/swagger-it/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# swagger-it
> Automatically generate swagger.io yaml file from your project.
yaml file.

This turn your workflow around by code first then generate an update to date
API documentation.


<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [swagger-it](#swagger-it)
    - [Command Line](#command-line)
        - [-](#-)
    - [Installation](#installation)
    - [Supported Languages](#supported-languages)
    - [Todo List](#todo-list)
    - [References](#references)

<!-- markdown-toc end -->


## Command Line

Full command line design.

```
usage: swagger-it.py [-h] [--input INPUT] [--output OUTPUT] [--version]

swagger-it: Parse your microservice project into a swagger yaml file. (Version 0.0.1)

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT, -i INPUT
                        Input path, this can be a directory or file.
  --output OUTPUT, -o OUTPUT
                        Output path, this must be a path point to a file.
  --version             Display version information and dependencies.
```

#### Example Usage

Parameters `-i` and `-o` are must variables for now.

**[INFO] I am currently working on the parsing comment/docstring.**

```
python -i './' -o './output/file.yml'
```

## Installation

**NOTE**: Python 3.6 or higher is required.

```bash
# clone the repo
$ git clone https://github.com/jcs-workspace/swagger-it.git

# change the working directory to sherlock
$ cd sherlock

# install python3 and python3-pip if they are not installed

# install the requirements
python3 -m pip install -r requirements.txt
```

## Supported Languages

* C
* C++
* Objective-C
* C#
* JavaScript
* Java
* Python
* Go
* Ruby

## Todo List

- [ ] Implementes core changes to generate yaml file.
- [ ] Design the template file. (Make it as extensible as possible)
- [ ] Design the tags and docstring to work together.

## References

* https://github.com/swaggo/swag
* https://editor.swagger.io/?_ga=2.130550666.406048183.1579233982-1663214344.1579233982
