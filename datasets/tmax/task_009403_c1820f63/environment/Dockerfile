FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

COPY post_install.sh /tmp/post_install.sh
RUN bash /tmp/post_install.sh && rm /tmp/post_install.sh
