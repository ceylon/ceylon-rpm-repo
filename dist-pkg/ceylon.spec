# *** BEGIN LICENSE BLOCK ***
#
# *** END LICENSE BLOCK ***

%define section free

%define major_version 1
%define minor_version 3
%define micro_version 2

# Make sure the following is [MAJOR][MINOR][MICRO]0 with MINOR and MICRO being 0-padded to 2 digits (yes, there's an extra 0 on the end)
%define alternatives_version 103020

%define ceylon_home /usr/lib/ceylon/%{major_version}.%{minor_version}.%{micro_version}

# The name of the source zip file (without .zip)
%define name_source %{name}
# The name of the root folder within the source zip
%define folder_source %{name}

# Make sure rpmbuild leaves JAR files alone!
%define __jar_repack 0
%global __provides_exclude ^.*$
%global __requires_exclude ^.*$

Name: ceylon-%{version}
Epoch: 0
Version: %{major_version}.%{minor_version}.%{micro_version}
Release: 1
Summary: Ceylon language

Group: Development/Languages
License: ASL 2.0 and GPL v 2 + Classpath exception
URL: http://www.ceylon-lang.org//
Source0: http://downloads.ceylon-lang.org/cli/%{name_source}.zip
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
BuildRequires: zip
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
AutoReqProv: no

%description
Ceylon is a programming language for writing large programs in a team
environment. The language is elegant, highly readable, extremely typesafe,
and makes it easy to get things done. And it's easy to learn for programmers
who are familiar with mainstream languages used in business computing.
Ceylon has a full-featured Eclipse-based development environment, allowing
developers to take best advantage of the powerful static type system.
Programs written in Ceylon execute on any JVM.

%prep
%setup -q -n %{folder_source}


%build
export LANG=en_US.UTF-8


%install
rm -rf $RPM_BUILD_ROOT%{ceylon_home}
# CEYLON_HOME and subdirs
mkdir -p $RPM_BUILD_ROOT%{ceylon_home}/{bin,lib,repo,doc,doc/en,samples,templates}
install -d -m 755 %{buildroot}%{_mandir}/man1
install -d -m 755 %{buildroot}%{_infodir}

