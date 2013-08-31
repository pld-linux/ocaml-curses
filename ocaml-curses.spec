#
# Conditional build:
%bcond_without	opt		# build opt

Summary:	OCaml bindings for ncurses
Name:		ocaml-curses
Version:	1.0.3
Release:	7
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://download.savannah.gnu.org/releases/ocaml-tmk/%{name}-%{version}.tar.gz
# Source0-md5:	3c11b46b7c057f8fd110ace319589877
URL:		http://savannah.nongnu.org/projects/ocaml-tmk/
BuildRequires:	autoconf
BuildRequires:	gawk
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	ocaml >= 1:3.10.2
BuildRequires:	ocaml-findlib-devel >= 1.3.3-3
ExcludeArch:	sparc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCaml bindings for ncurses.

%package        devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%configure \
	--enable-widec

%{__make} all opt

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocamlfind install curses META *.cmi *.cmx *.cma *.cmxa *.a *.so *.mli

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/curses
mv $OCAMLFIND_DESTDIR/curses/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/curses

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/ocaml/curses
%exclude %{_libdir}/ocaml/curses/*.mli
%if %{with opt}
%exclude %{_libdir}/ocaml/curses/*.a
%exclude %{_libdir}/ocaml/curses/*.cmxa
%exclude %{_libdir}/ocaml/curses/*.cmx
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_libdir}/ocaml/site-lib/curses

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/curses/*.mli
%if %{with opt}
%{_libdir}/ocaml/curses/*.a
%{_libdir}/ocaml/curses/*.cmxa
%{_libdir}/ocaml/curses/*.cmx
%endif