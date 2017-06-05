#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml bindings for ncurses
Name:		ocaml-curses
Version:	1.0.3
Release:	12
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

%{__make} -j1 all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
ocamlfind install curses META *.cmi *.cma %{?with_ocaml_opt:*.cmx *.cmxa *.a} *.so *.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/ocaml/site-lib/curses
%exclude %{_libdir}/ocaml/site-lib/curses/*.mli
%if %{with ocaml_opt}
%exclude %{_libdir}/ocaml/site-lib/curses/*.a
%exclude %{_libdir}/ocaml/site-lib/curses/*.cmxa
%exclude %{_libdir}/ocaml/site-lib/curses/*.cmx
%endif
# XXX: proper packaging this would be?
%dir %{_libdir}/ocaml/site-lib/stublibs
%attr(755,root,root) %{_libdir}/ocaml/site-lib/stublibs/*.so
%{_libdir}/ocaml/site-lib/stublibs/*.so.owner

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/site-lib/curses/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/site-lib/curses/*.a
%{_libdir}/ocaml/site-lib/curses/*.cmxa
%{_libdir}/ocaml/site-lib/curses/*.cmx
%endif
