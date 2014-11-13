Name:           gpg2
Version:        2.0.26
Release:        0
License:        GPL-3.0+
Summary:        GnuPG 2
Url:            http://www.gnupg.org/aegypten2/
Group:          Security/Certificate Management
Source:         gnupg-%{version}.tar.bz2
Source1001:     gpg2.manifest
BuildRequires:  automake
BuildRequires:  expect
BuildRequires:  fdupes
BuildRequires:  gettext-tools
BuildRequires:  libadns-devel
BuildRequires:  libassuan-devel >= 2.0.0
BuildRequires:  libcurl-devel >= 7.10
BuildRequires:  libgcrypt-devel >= 1.4.0
BuildRequires:  libgpg-error-devel >= 1.7
BuildRequires:  libksba-devel >= 1.0.7
BuildRequires:  libpth-devel >= 1.3.7
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(zlib)
Provides:       gnupg = %{version}
Provides:       gpg = 1.4.9
Provides:       newpg
Provides:       gpg2_signd_support
Obsoletes:      gpg < 1.4.9

%description
GnuPG 2 is the successor of "GnuPG" or GPG. It provides: GPGSM,
gpg-agent, and a keybox library.

%prep
%setup  -q -n gnupg-%{version}
cp %{SOURCE1001} .

%build
%autogen
# build PIEs (position independent executables) for address space randomisation:
PIE="-fpie"
export CFLAGS="%{optflags} ${PIE}"
export LDFLAGS=-pie
%configure \
    --libexecdir=%{_libdir} \
    --docdir=%{_docdir}/%{name} \
    --with-agent-pgm=%{_bindir}/gpg-agent \
    --with-scdaemon-pgm=%{_bindir}/scdaemon \
    --enable-gpgsm=yes \
    --enable-gpg \
    --with-gnu-ld

%__make %{?_smp_mflags}

%check
%if ! 0%{?qemu_user_space_build}
%__make check
%{buildroot}%{_bindir}/gpgsplit -v -p pubsplit-                    --uncompress <tests/openpgp/pubring.gpg
%{buildroot}%{_bindir}/gpgsplit -v -p secsplit- --secret-to-public --uncompress <tests/openpgp/secring.gpg
%endif

%install
%make_install
mkdir -p %{buildroot}%{_sysconfdir}/gnupg/

install -m 644 doc/examples/gpgconf.conf %{buildroot}%{_sysconfdir}/gnupg

rm -rf %{buildroot}%{_datadir}/doc/packages/gpg2/examples/gpgconf.conf

ln -sf gpg2 %{buildroot}%{_bindir}/gpg
ln -sf gpgv2 %{buildroot}%{_bindir}/gpgv
ln -sf gpg2.1 %{buildroot}%{_mandir}/man1/gpg.1
ln -sf gpgv2.1 %{buildroot}%{_mandir}/man1/gpgv.1

rm -rf %{buildroot}/%{_datadir}/locale/en@{bold,}quot

%find_lang gnupg2

%fdupes %{buildroot}


%files -f gnupg2.lang
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING.LIB COPYING
%doc %{_infodir}/gnupg*
%doc %{_docdir}/%{name}
%{_mandir}/man*/*
%{_bindir}/*
%{_libdir}/[^d]*
%{_sbindir}/addgnupghome
%{_sbindir}/applygnupgdefaults
%{_datadir}/gnupg
%dir %{_sysconfdir}/gnupg
%config(noreplace) %{_sysconfdir}/gnupg/gpgconf.conf
