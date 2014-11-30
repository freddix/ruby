%bcond_with	bootstrap

%define		ruby_ver	2.1.0

Summary:	Ruby - interpreted scripting language
Name:		ruby
Version:	2.1.5
Release:	1
License:	The Ruby License
Group:		Development/Languages
Source0:	http://cache.ruby-lang.org/pub/ruby/2.1/%{name}-%{version}.tar.xz
# Source0-md5:	8a30ed4b022a24acbb461976c9c70789
Source1:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{name}-1.8.7-p358.tar.gz
# Source1-md5:	26bd55358847459a7752acdbd33a535f
Patch0:		%{name}-r5108.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
#BuildRequires:	doxygen
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel
%{!?with_bootstrap:BuildRequires:	ruby}
BuildRequires:	sed
#BuildRequires:	tk-devel
BuildRequires:	unzip
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Provides:	ruby(ver) = %{ruby_ver}
Provides:	ruby-modules(ver) = %{ruby_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/ruby

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

%package libs
Summary:	Ruby libraries
Group:		Libraries

%description libs
Ruby libraries.

%package tk
Summary:	Ruby/Tk bindings
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description tk
This pachage contains Ruby/Tk bindings.

%package devel
Summary:	Ruby development libraries
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Ruby development libraries.

%prep
%setup -q -a1

find -type f \( -name '*.rb' -o -name '*.cgi' -o -name '*.test' -o -name 'ruby.1' \
	-o -name 'ruby.info*' -o -name '*.html' -o -name '*.tcl' -o -name '*.texi' \) \
	| xargs %{__sed} -i 's,/usr/local/bin/,%{_bindir}/,'

%if %{with bootstrap}
cd %{name}-1.8.7-p358
%patch0 -p1
%endif

%build
cp -f /usr/share/automake/config.sub .

%if %{with bootstrap}
cd %{name}-1.8.7-p358
%configure
%{__make}
cd ..
%endif

%{__autoconf}
%configure \
	--disable-install-doc	\
	--enable-pthread	\
	--enable-shared		\
	--with-dbm-type=gdbm_compat \
	%{?with_bootstrap:--with-baseruby=%{name}-1.8.7-p358/miniruby}

%{__make} -j1 %{?with_bootstrap:BASERUBY="ruby-1.8.7-p358/miniruby -I./ruby-1.8.7-p358/lib"}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-nodoc \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/gems/%{ruby_ver}/gems
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/*.a

%check
%{__make} test

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.EXT ChangeLog
%attr(755,root,root) %{_bindir}/erb
%attr(755,root,root) %{_bindir}/gem
%attr(755,root,root) %{_bindir}/irb
%attr(755,root,root) %{_bindir}/rake
%attr(755,root,root) %{_bindir}/rdoc
%attr(755,root,root) %{_bindir}/ri
%attr(755,root,root) %{_bindir}/ruby
%attr(755,root,root) %{_bindir}/testrb

%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{ruby_ver}
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/dl
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/trans
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json/ext
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/mathn
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/rbconfig

%dir %{_libdir}/%{name}/site_ruby
%dir %{_libdir}/%{name}/site_ruby/%{ruby_ver}
%dir %{_libdir}/%{name}/site_ruby/%{ruby_ver}/*-linux*
%dir %{_libdir}/%{name}/vendor_ruby
%dir %{_libdir}/%{name}/vendor_ruby/%{ruby_ver}
%dir %{_libdir}/%{name}/vendor_ruby/%{ruby_ver}/*-linux*

%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[a-t]*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[u-z]*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/dl/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/trans/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json/ext/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/mathn/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/rbconfig/sizeof.so

%dir %{_libdir}/%{name}/gems
%dir %{_libdir}/%{name}/gems/%{ruby_ver}
%dir %{_libdir}/%{name}/gems/%{ruby_ver}/specifications
%dir %{_libdir}/%{name}/gems/%{ruby_ver}/specifications/default
%{_libdir}/%{name}/gems/%{ruby_ver}/specifications/default/*.gemspec

%{_libdir}/%{name}/%{ruby_ver}/*-linux*/rbconfig.rb
%{_libdir}/%{name}/%{ruby_ver}/*.rb
%{_libdir}/%{name}/%{ruby_ver}/bigdecimal
%{_libdir}/%{name}/%{ruby_ver}/cgi
%{_libdir}/%{name}/%{ruby_ver}/date
%{_libdir}/%{name}/%{ruby_ver}/digest
%{_libdir}/%{name}/%{ruby_ver}/dl
%{_libdir}/%{name}/%{ruby_ver}/drb
%{_libdir}/%{name}/%{ruby_ver}/fiddle
%{_libdir}/%{name}/%{ruby_ver}/io
%{_libdir}/%{name}/%{ruby_ver}/irb
%{_libdir}/%{name}/%{ruby_ver}/json
%{_libdir}/%{name}/%{ruby_ver}/matrix
%{_libdir}/%{name}/%{ruby_ver}/minitest
%{_libdir}/%{name}/%{ruby_ver}/net
%{_libdir}/%{name}/%{ruby_ver}/openssl
%{_libdir}/%{name}/%{ruby_ver}/optparse
%{_libdir}/%{name}/%{ruby_ver}/psych
%{_libdir}/%{name}/%{ruby_ver}/racc
%{_libdir}/%{name}/%{ruby_ver}/rake
%{_libdir}/%{name}/%{ruby_ver}/rbconfig
%{_libdir}/%{name}/%{ruby_ver}/rdoc
%{_libdir}/%{name}/%{ruby_ver}/rexml
%{_libdir}/%{name}/%{ruby_ver}/rinda
%{_libdir}/%{name}/%{ruby_ver}/ripper
%{_libdir}/%{name}/%{ruby_ver}/rss
%{_libdir}/%{name}/%{ruby_ver}/rubygems
%{_libdir}/%{name}/%{ruby_ver}/shell
%{_libdir}/%{name}/%{ruby_ver}/syslog
%{_libdir}/%{name}/%{ruby_ver}/test
%{_libdir}/%{name}/%{ruby_ver}/uri
%{_libdir}/%{name}/%{ruby_ver}/webrick
%{_libdir}/%{name}/%{ruby_ver}/xmlrpc
%{_libdir}/%{name}/%{ruby_ver}/yaml

%{_mandir}/man1/erb.1*
%{_mandir}/man1/irb.1*
%{_mandir}/man1/rake.1*
%{_mandir}/man1/ri.1*
%{_mandir}/man1/ruby.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libruby.so.?.?
%attr(755,root,root) %{_libdir}/libruby.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby.so
%{_includedir}/%{name}-%{ruby_ver}
%{_pkgconfigdir}/*.pc

%if 0
%files tk
%defattr(644,root,root,755)
%{_libdir}/%{name}/%{ruby_ver}/tcltk.rb
%{_libdir}/%{name}/%{ruby_ver}/tk*.rb
%{_libdir}/%{name}/%{ruby_ver}/tk
%{_libdir}/%{name}/%{ruby_ver}/tkextlib
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/t*.so
%endif

