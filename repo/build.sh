#!/bin/sh

RPMS="ceylon-1.0.0-1.0.0-0.noarch.rpm \
 ceylon-1.1.0-1.1.0-0.noarch.rpm \
 ceylon-1.1.0-1.1.0-1.noarch.rpm \
 ceylon-1.2.0-1.2.0-0.noarch.rpm \
 ceylon-1.2.1-1.2.1-0.noarch.rpm" 
rm -rf repodata

for pkg in $RPMS
do
 if test -f $okg
 then
  echo "Not downloading $pkg: already there"
 else
  wget http://downloads.ceylon-lang.org/cli/$pkg
 fi
done

createrepo $RPMS
rpm --addsign $RPMS
