#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml bindings for ncurses
Summary(pl.UTF-8):	Wiązania OCamla do ncurses
Name:		ocaml-curses
Version:	1.0.3
Release:	13
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://download.savannah.gnu.org/releases/ocaml-tmk/%{name}-%{version}.tar.gz
# Source0-md5:	3c11b46b7c057f8fd110ace319589877
URL:		http://savannah.nongnu.org/projects/ocaml-tmk/
BuildRequires:	autoconf >= 2.50
BuildRequires:	gawk
BuildRequires:	ncurses-devel >= 5
BuildRequires:	ocaml >= 1:3.10.2
BuildRequires:	ocaml-findlib >= 1.3.3-3
ExcludeArch:	sparc64 s390 s390x
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCaml bindings for ncurses.

%description -l pl.UTF-8
Wiązania OCamla do ncurses.

%package devel
Summary:	Development files for OCaml curses library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki OCamla curses
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains libraries and signature files for developing
applications that use OCaml curses library.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki sygnatur do tworzenia aplikacji
z użyciem biblioteki OCamla curses.

%prep
%setup -q

%build
%{__autoconf}
%{__autoheader}
%configure \
	--enable-widec

%{__make} -j1 all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/curses,stublibs}

%{__make} install \
	OCAMLFIND_INSTFLAGS="-destdir $RPM_BUILD_ROOT%{_libdir}/ocaml"

%if %{with ocaml_opt}
# *.cmx missing from make install
cp -p *.cmx $RPM_BUILD_ROOT%{_libdir}/ocaml/curses
%endif

%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/{,site-lib/}curses/META
cat <<EOF >>$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/curses/META
directory="+curses"
EOF

%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/*.so.owner

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/curses
%{_libdir}/ocaml/curses/*.cmi
%{_libdir}/ocaml/curses/curses.cma
%dir %{_libdir}/ocaml/stublibs
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllcurses_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/curses/curses.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/curses/*.cmx
%{_libdir}/ocaml/curses/curses.a
%{_libdir}/ocaml/curses/curses.cmxa
%{_libdir}/ocaml/curses/libcurses_stubs.a
%endif
%{_libdir}/ocaml/site-lib/curses
