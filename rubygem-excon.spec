%global gem_name excon

# This will enable test on the future
# and also added it depdendencies
%global with_test 0

Name: rubygem-%{gem_name}
Version: 0.54.0
Release: 4%{?dist}
Summary: Usable, fast, simple HTTP 1.1 for Ruby
Group: Development/Languages
License: MIT
URL: https://github.com/excon/excon
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# Update expired certificates.
# https://github.com/excon/excon/commit/6a6a30ac9e68ea54f7fd4774bf304074bfd4e505
Patch0: excon-0.54.0-update-self-signed-certs-to-fix-tests.patch
BuildRequires: ruby(release)
BuildRequires: rubygems-devel
BuildRequires: ruby
%if 0%{?with_test}
BuildRequires: %{_bindir}/rackup
BuildRequires: %{_bindir}/shindo
BuildRequires: rubygem(activesupport)
BuildRequires: rubygem(delorean)
BuildRequires: rubygem(eventmachine)
BuildRequires: rubygem(open4)
BuildRequires: rubygem(puma)
BuildRequires: rubygem(sinatra)
BuildRequires: rubygem(rspec)
%endif
BuildArch: noarch

%if 0%{?rhel} > 0
Provides: rubygem(%{gem_name}) = %{version}
%endif

%description
Usable, fast, simple Ruby HTTP 1.1
Excon was designed to be simple, fast and performant. It works great as a general HTTP(s) client and is particularly well suited to usage in API clients.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%setup -q -c -T
%gem_install -n %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
sed -i -e 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/g' ./tests/servers/eof.rb
sed -i -e 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/g' ./tests/servers/good.rb
sed -i -e 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/g' ./tests/servers/error.rb
sed -i -e 's/\/usr\/bin\/env ruby/\/usr\/bin\/ruby/g' ./tests/servers/bad.rb

popd

# Use system crypto policies.
# https://fedoraproject.org/wiki/Packaging:CryptoPolicies
sed -i "/ciphers/ s/'.*'/'PROFILE=SYSTEM'/" .%{gem_libdir}/excon/constants.rb
%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

# Kill bundled cacert.pem
rm -rf %{buildroot}%{gem_instdir}/data

%check
pushd .%{gem_instdir}
%if 0%{?with_test}
# Unicorn is not available in Fedora yet (rhbz#1065685).
sed -i '/if plugin == :unicorn/ i\  before { skip("until #{plugin} is in Fedora") } if plugin == :unicorn' spec/support/shared_contexts/test_server_context.rb
sed -i '/with_unicorn/ s/^/  pending\n\n/' tests/{basic_tests.rb,proxy_tests.rb}

# spec_helper is not required on all places.
# https://github.com/excon/excon/pull/610
# time must be required for some tests.
# https://github.com/excon/excon/pull/611
rspec -rspec_helper -rtime spec

# Don't use Bundler.
sed -i "/'bundler\/setup'/ s/^/#/" tests/test_helper.rb

# This would require Sinatra 2.x+ or sinatra-contrib.
 sed -i '/redirecting_with_cookie.ru/,/^  end/ s/^/#/' tests/middlewares/capture_cookies_tests.rb
%endif
#shindo
popd

%files
%dir %{gem_instdir}
%license %{gem_instdir}/LICENSE.md
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/CONTRIBUT*
%{gem_instdir}/Gemfile*
%doc %{gem_instdir}/README.md
%{gem_instdir}/Rakefile
%{gem_instdir}/benchmarks
%doc %{gem_instdir}/changelog.txt
%{gem_instdir}/excon.gemspec
%{gem_instdir}/spec
%{gem_instdir}/tests

%changelog
* Mon Oct 23 2017 Juan Badia Payno <jbadiapa@redhat.com> - 0.54.0-4
- Imported to CentOS

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Vít Ondruch <vondruch@redhat.com> - 0.54.0-1
- Update to excon 0.54.0.

* Thu Sep 08 2016 Vít Ondruch <vondruch@redhat.com> - 0.52.0-1
- Update to excon 0.52.0.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.45.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 21 2015 Vít Ondruch <vondruch@redhat.com> - 0.45.4-1
- Update to excon 0.45.4.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.45.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Vít Ondruch <vondruch@redhat.com> - 0.45.1-1
- Update to excon 0.45.1.

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
