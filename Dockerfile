#FROM debian:buster-slim
FROM continuumio/miniconda3

MAINTAINER Valentino Lauciani <valentino.lauciani@ingv.it>

#
ENV DEBIAN_FRONTEND=noninteractive
ENV INITRD No
ENV FAKE_CHROOT 1

RUN conda install -c conda-forge obspy

COPY ./mseed2wa.py /opt/

