stdin-tagger
==========

[![stdin-tagger version](https://img.shields.io/pypi/v/stdin-tagger.svg)](https://pypi.python.org/pypi/stdin-tagger)
[![stdin-tagger python compatibility](https://img.shields.io/pypi/pyversions/stdin-tagger.svg)](https://pypi.python.org/pypi/stdin-tagger)
[![say thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/msztolcman)

`stdin-tagger` just decorate stdin with current timestamp and optional tag.

If you like this tool, just [say thanks](https://saythanks.io/to/msztolcman).

Current stable version
----------------------

1.0.0

Python version
--------------

`stdin-tagger` works with Python 2.7 and 3.3+.

Some examples
-------------

Some examples:

    # decorate with default timestamp
    % echo something | stdin-tagger
    2019-05-01 09:42:11.141874 something
    
    # decorate with other timestamp format
    % echo something | stdin-tagger --timestamp-format '%Y%m%d%H%M%S'
    20190501094333 something 

    # decorate with other timestamp format and UTC timezone
    % echo something | stdin-tagger --timestamp-format '%Y%m%d%H%M%S' --timezone utc
    20190501074610 something
    
    # add additional tag right after timestamp
    % echo something | stdin-tagger  --additional-tag '[some tag]'
    2019-05-01 09:49:58.775573 [some tag] something

Installation
------------

1. Using PIP

`stdin-tagger` should work on any platform where [Python](http://python.org)
is available, it means Linux, Windows, MacOS X etc. 

Simplest way is to use Python's built-in package system:

    pip install stdin-tagger

2. Using [pipsi](https://github.com/mitsuhiko/pipsi)
  
    pipsi install stdin-tagger

Voila!

Authors
-------

Marcin Sztolcman <marcin@urzenia.net>

Contact
-------

If you like or dislike this software, please do not hesitate to tell me about
this me via email (marcin@urzenia.net).

If you find bug or have an idea to enhance this tool, please use GitHub's
[issues](https://github.com/msztolcman/stdin-tagger/issues).

ChangeLog
---------

### v1.0.0

* first public version
