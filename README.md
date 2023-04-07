# short-it

[![Support Ukraine](https://badgen.net/badge/support/UKRAINE/?color=0057B8&labelColor=FFD700)](https://www.gov.uk/government/news/ukraine-what-you-can-do-to-help)

[![Build Status](https://github.com/PerchunPak/short-it/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/PerchunPak/short-it/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/PerchunPak/short-it/branch/master/graph/badge.svg)](https://codecov.io/gh/PerchunPak/short-it)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

My personal link shorter adapted to my needs and special link structure!

## Special structure

The links are separated to two types. Project and simple.

### Project links

Those will be used for projects, which have a bunch of links, and I want to
group them together. For example, I have a project `short-it`, and I want to
have a link to its repository, documentation, and so on. So I will create a
project `short-it`, and then add links to it.

```yaml
# data/config.yml
projects:  # This is a list of projects
  short-it:  # a project name
    github:  # a link type
      to: https://github.com/PerchunPak/short-it  # a destination
      # parsed into 'example.com/short-it/github'
    readme:  # another link type
      to: https://github.com/PerchunPak/short-it#readme
      aliases:  # add more aliases
        - info
        - about
      # parsed into three different links with the same destination:
      # 'example.com/short-it/readme'
      # 'example.com/short-it/info'
      # 'example.com/short-it/about'
```

The aliases attribute is just a syntax sugar, it's equal to:

```yaml
projects:
  short-it:
    readme:
      to: https://github.com/PerchunPak/short-it#readme
    info:
      to: https://github.com/PerchunPak/short-it#readme
    about:
      to: https://github.com/PerchunPak/short-it#readme
```

> **Note**
> 
> We auto adding some aliases to the chosen links. You can overwrite those by setting `aliases`
> attribute or add more aliases with `additional_aliases` attribute.
> 
> You can find all such aliases [here](https://github.com/PerchunPak/short-it/blob/master/short_it/config.py#L28-L34).

### Simple links

Those will be used for simple links, which have only one destination. For
example, I want to have a link to my GitHub profile, so I will create a simple
link `github`.

```yaml
# data/config.yml
simple:  # This is a list of simple links
  github: https://github.com/PerchunPak  # a link name and a destination *inline*
  site: https://perchun.it
```

## Self-hosting

I recommend using Docker for hosting the project, but if you don't want to, you can just follow
`for local developing` instructions and in the end use
`uvicorn short_it.app:app --proxy-headers --host 0.0.0.0 --port 80`.
Below will be instructions for hosting in Docker.

Firstly, you need to install Docker, follow instructions [here](https://docs.docker.com/get-docker/).

Then you need to create a directory for the project, and create a file `data/config.yml` in it.
Be sure that you give the correct permissions to the file. If you don't know how to do it, just run
`chmod 777 data/config.yml` (only for Linux) in the project directory.

Then you can run the project with the following command:

```bash
docker run -d --name short-it -p 80:80 -v $(pwd)/data:/app/data perchunpak/short-it
```

Application should generate config, and you can edit it. But before, stop the app with `docker stop short-it`
and, after you edited the config, start it again with `docker start short-it`.

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
poetry install
```

### Configuration

All configuration happens in `data/config.yml`. The structure was described [here](#special-structure)

### If something is not clear

You can always write to me!

## Updating

Just run `docker pull perchunpak/short-it` and `docker restart short-it`.

### For local development

For updating, just re-download repository (don't forget to save config),
if you used `git` for downloading, just run `git pull`.

## Thanks

This project was generated with [python-template](https://github.com/PerchunPak/python-template).
