NethServer SOGo
===============

See [official documentation](https://nethserver.github.io/nethserver-cockpit/tutorial/)


In Short to build the rpm

  ./prep-sources
  make-rpms *.spec

`SOGo <http://www.sogo.nu/english/about/overview.html>`__ configuration
for NethServer.

    SOGo offers multiple ways to access the calendaring and messaging
    data. Your users can either use a web browser, Microsoft Outlook,
    Mozilla Thunderbird, Apple iCal, or a mobile device to access the
    same information.

.. contents:: :local:

Features
--------

-  ``mysql``, ``slapd``, ``sogod``, ``memcached`` configuration
-  apache2 configuration to access SOGo web interface at
   ``https://<hostname>/SOGo/``
-  daily cronjob to check *auto-reply* expiration
-  custom addressbooks in ``/var/lib/nethserver/db/sogo_sources``
   (undocumented)
-  extension for Thunderbird intergration (see [[sogo-frontends]])


Database Reference
------------------

Special properties:

* AdminUsers: Parameter used to set which usernames require
  administrative privileges over all the users tables.

* DraftsFolder: name of draft folder, default is ‘Drafts’

* SentFolder: name of the sent folder, default is ‘Sent’

* TrashFolder: name of the trash folder, default is ‘Trash’

* WOWorkersCount: The amount of instances of SOGo that will be spawned
  to handle multiple requests simultaneously

* MailAuxiliaryUserAccountsEnabled: Parameter used to activate the
  auxiliary IMAP accounts in SOGo. When set to YES, users can add
  other IMAP accounts that will be visible from the SOGo Webmail
  interface.
  
* Notifications: enabled notifications. The value is a comma separated
  list. Default value is “Appointment, EMail”

Configuration DB
~~~~~~~~~~~~~~~~

::

    sogod=service
        ...
        AdminUsers=admin
        DraftsFolder=Drafts
        Notifications=Appointment,ACLs
        SentFolder=Sent
        TrashFolder=Trash
        VirtualHosts=

    memcached=service
        ...

.. note:: *Italic* terms are documented in `SOGo installation and
	  configuration guide
	  <http://www.sogo.nu/english/support/documentation.html>`__

-  ``AdminUsers`` comma separated list of accounts allowed to bypass
   SOGo ACLs. See *SOGoSuperUsernames* key
-  ``Notifications`` comma separated list of values (no spaces between
   commas). Known item names are ``ACLs``, ``Folders``,
   ``Appointments``. See *SOGoSendEMailNotifications*
-  ``{Drafts,Sent,Trash}Folder`` See respective *SOGoFolderName*
   parameters
-  ``VirtualHosts`` comma separated list of host keys in ``hosts`` DB,
   with ``type=self``. SOGo is reachable from the default host name plus
   any host listed here (see #2371).

Inspect SOGo configuration
--------------------------

SOGo configuration is stored in an internal database (XML format) under
``/var/lib/sogo/GNUstep/`` directory. All database manipulations are
performed through ``/usr/bin/defaults`` command.

To dump the current configuration type:

::

      # su -s '/bin/bash' -c 'defaults read' sogo

To modify a value:

::

      # su -s '/bin/bash' -c 'defaults write sogod SxVMemLimit 512' - sogo

Increase ``sogod`` log verbosity
--------------------------------

For instance, to see LDAP queries add the following custom fragment:

::

    mkdir -p /etc/e-smith/templates-custom/sogo-config
    echo -n "{ \$S{LDAPDebugEnabled} = 'YES'; ''; }"  > /etc/e-smith/templates-custom/sogo-config/80logverbose
    signal-event nethserver-sogo-update

Read the `SOGo
FAQ <http://www.sogo.nu/nc/support/faq/article/how-to-enable-more-verbose-logging-in-sogo.html>`__
for other debugging features.

Access SOGo from the public network
-----------------------------------

To make SOGo accessible with a public DNS hostname:

* In “DNS and DHCP” UI module (Hosts), create the DNS host name as a
  server alias (i.e. ``public.example.com``)
* Add the host name to ``sogod/VirtualHosts`` prop list:

::

     # config setprop sogod VirtualHosts public.example.com
     # signal-event nethserver-sogo-update

Same rule applies if SOGo must be accessible using server IP address.
For example:

::

    # config setprop sogod VirtualHosts 192.168.1.1
    # signal-event nethserver-sogo-update

Active Directory integration
----------------------------

[This section is extracted from issue #2000]

#. [[nethserver-samba\|Join]] an Active Directory domain
#. In AD, create a user (ie ``sogoad``) under ``CN=Users`` container,
   with a non-expiring password (ie ``PASSWORD``). This is needed by
   SOGo to browse AD LDAP. Choose a password that does not contain the
   percent ``%`` symbol.
#. Save ``sogoad`` credentials in configuration DB: ::
     
    # config setprop sogod AdsCredentials ‘sogoad%PASSWORD’
    # signal-event nethserver-sogo-update


To disable SOGo AD integration

::

       # config setprop sogod AdsCredentials ''
       # signal-event nethserver-sogo-update

**WARNING**

In ADS mode SOGo uses simple LDAP binds on Active Directory LDAP, that
means users’ **passwords are sent in clear text** over the network.

If you have `LDAP SSL
enabled <http://support.microsoft.com/kb/321051>`__ or you know how to
set up a persistent encrypted tunnel, the ``AdsLdapServer`` prop can
help:

::

       # config setprop sogod AdsLdapServer PROTO://DOMAIN:PORTNUMBER
       # signal-event nethserver-sogo-update

Where

* **PROTO://** can be ``ldap://`` or ``ldaps://`` (optional)
* **DOMAIN** should be the lowercased realm
* **PORTNUMBER** default 389 (optional)

Also STARTTLS should be supported. Refer to the SOGo documentation about
``hostname`` parameter.

YUM issues
----------

SOGo comes with a recompiled version of GNUStep packages that may
conflict with EPEL versions. From `SOGo install
FAQ <http://www.sogo.nu/english/support/faq/article/how-to-install-sogo-and-sope-through-yum.html>`__:

add the following line to the EPEL repo definition: ::

  [epel]
  …
  exclude=gnustep-\*

However, ``gnustep-make`` and ``gnustep-base`` packages should be rarely
installed on a server system.

.. |image0| image:: {width: 500px}/attachments/download/171/sogo.svg


Download and publish new rpms
-----------------------------

* Configure SOGo repo `/etc/yum.repos.d/sogo.repo`: ::

  [sogo3-rhel7]
  name=Inverse SOGo Repository
  baseurl=http://inverse.ca/rhel-v3/7/$basearch
  gpgcheck=0

* Download latest release: ::

  yum --enablerepo=nethserver-testing --downloadonly --downloaddir=sogo install sogo --disablerepo=epel,nethserver*

* Remove all packages downloaded from non-sogo repos. This should be enough: ::

  rm -f libevent* libmemcached* libobjc* memcached* zip*

* Upload the rpms to NethForge: ::

  upload-rpms packages.nethserver.org:nscom/7.2.1511/nethforge *rpm
