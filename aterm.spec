Summary:	aterm - terminal emulator in an X Window System
Summary(pl):	aterm - emulator terminala dla X Window System
Summary(pt_BR):	Um emulador de vt102 colorido
Name:		aterm
Version:	0.4.2
Release:	4
License:	GPL
Vendor:		Sasha Vasko <sashav@sprintmail.com>
Group:		X11/Applications
Source0:	http://download.sourceforge.net/aterm/%{name}-%{version}.tar.bz2
Source1:	%{name}.desktop
Patch0:		%{name}-utempter.patch
Patch1:		%{name}-wtmp.patch
URL:		http://aterm.sourceforge.net/
BuildRequires:	XFree86-devel
BuildRequires:	autoconf
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	utempter-devel
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

%description -l pt_BR
Aterm é um emulador de terminal vt102 baseado no rxvt 2.4.8, com a
adição de fundo transparente. Aterm é um substituto para o xterm, mais
leve.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd autoconf
%{__autoconf}
cp -f ./configure ..
cd ..
LDFLAGS="%{rpmldflags} -lutempter -L%{_libdir}"
export LDFLAGS
%configure \
	--enable-ttygid \
	--enable-wtmp \
	--enable-background-image \
	--with-term=rxvt \
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
install -d $RPM_BUILD_ROOT%{_applnkdir}/Terminals

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Terminals

tar -cf docs.tar doc/etc doc/menu

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog doc/*html doc/README* doc/FAQ doc/TODO docs.tar
%attr(755,root,root) %{_bindir}/aterm
%{_mandir}/man1/aterm.1*
%{_applnkdir}/Terminals/aterm.desktop
