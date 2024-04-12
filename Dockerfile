FROM docker.io/ubuntu:latest

RUN apt-get update && apt-get -y upgrade && apt-get autoremove && apt-get autoclean

RUN apt-get install -y texlive-latex-base \
                       texlive-fonts-recommended \
                       texlive-fonts-extra \
                       texlive-latex-extra \
                       texlive-lang-european

RUN apt-get install -y latexmk

RUN apt-get install -y python3-full python3-pip python3-pip-whl python-is-python3

COPY ./dist/cvcreator-1.1.17-py2.py3-none-any.whl /
RUN python -m venv .venv && .venv/bin/python -m pip install cvcreator-1.1.17-py2.py3-none-any.whl
