Name: @PACKAGE@
Summary: Bruce's Cron System
Version: @VERSION@
Release: 1
Copyright: GPL
Group: Utilities/System
Source: http://untroubled.org/@PACKAGE@/@PACKAGE@-@VERSION@.tar.gz
BuildRoot: %{_tmppath}/@PACKAGE@-buildroot
URL: http://untroubled.org/@PACKAGE@/
Packager: Bruce Guenter <bruceg@em.ca>
BuildRequires: bglibs >= 1.018

%description
Bruce's Cron System

%prep
%setup
echo gcc "%{optflags}" >conf-cc
echo gcc -s >conf-ld

%build
make programs

%install
rm -fr %{buildroot}
rm -f conf_bin.c insthier.o installer instcheck
echo %{buildroot}%{_bindir} >conf-bin
make installer instcheck

mkdir -p %{buildroot}%{_bindir}
./installer
./instcheck

mkdir -p %{buildroot}%{_mandir}/man{1,8}
cp bcron-{exec,sched,spool,start,update}.8 %{buildroot}%{_mandir}/man8
cp bcrontab.1 %{buildroot}%{_mandir}/man1

mkdir -p %{buildroot}/var/service/bcron-{sched/log,spool,update}
cp bcron-sched.run %{buildroot}/var/service/bcron-sched/run
cp bcron-sched-log.run %{buildroot}/var/service/bcron-sched/log/run
cp bcron-spool.run %{buildroot}/var/service/bcron-spool/run
cp bcron-update.run %{buildroot}/var/service/bcron-update/run
chmod +t %{buildroot}/var/service/bcron-sched

mkdir -p %{buildroot}/var/log/bcron

mkdir -p %{buildroot}/var/spool/cron/{crontabs,tmp}
mkfifo %{buildroot}/var/spool/cron/trigger

mkdir -p %{buildroot}/etc/cron.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ANNOUNCEMENT COPYING NEWS README # bcron.texi *.html
%dir /etc/cron.d
%{_bindir}/*
%{_mandir}/*/*

/var/service/*

%attr(700,cron,cron) %dir /var/spool/cron
%attr(700,cron,cron) %dir /var/spool/cron/crontabs
%attr(700,cron,cron) %dir /var/spool/cron/tmp
%attr(600,cron,cron)      /var/spool/cron/trigger

%attr(700,root,root) %dir /var/log/bcron