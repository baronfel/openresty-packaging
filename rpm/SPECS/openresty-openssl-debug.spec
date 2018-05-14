Name:               openresty-openssl-debug
Version:            1.1.0h
Release:            1%{?dist}
Summary:            Debug version of the OpenSSL library for OpenResty

Group:              Development/Libraries

# https://www.openssl.org/source/license.html
License:            OpenSSL
URL:                https://www.openssl.org/
Source0:            https://www.openssl.org/source/openssl-%{version}.tar.gz

Patch0:             https://raw.githubusercontent.com/openresty/openresty/master/patches/openssl-1.1.0d-sess_set_get_cb_yield.patch

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:      gcc, make, perl

BuildRequires:      openresty-zlib-devel >= 1.2.11
Requires:           openresty-zlib >= 1.2.11

AutoReqProv:        no

%define openssl_prefix      %{_usr}/local/openresty-debug/openssl
%define zlib_prefix         /usr/local/openresty/zlib
%global _default_patch_fuzz 1


%description
This is the debug version of the OpenSSL library build for OpenResty uses.


%package devel

Summary:            Debug version of development files for OpenResty's OpenSSL library
Group:              Development/Libraries
Requires:           openresty-openssl-debug

%description devel
Provides C header and static library for the debug version of OpenResty's OpenSSL library. This is the debug version.

%prep
%setup -q -n openssl-%{version}

%patch0 -p1


%build
./config \
    no-threads no-asm \
    enable-ssl3 enable-ssl3-method \
    shared zlib -g -O0 -DPURIFY \
    --prefix=%{openssl_prefix} \
    --libdir=lib \
    -I%{zlib_prefix}/include \
    -L%{zlib_prefix}/lib \
    -Wl,-rpath,%{zlib_prefix}/lib:%{openssl_prefix}/lib

sed -i 's/ -O3 / -O0 /g' Makefile

make %{?_smp_mflags}


%install
make install_sw DESTDIR=%{buildroot}

chmod +w %{buildroot}%{openssl_prefix}/lib/*.so
chmod +w %{buildroot}%{openssl_prefix}/lib/*/*.so

rm -rf %{buildroot}%{openssl_prefix}/bin/c_rehash
rm -rf %{buildroot}%{openssl_prefix}/lib/pkgconfig
rm -rf %{buildroot}%{openssl_prefix}/misc

# to silence the check-rpath error
export QA_RPATHS=$[ 0x0002 ]


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)

%attr(0755,root,root) %{openssl_prefix}/bin/openssl
%attr(0755,root,root) %{openssl_prefix}/lib/*.so*
%attr(0755,root,root) %{openssl_prefix}/lib/*/*.so*
%attr(0644,root,root) %{openssl_prefix}/openssl.cnf


%files devel
%defattr(-,root,root,-)

%{openssl_prefix}/include/*
%attr(0755,root,root) %{openssl_prefix}/lib/*.a


%changelog
* Mon May 14 2018 Yichun Zhang (agentzh) 1.1.0h-1
- upgraded openresty-openssl to 1.1.0h.
* Thu Apr 19 2018  Yichun Zhang (agentzh) 1.0.2n-1
- upgraded openssl to 1.0.2n.
* Sun May 21 2017 Yichun Zhang (agentzh) 1.0.2k-2
- avoided the electric fence dependency.
* Sun Mar 19 2017 Yichun Zhang (agentzh)
- upgraded OpenSSL to 1.0.2k.
* Fri Nov 25 2016 Yichun Zhang (agentzh)
- added perl to the BuildRequires list.
* Tue Oct  4 2016 Yichun Zhang (agentzh)
- fixed the rpath of libssl.so (we should have linked against
our own libcrypto.so).
* Sat Sep 24 2016 Yichun Zhang (agentzh)
- upgrade to OpenSSL 1.0.2i.
* Tue Aug 23 2016 zxcvbn4038
- use openresty-zlib instead of the system one.
* Wed Jul 13 2016 makerpm
- initial build for OpenSSL 1.0.2h.
