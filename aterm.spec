Summary:	aterm - terminal emulator in an X window
Name:		aterm
Version:	0.3.6
Release:	1
Copyright:	GPL
Group:		X11/Utilities
Vendor:		Sasha Vasko <sashav@sprintmail.com>
URL:		http://members.xoom.com/sashav/aterm
Source:		http://members.xoom.com/sashav/aterm/%{name}-%{version}.tar.gz
Source1:	aterm.wmconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
aterm is a colour vt102 terminal emulator based on
rxvt 2.4.8 with Alfredo Kojima's additions of fast transparency,
intended as an xterm(1) replacement for users who do not require
features such as Tektronix 4014 emulation and toolkit-style
configurability. As a result, aterm uses much less swap space -- a
significant advantage on a machine serving many X sessions.

It was created with AfterStep Window Manger users in mind, but is not
tied to any libraries, and can be used anywhere.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target_platform} \
	--prefix=/usr/X11R6 \
	--enable-utmp \
	--enable-wtmp \
	--enable-background-image \
	--with-png \
	--with-jpeg \
	--enable-transparency \
	--enable-menubar \
	--enable-graphics \
	--enable-next-scroll \
	--disable-backspace-key \
	--disable-delete-key \
	--enable-xgetdefault
make

%install
if [ -d $RPM_BUILD_ROOT ]; then rm -rf $RPM_BUILD_ROOT; fi
mkdir -p $RPM_BUILD_ROOT/usr/X11R6
mkdir -p $RPM_BUILD_ROOT/etc/X11/wmconfig

make prefix=$RPM_BUILD_ROOT/usr/X11R6 install
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/X11/wmconfig/aterm

gzip -9nf $RPM_BUILD_ROOT/usr/X11R6/man/man1/aterm.1
	ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc ChangeLog.gz
%attr(755,root,root) /usr/X11R6/bin/aterm
/usr/X11R6/man/man1/aterm.1.gz
%config(missingok) /etc/X11/wmconfig/aterm
