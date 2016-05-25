%define _unpackaged_files_terminate_build 0
%global skipmanaged	1
%global skipnative	0

Name:		corefx
Version:	0.0.1
Release:	1
Summary:	Microsoft .NET Foundation Library
Group:		Development/Languages
License:	Apache-2.0
URL:		http://github.com/dotnet/coreclr
Source0:	%{name}-%{version}.tar.gz
#Source1000:	downloaded_changed.tar.gz

BuildRequires:	cmake
BuildRequires:	llvm
BuildRequires:	libllvm
BuildRequires:	llvm-devel
BuildRequires:	clang
BuildRequires:	clang-devel
BuildRequires:	lldb >= 3.6
BuildRequires:	lldb-devel >= 3.6
BuildRequires:	libunwind libunwind-devel
BuildRequires:	gettext-tools
BuildRequires:  userspace-rcu-devel
BuildRequires:	libicu-devel
BuildRequires:	lttng-ust-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libuuid-devel

# This may become problematic
BuildRequires:	libcurl-devel 
#BuildRequires:	libcurl4-openssl-dev

BuildRequires:	mono-core
BuildRequires:	mono-compiler
BuildRequires:	mono-devel
BuildRequires:	mono-compat

BuildRequires:	python
BuildRequires:	python-xml

# Actually curl/wget are not required, but the build script checks it.
BuildRequires:	curl
BuildRequires:	wget

# The followings are suggested by Jan Kotas
Requires:	userspace-rcu
Requires:	lttng-ust

%description
The .NET Core foundational libraries, called CoreFX.
It includes classes for collections, file systems,
console, XML, async and many others.

%package native
Summary:	Core foundational native libraries
Requires:	coreclr
Requires:	mscorlib

%description native
The native part (.so) of dotnet core foundational libraries

%package managed
Summary:	Core foundational managed libraries
Requires:	coreclr
Requires:	mscorlib

%description managed
The managed part (.dll) of dotnet core foundational libraries


%prep
%setup -q -n %{name}-%{version}
#cp ${SOURCE1000} ./
#tar -xf downloaded_changed.tar.gz


%build

