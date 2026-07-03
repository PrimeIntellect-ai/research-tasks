FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV GOPATH=/home/user/go
ENV PATH=/home/user/go/bin:/home/user/.cargo/bin:$PATH

COPY base_install.sh /tmp/base_install.sh
RUN bash /tmp/base_install.sh && rm /tmp/base_install.sh

COPY _fixtures/app/fixtures/minicalc/Makefile /app/fixtures/minicalc/Makefile
COPY _fixtures/app/fixtures/minicalc/minicalc.c /app/fixtures/minicalc/minicalc.c
COPY _fixtures/app/fixtures/minicalc/README.md /app/fixtures/minicalc/README.md
COPY _fixtures/app/fixtures/minicalc/_perturbation.json /app/fixtures/minicalc/_perturbation.json

COPY post_install.sh /tmp/post_install.sh
RUN bash /tmp/post_install.sh && rm /tmp/post_install.sh
