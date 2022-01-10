Summary: NethServer SOGo configuration
Name: nethserver-sogo
Version: 1.8.5
Release: 1%{?dist}
License: GPL
URL: %{url_prefix}/%{name} 
Source0: %{name}-%{version}.tar.gz
# Execute prep-sources to create Source1
Source1:        %{name}.tar.gz
BuildArch: noarch

# nethserver-base requires postfix MTA:
Requires: nethserver-mail-server >= 1.1.0-2
Requires: nethserver-mysql >= 1.0.0
Requires: nethserver-memcached >= 1.0.0
Requires: nethserver-httpd >= 1.0.1-2
Requires: nethserver-sssd
Requires: sogo >= 4.0.0
Requires: sogo-tool
Requires: sope49-gdl1-mysql
Requires: sogo-activesync
Requires: libwbxml
Requires: sogo-ealarms-notify

BuildRequires: perl
BuildRequires: nethserver-devtools 

%description
NethServer SOGo configuration

%prep
%setup

%build
%{makedocs}
perl createlinks
sed -i 's/_RELEASE_/%{version}/' %{name}.json

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})

mkdir -p %{buildroot}/usr/share/cockpit/%{name}/
mkdir -p %{buildroot}/usr/share/cockpit/nethserver/applications/
mkdir -p %{buildroot}/usr/libexec/nethserver/api/%{name}/

tar xvf %{SOURCE1} -C %{buildroot}/usr/share/cockpit/%{name}/

