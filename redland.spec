Name:           redland
Version:        1.0.7
Release:        11%{?dist}
Summary:        RDF Application Framework

Group:          System Environment/Libraries
License:        LGPLv2+ or ASL 2.0
URL:            http://librdf.org/
Source:         http://download.librdf.org/source/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxml2-devel >= 2.4.0
BuildRequires:  curl-devel
BuildRequires:  rasqal-devel >= 0.9.15
BuildRequires:  raptor-devel >= 1.4.16
BuildRequires:  db4-devel
BuildRequires:  mysql-devel
BuildRequires:  sqlite-devel
BuildRequires:  postgresql-devel
BuildRequires:  gtk-doc

%description
Redland is a library that provides a high-level interface for RDF
(Resource Description Framework) implemented in an object-based API.
It is modular and supports different RDF/XML parsers, storage
mechanisms and other elements. Redland is designed for applications
developers to provide RDF support in their applications as well as
for RDF developers to experiment with the technology.

%package         devel
Summary:         Libraries and header files for programs that use Redland
Group:           Development/Libraries
Requires:        %{name} = %{version}-%{release}
Requires:        raptor-devel >= 1.4.16
Requires:        rasqal-devel >= 0.9.15
Requires:        pkgconfig

%description     devel
Header files for development with Redland.

%prep
%setup -q

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif

# hack around SQLITE_API macro collision with newer sqlite
sed -i.REDLAND_SQLITE_API -e "s|SQLITE_API|REDLAND_SQLITE_API|" \
  configure.ac configure librdf/rdf_config.h.in librdf/rdf_storage_sqlite.c


%build
# disable-static does not work if we override to use the system's libtool
%configure \
  --enable-release \
  --with-raptor=system --with-rasqal=system --with-threestore=no \
  --disable-static

make %{?_smp_mflags}

%check
make check

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name \*.la -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING.LIB ChangeLog LICENSE.txt NEWS README
%doc LICENSE-2.0.txt NOTICE
%doc *.html
%{_libdir}/librdf.so.0*
%{_bindir}/rdfproc
%{_bindir}/redland-db-upgrade
%dir %{_datadir}/redland
#{_datadir}/redland/mysql-v1.ttl
#{_datadir}/redland/mysql-v2.ttl
%{_mandir}/man1/redland-db-upgrade.1*
%{_mandir}/man1/rdfproc.1*
%{_mandir}/man3/redland.3*

%files devel
%defattr(-,root,root,-)
%{_bindir}/redland-config
%{_libdir}/librdf.so
%{_includedir}/redland.h
%{_includedir}/librdf.h 
%{_includedir}/rdf_*.h
%{_mandir}/man1/redland-config.1*
%{_libdir}/pkgconfig/redland.pc
%{_datadir}/redland/Redland.i
%{_datadir}/redland/mysql*
%{_datadir}/gtk-doc/html/redland/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Fri Feb 12 2010 Lukas Tinkl <ltinkl@redhat.com> - 1.0.7-11
- Related: rhbz#543948
  bump release (extra characters after dist tag) and reenable mysql support

* Fri Aug 28 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0.7-10.1
- temporarily drop mysql support (restore once mysql is unbroken in rawhide)

* Thu Aug 27 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0.7-10
- fix build with newer sqlite (#519781)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.7-9
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.7-7
- slighgly less ugly rpath hack
- cleanup %%files

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0.7-5 
- respin (mysql)

* Fri Jan 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.7-4
- rebuild for new OpenSSL

* Sun Nov 23 2008 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.7-3
- updated summary
- not rebuilt yet 

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.7-2
- rebuild for db4-4.7

* Sat Feb 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.7-1
- update to 1.0.7
- update minimum raptor and rasqal versions

* Tue Dec 04 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.6-3
- respin for openssl

* Tue Oct 16 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.6-2
- fix unpackaged files and unowned directory

* Tue Oct 16 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.6-1
- update to 1.0.6 (for Soprano 2, also some bugfixes)
- update minimum raptor and rasqal versions
- drop sed hacks for dependency bloat (#248106), fixed upstream

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.5-6
- respin (BuildID)

* Fri Aug 3 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.5-5
- specify LGPL version in License tag

* Sat Jul 14 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.5-4
- get rid of redland-config dependency bloat too (#248106)

* Sat Jul 14 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.5-3
- fix bug number in changelog

* Sat Jul 14 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.5-2
- add missing Requires: pkgconfig to the -devel package
- get rid of pkgconfig dependency bloat (#248106)

* Thu Jun 28 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.0.5-1
- update to 1.0.5 (1.0.6 needs newer raptor and rasqal than available)
- update minimum raptor version

* Fri Dec 15 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.4-3
- use DESTDIR

* Sat Jun 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.4-2
- fixed x86_64 rpath issue with an ugly hack
- removed OPTIMIZE from make invocation
- added smp flags
- added make check
- updated license

* Sun May 14 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.4-1
- update to new release, needs later raptor
- remove patch

* Sat Apr 08 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.3-1
- update to latest release
- include patch for fclose() double-free

* Sat Apr 08 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.2-1
- package for Fedora Extras

* Wed Feb 15 2006  Dave Beckett <dave@dajobe.org>
- Require db4-devel

* Thu Aug 11 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Update Source:
- Do not require python-devel at build time
- Add sqlite-devel build requirement.
- Use configure and makeinstall

* Thu Jul 21 2005  Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for gtk-doc locations

* Mon Nov 1 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- License now LGPL/Apache 2
- Added LICENSE-2.0.txt and NOTICE

* Mon Jul 19 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- move perl, python packages into redland-bindings

* Mon Jul 12 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- put /usr/share/redland/Redland.i in redland-devel

* Wed May  5 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- require raptor 1.3.0
- require rasqal 0.2.0

* Fri Jan 30 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- require raptor 1.2.0
- update for removal of python distutils
- require python 2.2.0+
- require perl 5.8.0+
- build and require mysql
- do not build and require threestore

* Sun Jan 4 2004  Dave Beckett <dave.beckett@bristol.ac.uk>
- added redland-python package
- export some more docs

* Mon Dec 15 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- require raptor 1.1.0
- require libxml 2.4.0 or newer
- added pkgconfig redland.pc
- split redland/devel package shared libs correctly

* Mon Sep 8 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- require raptor 1.0.0
 
* Thu Sep 4 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- added rdfproc
 
* Thu Aug 28 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- patches added post 0.9.13 to fix broken perl UNIVERSAL::isa
 
* Thu Aug 21 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- Add redland-db-upgrade.1
- Removed duplicate perl CORE shared objects

* Sun Aug 17 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- Updates for new perl module names.

* Tue Apr 22 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for Redhat 9, RPM 4

* Fri Feb 12 2003 Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for redland 0.9.12

* Fri Jan 4 2002 Dave Beckett <dave.beckett@bristol.ac.uk>
- Updated for new Perl module names

* Fri Sep 14 2001 Dave Beckett <dave.beckett@bristol.ac.uk>
- Added shared libraries
