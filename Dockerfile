FROM docker.io/archlinux:latest

RUN pacman -Syu --noconfirm && pacman -S --noconfirm python python-pip python-virtualenv

RUN pacman -S --noconfirm texlive-basic \
                          texlive-bibtexextra \
                          texlive-bin \
                          texlive-binextra \
                          texlive-fontsextra \
                          texlive-fontutils \
                          texlive-langenglish \
                          texlive-langeuropean \
                          texlive-latexextra \
                          texlive-latexrecommended \
                          texlive-mathscience \
                          texlive-meta \
                          texlive-pictures \
                          texlive-publishers \
                          texlive-xetex \
                          texlive-formatsextra

COPY ./dist/cvcreator-1.1.15-py2.py3-none-any.whl /

RUN python -m virtualenv .venv && source .venv/bin/activate && pip install cvcreator-1.1.15-py2.py3-none-any.whl
