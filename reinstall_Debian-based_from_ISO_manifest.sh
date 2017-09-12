#!/bin/bash
#
# @Breogan Costa
#
# Purpose: do a full reinstall of all the default packages of your distro. For example: you had removed accidentally more packages than you consider you have should.
#
# INSTRUCTIONS:
#  1.- update manifest_URL with your favourite Debian GNU/Linux-based Distro
#  2.- give run permisions to this script (chmod u+x)
#  3.- run it with SUDO and the manifest URL as parameter, or the default one: for Ubuntu Gnome 17.04, although that is my laptop one ;)

if [ $# == 1 ]; then
  manifest_URL=$1
  echo "Using the given URL: $manifest_URL"
else
  manifest_URL=http://cdimage.ubuntu.com/ubuntu-gnome/releases/17.04/release/ubuntu-gnome-17.04-desktop-amd64.manifest
  echo "Using the default URL: $manifest_URL"
fi

#for pkg in `curl $manifest_URL | awk '{print $1}' | egrep -v '(dpkg|apt|mysql|mythtv)'` ; do  apt-get -y --force-yes install --reinstall $pkg; done

# commnet previous line and uncomment next one if you want to check which packages you will install

for pkg in `curl $manifest_URL | awk '{print $1}' | egrep -v '(dpkg|apt|mysql|mythtv)'` ; do  echo $pkg; done
