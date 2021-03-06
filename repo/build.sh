#!/bin/sh

set -e

RPMS="ceylon-1.0.0-1.0.0-0.noarch.rpm"
RPMS="$RPMS ceylon-1.1.0-1.1.0-0.noarch.rpm"
RPMS="$RPMS ceylon-1.1.0-1.1.0-1.noarch.rpm"
RPMS="$RPMS ceylon-1.2.0-1.2.0-0.noarch.rpm"
RPMS="$RPMS ceylon-1.2.1-1.2.1-1.noarch.rpm"
RPMS="$RPMS ceylon-1.2.2-1.2.2-0.noarch.rpm"
RPMS="$RPMS ceylon-1.3.0-1.3.0-0.noarch.rpm"
RPMS="$RPMS ceylon-1.3.1-1.3.1-1.noarch.rpm"
RPMS="$RPMS ceylon-1.3.2-1.3.2-0.noarch.rpm"
RPMS="$RPMS ceylon-1.3.3-1.3.3-0.noarch.rpm"
# @NEW_VERSION@
rm -rf repodata

for pkg in $RPMS
do
 if test -f $pkg
 then
  echo "Not downloading $pkg: already there"
 else
  wget http://downloads.ceylon-lang.org/cli/$pkg
 fi
done

rpm --addsign $RPMS
createrepo .