%ifarch x86_64
%define _barch	x64
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/gcc/x86_64-tizen-linux/4.9
export LIBRARY_PATH=$LIBRARY_PATH:/usr/lib64/gcc/x86_64-tizen-linux/4.9
export CFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/x86_64-tizen-linux/4.9/"
export CPPFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/x86_64-tizen-linux/4.9/"
export CXXFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/x86_64-tizen-linux/4.9/"
export CPLUS_INCLUDE_PATH="/usr/include/llvm/:/usr/include/llvm-c/:/usr/include/c++/4.9/:/usr/include/c++/4.9/backward:/usr/include/c++/4.9/x86_64-tizen-linux/:/usr/local/include:/usr/lib/clang/3.6.0/include/:/usr/include/"
export C_INCLUDE_PATH="/usr/include/llvm-c/:/usr/include/"
%define _reldir	bin/Linux.x64.Release
%else
%ifarch aarch64
%define _barch	arm64
# BEWARE: NOT EVER TESTED.
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/gcc/aarch64-tizen-linux/4.9
export LIBRARY_PATH=$LIBRARY_PATH:/usr/lib64/gcc/aarch64-tizen-linux-gnueabi/4.9
export CFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/aarch64-tizen-linux-gnueabi/4.9/"
export CPPFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/aarch64-tizen-linux-gnueabi/4.9/"
export CXXFLAGS="-B/usr/lib64/llvm/ -B/usr/lib64/gcc/aarch64-tizen-linux-gnueabi/4.9/"
export CPLUS_INCLUDE_PATH="/usr/include/llvm/:/usr/include/llvm-c/:/usr/include/c++/4.9/:/usr/include/c++/4.9/backward:/usr/include/c++/4.9/aarch64-tizen-linux-gnueabi/:/usr/local/include:/usr/lib/clang/3.6.0/include/:/usr/include/"
export C_INCLUDE_PATH="/usr/include/llvm-c/:/usr/include/"
%define _reldir	bin/Linux.arm64.Release
%else
%ifarch i586
%define _barch	x86
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/gcc/i586-tizen-linux/4.9
export LIBRARY_PATH=$LIBRARY_PATH:/usr/lib/gcc/i586-tizen-linux/4.9
export CFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/i586-tizen-linux/4.9/"
export CPPFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/i586-tizen-linux/4.9/"
export CXXFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/i586-tizen-linux/4.9/"
export CPLUS_INCLUDE_PATH="/usr/include/llvm/:/usr/include/llvm-c/:/usr/include/c++/4.9/:/usr/include/c++/4.9/backward:/usr/include/c++/4.9/i586-tizen-linux/:/usr/local/include:/usr/lib/clang/3.6.0/include/:/usr/include/"
export C_INCLUDE_PATH="/usr/include/llvm-c/:/usr/include/"
%define _reldir	bin/Linux.x86.Release
%else
%ifarch armv7l
%define _barch	arm
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9
export LIBRARY_PATH=$LIBRARY_PATH:/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9
#export CFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9/ -O2 -g2 -feliminate-unused-debug-types -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 --param=ssp-buffer-size=32 -fdiagnostics-color=never -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -Wp,-D__SOFTFP__ -g"
# DO NOT FORTIFY SOURCE for toolchains like this. This needs to play along with stacks, PCs, and such.
export CFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9/ -O2 --param=ssp-buffer-size=32 -fdiagnostics-color=never -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -Wp,-D__SOFTFP__ -Wno-error=inline-asm -integrated-as -Wno-ignored-attributes -Wno-switch-enum -Wno-switch -Wno-error=switch -Wno-error=switch-enum -w"
export CPPFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9/ -O2 --param=ssp-buffer-size=32 -fdiagnostics-color=never -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -Wp,-D__SOFTFP__ -Wno-error=inline-asm -integrated-as -Wno-ignored-attributes -Wno-switch-enum -Wno-switch -Wno-error=switch -Wno-error=switch-enum -w"
export CXXFLAGS="-B/usr/lib/llvm/ -B/usr/lib/gcc/armv7l-tizen-linux-gnueabi/4.9/ -O2 --param=ssp-buffer-size=32  -fdiagnostics-color=never -march=armv7-a -mtune=cortex-a8 -mlittle-endian -mfpu=neon -mfloat-abi=softfp -Wp,-D__SOFTFP__ -Wno-error=inline-asm -integrated-as -Wno-ignored-attributes -Wno-switch-enum -Wno-switch -Wno-error=switch -Wno-error=switch-enum -w"
export CPLUS_INCLUDE_PATH="/usr/include/llvm/:/usr/include/llvm-c/:/usr/include/c++/4.9/:/usr/include/c++/4.9/backward:/usr/include/c++/4.9/armv7l-tizen-linux-gnueabi/:/usr/local/include:/usr/lib/clang/3.6.0/include/:/usr/include/"
export C_INCLUDE_PATH="/usr/include/llvm-c/:/usr/include/"
%define _reldir	bin/Linux.arm.Release
%else
# write the paths in general!

%endif
%endif
%endif
%endif

%if 0%{skipmanaged}
./build.sh %{_barch} Release native
%else
%if 0%{skipnative}
./build.sh %{_barch} Release managed
%else
./build.sh %{_barch} Release
%endif
%endif

%install
mkdir -p %{buildroot}%{_bindir}/dotnet/
%if 0%{skipmanaged}
cp %{_reldir}/Native/* %{buildwoor}%{_bindir}/dotnet/
%else
%if 0%{skipnative}
cp %{_reldir}/Managed/* %{buildwoor}%{_bindir}/dotnet/
%else
cp %{_reldir}/Native/* %{buildwoor}%{_bindir}/dotnet/
cp %{_reldir}/Managed/* %{buildwoor}%{_bindir}/dotnet/
%endif
%endif

%post native -p /sbin/ldconfig
%postun native -p /sbin/ldconfig

%if 0%{skipnative}
%else
%files native
%dir %{_bindir}/dotnet
%{_bindir}/dotnet/*.so
%endif

%if 0%{skipmanaged}
%else
%dir %{_bindir}/dotnet
%{_bindir}/dotnet/*.dll
%files managed

%endif


%changelog
* Fri Feb 5 2016 MyungJoo Ham <myungjoo.ham@samsung.com> - 0.0.1-1
- Initial spec file for corefx
