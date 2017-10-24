%global gem_name excon
%global need_bootstrap 1

Summary: Http(s) EXtended CONnections
Name: rubygem-%{gem_name}
Version: 0.58.0
Release: 1%{?dist}
Group: Development/Languages
License: MIT
URL: https://github.com/excon/excon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: ruby(rubygems)
Requires: ca-certificates
BuildRequires: rubygems-devel
BuildRequires: ca-certificates
%if 0%{?need_bootstrap} < 1
# For the tests
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(delorean)
BuildRequires: rubygem(open4)
BuildRequires: rubygem(shindo)
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(eventmachine)
%endif
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
EXtended http(s) CONnections

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec

%gem_install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* %{buildroot}%{gem_dir}/

# kill bundled cacert.pem
ln -sf %{_sysconfdir}/pki/tls/cert.pem \
       %{buildroot}%{gem_instdir}/data/cacert.pem

%check
%if 0%{?need_bootstrap} < 1
pushd .%{gem_instdir}
# Don't use Bundler.
sed -i "/'bundler\/setup'/ s/^/#/" tests/test_helper.rb

# Unicorn is not available in Fedora yet (rhbz#1065685).
sed -i '/with_unicorn/ s/^/  pending\n\n/' tests/basic_tests.rb

shindo
popd
%endif

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%{gem_instdir}/benchmarks
%{gem_instdir}/data
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUTING.md
%doc %{gem_instdir}/CONTRIBUTORS.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Gemfile.lock
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/changelog.txt
%{gem_instdir}/excon.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tests

%changelog
* Thu Aug 17 2017 Richard Megginson <rmeggins@localhost.localdomain> - 0.58.0-1
- Update to excon 0.58.0

* Thu Jun 29 2017 Rich Megginson <rmeggins@redhat.com> - 0.57.0-1
- Update to excon 0.57.0

* Tue Oct 18 2016 Rich Megginson <rmeggins@redhat.com> - 0.54.0-1
- Update to excon 0.54.0

* Wed Sep 28 2016 Rich Megginson <rmeggins@redhat.com> - 0.53.0-1
- Update to excon 0.53.0

* Fri Sep 16 2016 Rich Megginson <rmeggins@redhat.com> - 0.52.0-1
- Update to excon 0.52.0

* Fri Dec 19 2014 Troy Dawson <tdawson@redhat.com> - 0.8.0-9
- Update spec to work in EPEL7

* Mon Sep 29 2014 Brett Lentz <blentz@redhat.com> - 0.39.6-1
- Update to excon 0.39.6.

* Wed Jul 30 2014 Brett Lentz <blentz@redhat.com> - 0.38.0-1
- Update to excon 0.38.0.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Vít Ondruch <vondruch@redhat.com> - 0.33.0-1
- Update to excon 0.33.0.

* Wed Oct 09 2013 Josef Stribny <jstribny@redhat.com> - 0.25.3-1
- Update to excon 0.25.3.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Vít Ondruch <vondruch@redhat.com> - 0.21.0-1
- Update to excon 0.21.0.

* Fri Mar 08 2013 Vít Ondruch <vondruch@redhat.com> - 0.16.7-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.16.7-1
- Update to Excon 0.16.7.

* Mon Jul 23 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.3-1
- Update to Excon 0.14.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.14.1-1
- Update to Excon 0.14.1
- Removed no longer needed patch for downgrading dependencies.
- Remove newly bundled certificates and link to system ones.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.5-2
- Fixed the changelog.

* Wed Feb 01 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.5-1
- Update to version 0.9.5
- Fixed the dependencies for the new version.

* Mon Dec 05 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.12-1
- Update to version 0.7.12.

* Mon Nov 28 2011 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.8-1
- Update to version 0.7.8.
- Replaced defines with more appropriate globals.
- Added Build dependency on rubygem-eventmachine.
- Fixed running tests for the new version.

* Wed Oct 12 2011 bkabrda <bkabrda@redhat.com> - 0.7.6-1
- Update to version 0.7.6
- Introduced doc subpackage
- Introduced check section

* Tue Jul 05 2011 Chris Lalancette <clalance@redhat.com> - 0.6.3-1
- Initial package
