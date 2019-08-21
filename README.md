# Memorias del Olvido

Memorias del Olvido is a Twitter bot made in Python 3 using the Tweepy library.

Its main goal is to poll news sites each interval of time to check for fresh news about Alzheimer's disease and tweet them.

The structure of the bot allows multiple providers to be added and configured seamlessly, delegating tweet composition responsibility on the own provider. This allows matching criteria for certain news sites that require a particular way of citing or hashtagging.

The bot runs on a single thread and it's made to run standalon on a Python 3.7 installation.

## Setup

Just install the dependencies with:

`pip install -r requirements.txt`

Configure the bot with an `.env` file on the root of the package. An `.env.example` file is provided to aid you.

And run the bot with:

`python main.py`

And you should good to go.

## Developing a news provider

A new module for a news provider should only contain one function that returns a list of strings to tweet. You can check the `example.py` provider to have an idea on how to work with it.

## License

This repository is licensed under the MIT license. An extract of the license text is posted here. However a `LICENSE` file is included in the repository:

```
The MIT License

Copyright (c) 2010-2019 Google, Inc. http://angularjs.org

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```