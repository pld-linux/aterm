Summary:	aterm - terminal emulator in an X Window System
Summary(pl):	aterm - emulator terminala dla X Window System
Name:		aterm
Version:	0.4.2
Release:	1
License:	GPL
Group:		X11/Applications
Group(de):	X11/Applikationen
Group(pl):	X11/Aplikacje
Vendor:		Sasha Vasko <sashav@sprintmail.com>
URL:		http://aterm.sourceforge.net
Source0:	http://download.sourceforge.net/aterm/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		%{name}-utempter.patch
Patch1:		%{name}-wtmp.patch
BuildRequires:	utempter-devel
BuildRequires:	XFree86-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man

%description
aterm is a colour vt102 terminal emulator based on rxvt 2.4.8 with
Alfredo Kojima's additions of fast transparency, intended as an
xterm(1) replacement for users who do not require features such as
Tektronix 4014 emulation and toolkit-style configurability. As a
result, aterm uses much less swap space -- a significant advantage on
a machine serving many X sessions. It was created with AfterStep
Window Manger users in mind, but is not tied to any libraries, and can
be used anywhere.

%description -l pl
aterm jest kolorowym emulatorem terminala vt102, opartym na rxvt 2.4.8
z dodatkami Afredo Kojima do szybkiej emulacji przezroczysto¶ci. W
za³o¿eniu ma zast±piæ program xterm(1) u¿ytkownikom nie wymagaj±cym
takich rzeczy jak emulacja terminala Tektronix 4014 oraz
"toolkit-style configurability". W efekcie aterm u¿ywa du¿o mniej
pamiêci swap -- co jest du¿± zalet± w systemach obs³uguj±cych liczne
sesje Xów. Zosta³ stworzony z my¶l± o u¿ytkownikach AfterStepa, ale
nie jest zwi±zany z ¿adnymi specyficznymi bibliotekami i mo¿e byæ
u¿ywany gdziekolwiek.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd autoconf
autoconf
cp -f ./configure ..
cd ..
export LDFLAGS="%{rpmldflags} -lutempter -L/usr/X11R6/lib"
%configure \
	--enable-ttygid \
	--enable-wtmp \
	--enable-background-image \
	--with-term="xterm-color" \
	--with-png \
	--with-jpeg \
	--enable-transparency \
	--enable-fading \
	--enable-menubar \
	--enable-graphics \
	--enable-xgetdefault
#	--enable-utmp \
#	--enable-next-scroll \

CFLAGS="%{rpmcflags}" 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_applnkdir}/System

%{__make} DESTDIR=$RPM_BUILD_ROOT install
install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/System

tar -cf docs.tar doc/etc doc/menu doc/yodl
gzip -9nf ChangeLog doc/*html doc/README* doc/FAQ doc/TODO docs.tar


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/*.gz *.gz
%attr(755,root,root) %{_bindir}/aterm
%{_mandir}/man1/aterm.1*
%{_applnkdir}/System/aterm.desktop