cp -a %{name}.json %{buildroot}/usr/share/cockpit/nethserver/applications/
cp -a api/* %{buildroot}/usr/libexec/nethserver/api/%{name}/
chmod +x %{buildroot}/usr/libexec/nethserver/api/%{name}/*

%{genfilelist} %{buildroot} \
  --file /usr/bin/sogo-restore-user 'attr(0750,root,root)'\
  --file /etc/sudoers.d/50_nsapi_nethserver_sogo 'attr(0440,root,root)' \
> %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist
echo "%doc README.rst" >> %{name}-%{version}-filelist

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%dir %{_nseventsdir}/%{name}-update

%changelog
* Mon Jan 10 2022 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.5-1
- SOGo: Available from public or trusted network - NethServer/dev#6617

* Tue Jul 07 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.4-1
- Merge pull request #46 from NethServer/revert-45-httpdConfRemoval
- Revert "Remove httpd template after rpm removal"

* Sun Jul 05 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.3-1
  - Merge pull request #45 from stephdl/httpdConfRemoval
  - Remove httpd template after rpm removal

* Sun Feb 09 2020 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.2-1
- Sogo: Logs with regex - NethServer/dev#6056

* Tue Dec 10 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.1-1
- SOGo: URL of webmail in the application cockpit list - NethServer/dev#5982

* Sun Dec 08 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.8.0-1
- SOGo Cockpit Application - NethServer/dev#5920

* Sat Nov 23 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.9-1
- SOGo: status props error in Nethgui - Bug NethServer/dev#5954

* Fri Nov 22 2019 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.8-1
- SOGo: groups do not appear - Bug NethServer/dev#5953
- SMTP sender/login validation - NethServer/dev#5672

* Wed Sep 12 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.7-1
- SOGo  cleanup prop/event and disable dav - NethServer/dev#5579

* Thu Sep 06 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.6-1
- Make a panel to SOGo - NethServer/dev#5575

* Sat Jul 07 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.5-1
- Redirect acme-challenge to https - NethServer/dev#5541

* Thu Jul 05 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.4-1
- With SOGo virtualhost , redirect / to /SOGo - NethServer/dev#5541

* Mon Jun 25 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.3-1
- SOGO: Enabled  startTLS if needed - Bug NethServer/dev#5533

* Wed May 16 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.2-1
- SOGO: Table 'sogo.sogo_folder_info' doesn't exist - NethServer/dev#5497

* Wed May 09 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.1-1
- Nethserver-sogo must subscribe nethserver-sssd-save - NethServer/dev#5486 

* Wed May 09 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.1-1
- Nethserver-sogo must subscribe nethserver-sssd-save - NethServer/dev#5486 !! INCOMPLETE

* Sun Mar 18 2018 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.7.0-1
- Mysql migration for sogo v4.0.0

* Fri Dec 08 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.18-1
- sogo-restore-tool script for restoration

* Fri Dec 08 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.17-1
- Enable the sogo backup
- Save the folder /var/lib/sogo/backups if nethserver-backup-data is installed
- the backup time can be adjusted by BackupTime '* *', two arguments
- '# * *' to disable

* Tue Dec 05 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.16-1
- revert the change in  ldap setting ( UIDFieldName )
 
* Tue Dec 05 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.15-1
- for isLdap, back to 'CNFieldName = cn' instead 'CNFieldName = displayName'
- when the field is modified all sieve filters are no more visible, but not lost
- The file sogo.sieve still exists

* Mon Nov 27 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.14-1
- set the good name@domain.com name in imap acl for openldap

* Thu Nov 23 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.13-1
- migrate IMAPLoginFieldName property to CustomEmailField
- display the full name in sogo
- set the good name@domain.com name in imap acl for sambaAD
 
* Sun Oct 15 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.12-1
- Added customization of IMAPLoginFieldName when sogo bind to a MICROSOFT AD 

* Sat Sep 09 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.11-1
- email alarm is now enabled

* Wed May 03 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.10-1
- sogo-ealarms-notify is removed of the cron job
- needed to enable SOGoEnableEMailAlarms and set OCSEMailAlarmsFolderURL 

* Fri Apr 28 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.9-1
- Increase maximum IMAP command line length
- Sogo session are dropped after 24h
- Adjusted sogo cron.d, sieve credentials are in /etc/sogo/sieve.creds

* Wed Mar 29 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.7-1
- Increase values to avoid battery drain when using active sync
- https://sogo.nu/files/docs/SOGoInstallationGuide.html#_microsoft_enterprise_activesync_tuning

* Sat Feb 25 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.5-1
- Corrected the right Incoming IP in log

* Sat Feb 18 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.4-1
- Increase the workers to 10
- Added SOGoMaximumSyncWindowSize to the default value 100

* Fri Feb 10 2017 Stephane de Labrusse <stephdl@de-labrusse.fr> - 1.6.3-1
- removed the mail definition of MailFieldNames for the AD settings

* Mon Jan 30 2017 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.2-1
- First release for NS 7.3

* Mon Oct 03 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.6.1-1
- Apache vhost-default template expansion - NethServer/dev#5088

* Thu Jul 07 2016 Stefano Fancello <stefano.fancello@nethesis.it> - 1.6.0-1
- First NS7 release

* Thu Feb 18 2016 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.6-1
- Upgrade to upstream release 2.3.8 - Enhancement #3343
- Support junkmail folder, thanks to markVnl

* Mon Oct 05 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.5-1
- SOGo: add option to enable/disable ActiveSync - Enhancement #3279 [NethServer]

* Mon Jun 15 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.4-1
- nethserver-sogo-2.1.17-to-2.3.0-update action returns 1 if executed when not needed - Bug #3196 [NethServer]

* Mon Jun 08 2015 Stefano Fancello <stefano.fancello@nethesis.it> - 1.5.3-1.ns6
- Upgrade SOGO to 2.3.0 - Feature #3186 [NethServer]

* Mon May 11 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.2-1
- SOGo: proxy-nokeepalive option breaks compatibility with other HTTP servers - Bug #3157 [NethServer]

* Thu Apr 23 2015 Davide Principi <davide.principi@nethesis.it> - 1.5.1-1
- SOGo ActiveSync doesn't work properly with much data - Bug #3123 [NethServer]
- SOGo doesn't show multiple addresses on sender field - Bug #3122 [NethServer]
- SOGo: sharing resources (contacts or calendar) doesn't works - Bug #3116 [NethServer]

* Tue Mar 10 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.5.0-1
- SOGo active sync support - Feature #3063 [NethServer]
- SOGo user's assets not deleted - Bug #2880 [NethServer]
- SOGo: ACLs deployed using groups does not work - Bug #2808 [NethServer]
- SOGo: hide Groups addressbook - Enhancement #2801 [NethServer]
- SOGo: suppress DROP USER error message - Enhancement #2779 [NethServer]
- SOGo data disappeared after packages update - Bug #2778 [NethServer]

* Thu Jun 12 2014 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.4.0-1.ns6
- Preserve request host name in SOGo - Enhancement #2759
- AD group mail delivery type switch - Feature #2751
- SOGo: shared folders not working for AD accounts - Bug #2730
- Use DNS A record to locate AD controllers - Enhancement #2729
- Configurable AD accounts LDAP subtree - Enhancement #2727
- SOGo: add dashboard widget - Enhancement #2710

* Wed Feb 05 2014 Davide Principi <davide.principi@nethesis.it> - 1.3.0-1.ns6
- Upgrade SOGo to release 2.1.1b - Enhancement #2457 [NethServer]
- Directory: backup service accounts passwords  - Enhancement #2063 [NethServer]

* Mon Dec 16 2013 Davide Principi <davide.principi@nethesis.it> - 1.2.2-1.ns6
- Redirect to internal DNS name - Bug #2371 [NethServer]
- Support iOS7 carddav client - Enhancement #2221 [NethServer]
- Remove apache "already loaded" warnings - Enhancement #2074 [NethServer]

* Tue Jun 11 2013 Davide Principi <davide.principi@nethesis.it> - 1.2.1-1.ns6
- Active Directory integration (experimental) #2000

* Mon Jun 10 2013 Davide Principi <davide.principi@nethesis.it> - 1.1.1-1.ns6
- Sogo mysql password unescaped: connection fails #2002

* Tue Apr 30 2013 Davide Principi <davide.principi@nethesis.it> - 1.1.0-1.ns6
- Full automatic package install/upgrade/uninstall support #1870 #1872 #1874
- Protect dovecot master user password #1825
- Expand /etc/cron.d/sogo template #1637
- Backup SOGo user folders #1800
- Added group LDAP source #1842
- Use submission port 587 to send messages #1817
- Fixed #1843 #1823

* Tue Mar 19 2013 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1.ns6
- createlinks: fixed wrong function name event_{actions => services}()  call. Refs #1637
- Moved httpd.conf template fragment to new location. Refs #1637
- Add migration code #1717
- Update URL spec tag #1654
- Set minimum version requirements  #1653

* Fri Feb  1 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.1-1.ns6
- Fix #1643

* Thu Jan 31 2013 Davide Principi <davide.principi@nethesis.it> - 1.0.0-1.ns6
- Initial release
