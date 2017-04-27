#!/bin/bash

if [[ $# != 1 ]]; then
    echo "Usage: $0 <version>"
    echo ""
    echo "eg: $0 1.2.1"
    exit
fi

VERSION=$1

VS=(${VERSION//\./ })
if [[ ${#VS[@]} != 3 ]]; then
    echo "Error: version must have 3 numbers separated by periods, eg 1.2.1"
    exit
fi

PRIO=$(printf "%d%02d%02d0" ${VS[0]} ${VS[1]} ${VS[2]})

echo "Using version $VERSION and priority $PRIO..."

CHDATE=`date "+* %a %b %d %Y"`
CHAUTHOR="Stephane Epardaud <stef\@epardaud.fr>"

perl -pi -e "s/(#.*\@NEW_VERSION\@)/RPMS=\"\\\$RPMS ceylon-${VERSION}-${VERSION}-0.noarch.rpm\"\n\$1/" repo/build.sh
perl -pi -e "s/^(%changelog)$/\$1\n$CHDATE $CHAUTHOR ${VERSION}-0\n- New version ${VERSION}/" dist-pkg/ceylon.spec
perl -pi -e "s/^(%define major_version) .*$/\$1 ${VS[0]}/" dist-pkg/ceylon.spec
perl -pi -e "s/^(%define minor_version) .*$/\$1 ${VS[1]}/" dist-pkg/ceylon.spec
perl -pi -e "s/^(%define micro_version) .*$/\$1 ${VS[2]}/" dist-pkg/ceylon.spec
perl -pi -e "s/^(%define alternatives_version) .*$/\$1 ${PRIO}/" dist-pkg/ceylon.spec
git commit -a -m "New version $VERSION"

git checkout -q -b version-${VERSION}

git push --set-upstream origin version-$VERSION
git tag $VERSION
git push origin $VERSION

