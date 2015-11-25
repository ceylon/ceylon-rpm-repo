## Generate an RPM repo for Ceylon

You need to have an RPM-based machine (Fedora/RHEL works) for this to work.

Install the createrepo package:

    $ sudo yum install createrepo

Make sure you have the private GPG key to be allowed to sign.

Now make the repo:

    $ ./build.sh

This will download any rpm file for Ceylon unless already present in the current folder,
sign them and create an RPM repo in `repodata`.