cp -pr BUILDID $RPM_BUILD_ROOT%{ceylon_home}/
cp -pr LICENSE-* $RPM_BUILD_ROOT%{ceylon_home}/
cp -pr bin/* $RPM_BUILD_ROOT%{ceylon_home}/bin
cp -pr repo/* $RPM_BUILD_ROOT%{ceylon_home}/repo
cp -pr lib/* $RPM_BUILD_ROOT%{ceylon_home}/lib
cp -pr doc/en/* $RPM_BUILD_ROOT%{ceylon_home}/doc/en
cp -pr samples/* $RPM_BUILD_ROOT%{ceylon_home}/samples
cp -pr templates/* $RPM_BUILD_ROOT%{ceylon_home}/templates
cp -pr contrib/* $RPM_BUILD_ROOT%{ceylon_home}/contrib
cp -pr doc/en/spec/info/ceylon-spec.info $RPM_BUILD_ROOT%{_infodir}/ceylon-spec-%{version}.info
cp -pr doc/en/spec/info/ceylon-spec.info-1 $RPM_BUILD_ROOT%{_infodir}/ceylon-spec-%{version}.info-1
cp -pr doc/en/spec/info/ceylon-spec.info-2 $RPM_BUILD_ROOT%{_infodir}/ceylon-spec-%{version}.info-2
for man in doc/man/man1/*
do
    tool=$(basename $man .1)
    cp -pr $man $RPM_BUILD_ROOT%{_mandir}/man1/${tool}-%{version}.1
done

%post
INSTALL_LINE="%{_bindir}/ceylon ceylon %{ceylon_home}/bin/ceylon %{alternatives_version}"
INSTALL_LINE="$INSTALL_LINE --slave %{_prefix}/lib/ceylon/ceylon ceylon-dir %{_prefix}/lib/ceylon/%{version}"
INSTALL_LINE="$INSTALL_LINE --slave %{_mandir}/man1/ceylon.1 ceylon-main-man %{_mandir}/man1/ceylon-%{version}.1.gz"
for man in %{_mandir}/man1/ceylon-*
do
    tool=$(basename $man .1)
    INSTALL_LINE="$INSTALL_LINE --slave $man ${tool}-man %{_mandir}/man1/${tool}-%{version}.1.gz"
done
INSTALL_LINE="$INSTALL_LINE --slave %{_infodir}/ceylon-spec.info ceylon-info %{_infodir}/ceylon-spec-%{version}.info.gz"
INSTALL_LINE="$INSTALL_LINE --slave %{_infodir}/ceylon-spec.info-1 ceylon-info-1 %{_infodir}/ceylon-spec-%{version}.info-1.gz"
INSTALL_LINE="$INSTALL_LINE --slave %{_infodir}/ceylon-spec.info-2 ceylon-info-2 %{_infodir}/ceylon-spec-%{version}.info-2.gz"

%{_sbindir}/update-alternatives --install $INSTALL_LINE

%postun
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove ceylon %{ceylon_home}/bin/ceylon
fi

%files
%defattr(-,root,root)
%attr(755,root,root) %{ceylon_home}/bin/ceylon
%attr(755,root,root) %{ceylon_home}/bin/ceylon.bat
%{ceylon_home}/bin/ceylon-sh-setup
%{ceylon_home}/bin/ceylon-sh-setup.bat
%{ceylon_home}/bin/*.plugin
%{ceylon_home}/repo/*
%{ceylon_home}/lib/*
%doc %{ceylon_home}/doc/*
%doc %{_mandir}/man1/*
%doc %{_infodir}/*
%{ceylon_home}/samples/*
%{ceylon_home}/templates/*
%{ceylon_home}/contrib/*
%{ceylon_home}/BUILDID
%{ceylon_home}/LICENSE-*


%changelog
* Wed Mar 1 2017 Tako Schotanus <tschotan@redhat.com> 1.3.2-0
- Update for 1.3.2
* Mon Nov 21 2016 Tako Schotanus <tschotan@redhat.com> 1.3.1-1
- New release for 1.3.1 because of bugs
* Fri Nov 18 2016 Tako Schotanus <tschotan@redhat.com> 1.3.1-0
- Update for 1.3.1
* Wed Sep 14 2016 Tako Schotanus <tschotan@redhat.com> 1.3.0-0
- Update for 1.3.0
* Tue Mar 8 2016 Tako Schotanus <tschotan@redhat.com> 1.2.2-0
- Update for 1.2.2
* Thu Feb 11 2016 Tako Schotanus <tschotan@redhat.com> 1.2.1-1
- Fixed problem with alternatives
* Thu Feb 4 2016 Tako Schotanus <tschotan@redhat.com> 1.2.1-0
- Update for 1.2.1
* Wed Oct 28 2015 Tako Schotanus <tschotan@redhat.com> 1.2.0-0
- Update for 1.2.0
- Now installing .info files as well
* Fri Oct 10 2014 Tako Schotanus <tschotan@redhat.com> 1.1.0-2
- Fixed installation of man pages and main folder link
* Thu Oct 09 2014 Tako Schotanus <tschotan@redhat.com> 1.1.0-1
- Not scanning files for (OSGi) Provides and Requires definitions anymore
- Not copying manual pages to the global directory anymore because that conflicts with the alternatives
* Wed Oct 08 2014 Stephane Epardaud <separdau@redhat.com> 1.1.0-0
- Update for 1.1.0
* Sun Nov 10 2013 Tako Schotanus <tschotan@redhat.com> 1.0.0-0
- Update for 1.0.0
- Added contrib folder
- Using alternatives system now
* Tue Sep 24 2013 Tako Schotanus <tschotan@redhat.com> 0.6.1-0
- Update for 0.6.1
* Fri Sep 20 2013 Stephane Epardaud <separdau@redhat.com> 0.6.0-0
- Update for 0.6
* Wed Mar 13 2013 Tako Schotanus <tschotan@redhat.com> 0.5.0-1
- Removed references to ceylon-cp.sh that doesn't exist anymore
* Wed Oct 31 2012 Tako Schotanus <tschotan@redhat.com> 0.5.0-0
- Update for 0.5
* Thu Oct 25 2012 Stephane Epardaud <separdau@redhat.com> 0.4.0-0
- Update for 0.4
* Fri Jul 06 2012 Tako Schotanus <tschotan@redhat.com> 0.3.1-0
- Update for 0.3.1 and some small changes to simplify updating the version
* Thu Jun 21 2012 Tako Schotanus <tschotan@redhat.com> 0.3.0-1
- Some changes to simplify the build process a bit
* Mon May 14 2012 Stephane Epardaud <separdau@redhat.com> 0.3.0-0
- Update for 0.3
* Thu Mar 15 2012 Stephane Epardaud <separdau@redhat.com> 0.2.0-0
- Update for 0.2
* Tue Dec 20 2011 Mladen Turk <mturk@redhat.com> 0.1.0-0
- Initial build

