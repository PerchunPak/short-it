# short-it

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)

[![Build Status](https://github.com/PerchunPak/short-it/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/short-it/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/PerchunPak/short-it/branch/master/graph/badge.svg)](https://codecov.io/gh/PerchunPak/short-it)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

My personal link shorter adapted to my needs and special link structure!

## Features

- Free! We don't want any money from you!
- Add yours!

## Installing

```bash
pip install short-it
```

## Installing for local developing

```bash
git clone https://github.com/PerchunPak/short-it.git
cd short-it
```

### Installing `poetry`

Next we need install `poetry` with [recommended way](https://python-poetry.org/docs/master/#installation).

If you use Linux, use command:

```bash
curl -sSL https://install.python-poetry.org | python -
```

If you use Windows, open PowerShell with admin privileges and use:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Installing dependencies

```bash
poetry install --no-dev
```

### Configuration

All configuration happens in `config.yml`, or with enviroment variables.

### If something is not clear

You can always write me!

## Example

```py
from short_it.example import some_function

print(some_function(3, 4))
# => 7
```

## Updating

```bash
pip install -U short-it
```

### For local development

For updating, just re-download repository (do not forget save config),
if you used `git` for downloading, just run `git pull`.

## Thanks

This project was generated with [python-template](https://github.com/PerchunPak/python-template).
