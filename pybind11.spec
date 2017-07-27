# While the headers are architecture independent, the package must be
# built separately on all architectures so that the tests are run
# properly. See also
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
%global debug_package %{nil}

Name:    pybind11		
Version: 2.0.1
Release: 6%{?dist}
Summary: Seamless operability between C++11 and Python
License: BSD	
URL:	 https://github.com/pybind/pybind11	
Source0: https://github.com/pybind/pybind11/archive/v%{version}.tar.gz

# Disable numpy dtypes test as guided in https://github.com/pybind/pybind11/issues/694
Patch0:  pybind11-2.0.1-tests.patch
# Fix tests that are broken on bigendian systems, adapted from https://github.com/pybind/pybind11/pull/699
Patch1:  pybind11-2.0.1-byteorder.patch

# These are only needed for the checks
BuildRequires: python2-devel
BuildRequires: python2-pytest
BuildRequires: python2-numpy
BuildRequires: python2-scipy
BuildRequires: python3-devel
BuildRequires: python3-pytest
BuildRequires: python3-numpy
BuildRequires: python3-scipy
BuildRequires: eigen3-devel
BuildRequires: gcc-c++
BuildRequires: cmake

%description
pybind11 is a lightweight header-only library that exposes C++ types
in Python and vice versa, mainly to create Python bindings of existing
C++ code.

%package devel
Summary:  Development headers for pybind11
# https://fedoraproject.org/wiki/Packaging:Guidelines#Packaging_Header_Only_Libraries
Provides: %{name}-static = %{version}-%{release}
# For dir ownership
Requires: cmake

%description devel
pybind11 is a lightweight header-only library that exposes C++ types
in Python and vice versa, mainly to create Python bindings of existing
C++ code.

This package contains the development headers for pybind11.

%prep
%setup -q
%patch0 -p1 -b .tests
%patch1 -p1 -b .order

%build
for py in python2 python3; do
mkdir $py
cd $py
%cmake .. -DCMAKE_BUILD_TYPE=Release -DPYTHON_EXECUTABLE=/usr/bin/$py
make %{?_smp_mflags}
cd ..
done

%check
make -C python2 check %{?_smp_mflags}
make -C python3 check %{?_smp_mflags}

%install
%make_install -C python2

%files devel
%license LICENSE
%doc README.md
%{_includedir}/pybind11/
%{_datadir}/cmake/pybind11/


%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 27 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-5
- Full compliance with header only libraries guidelines.

* Thu Feb 23 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-4
- As advised by upstream, disable dtypes test for now.
- Include patch for tests on bigendian systems.

* Thu Feb 23 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-3
- Make the package arched so that tests can be run on all architectures.
- Run tests both against python2 and python3.

* Wed Feb 22 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-2
- Switch to python3 for tests.

* Sun Feb 05 2017 Susi Lehtola <jussilehtola@fedorapeople.org> - 2.0.1-1
- First release.
