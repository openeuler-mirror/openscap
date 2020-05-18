Name:                      openscap
Version:                   1.3.2
Release:                   6
Summary:                   An open source framework in order to provide a interface for using scap
License:                   LGPLv2+
URL:                       http://www.open-scap.org
Source0:                   https://github.com/OpenSCAP/openscap/archive/%{version}.tar.gz
Patch9000:                 Fix-scap_workbench-builderror.patch
BuildRequires:             cmake >= 2.6 gcc gcc-c++ swig libxml2-devel libxslt-devel perl-generators perl-XML-Parser
BuildRequires:             rpm-devel libgcrypt-devel pcre-devel libacl-devel libselinux-devel libcap-devel libblkid-devel
BuildRequires:             bzip2-devel asciidoc openldap-devel GConf2-devel dbus-devel chrpath libcurl-devel >= 7.12.0

%if %{?_with_check:1}%{!?_with_check:0}
BuildRequires:             perl-XML-XPath bzip2
%endif

Requires:                  libcurl >= 7.12.0 rpmdevtools rpm-build

Provides:                  %{name}-scanner = %{version}-%{release} %{name}-utils = %{version}-%{release}
Provides:                  %{name}-engine-sce = %{version}-%{release} %{name}-containers = %{version}-%{release}

Obsoletes:                 python2-openscap < %{version}-%{release} openscap-content-sectool < %{version}-%{release} openscap-extra-probes < %{version}-%{release}
Obsoletes:                 openscap-selinux < %{version}-%{release} openscap-selinux-compat < %{version}-%{release} openscap-extra-probes-sql < %{version}-%{release}
Obsoletes:                 %{name}-containers < %{version}-%{release} %{name}-utils < %{version}-%{release}
Obsoletes:                 %{name}-engine-sce < %{version}-%{release} %{name}-scanner < %{version}-%{release}

%description
Openscap is an open source framework that integrates secure content automation protocols. Its goal is to provide a simple
and easy to use interface for using scap.

%package                   devel
Summary:                   Header files and libraries for development
Requires:                  %{name} = %{version}-%{release} pkgconfig libxml2-devel
BuildRequires:             doxygen

Provides:                  %{name}-engine-sce-devel = %{version}-%{release}
Obsoletes:                 %{name}-engine-sce-devel < %{version}-%{release}

%description               devel
The openscap-devel package contains the static libraries, the header files and other development content.

%package                   python3
Summary:                   Python 3 bindings for openscap
Requires:                  %{name} = %{version}-%{release}
BuildRequires:             python3-devel

%description               python3
This package contains the bindings, python3 can use openscap libraries through this package.

%package                   perl
Summary:                   Perl bindings for openscap
Requires:                  %{name} = %{version}-%{release} perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildRequires:             perl-devel

%description               perl
This package contains the bindings, perl can use openscap libraries through this package.

%package                   help
Summary:                   Help documentation related to openscap
Requires:                  %{name} = %{version}-%{release}
BuildArch:                 noarch

%description               help
This package includes help documentation and manuals related to openscap.

%prep
%autosetup -n %{name}-%{version} -p1
mkdir -p build

%build
cd build
%cmake -DENABLE_DOCS=ON ..
%make_build
make docs

%check
%if %{?_with_check:1}%{!?_with_check:0}
ctest -V %{?_smp_mflags}
%endif

%install
cd build
%make_install

%delete_la

pathfix.py -i %{__python3} -p -n $RPM_BUILD_ROOT%{_bindir}/scap-as-rpm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING

%{_bindir}/*

%{_libdir}/libopenscap.so.*
%{_libdir}/libopenscap_sce.so.*
%{_datadir}/openscap/schemas/*
%{_datadir}/openscap/xsl/*
%{_datadir}/openscap/cpe/*

%{_sysconfdir}/bash_completion.d

%files devel
%{_libdir}/libopenscap.so
%{_libdir}/libopenscap_sce.so
%{_libdir}/pkgconfig/*.pc

%{_includedir}/openscap

%files python3
%{python3_sitearch}/*
%{python3_sitelib}/oscap_docker_python/*

%files perl
%{perl_vendorarch}/*
%{perl_vendorlib}/*

%files help
%doc AUTHORS NEWS README.md docs/oscap-scan.cron
%{_pkgdocdir}/manual/*
%{_pkgdocdir}/html/*
%{_mandir}/man8/*

%changelog
* Mon May 18 2020 wangchen <wangchen137@huawei.com> 1.3.2-6
- rebuild for openscap

* Wed Mar 11 2020 Senlin Xia <xiasenlin1@huawei.com> 1.3.2-5
- Fix scap-workbench compilation failure: declaration of 'operator' as parameter in oval_definitions.h

* Sat Feb 29 2020 lihao <lihao129@huawei.com> - 1.3.2-4
- Fix incompatible with rpm-devel-4.15

* Wed Oct 16 2019 dongjian <dongjian13@huawei.com> - 1.3.0_alpha2-3
- Package init
