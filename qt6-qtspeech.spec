%define beta beta2

Name:		qt6-qtspeech
Version:	6.6.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtspeech.git
Source:		qtspeech-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtspeech-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{qtmajor} Text-to-Speech Library
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6ShaderTools)
BuildRequires:	cmake(Qt6QmlModels)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6Multimedia)
# Just for the ****ing integrity check
BuildRequires:	qt6-qtmultimedia-gstreamer
BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	cmake(OpenGL)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(speech-dispatcher)
BuildRequires:	flite-devel
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} Text-to-Speech library

%global extra_files_TextToSpeech \
%dir %{_qtdir}/plugins/texttospeech \
%{_qtdir}/plugins/texttospeech/libqtexttospeech_mock.so \
%{_qtdir}/plugins/texttospeech/libqtexttospeech_flite.so \
%{_qtdir}/plugins/texttospeech/libqtexttospeech_speechd.so \
%{_qtdir}/qml/QtTextToSpeech

%global extra_devel_files_TextToSpeech \
%{_qtdir}/lib/cmake/Qt6/FindFlite.cmake \
%{_qtdir}/lib/cmake/Qt6/FindSpeechDispatcher.cmake \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtSpeechTestsConfig.cmake \
%{_qtdir}/lib/cmake/Qt6Qml/QmlPlugins/Qt6TextToSpeechQml*.cmake

%qt6libs TextToSpeech

%package examples
Summary:	Example code for the Qt 6 Text-to-Speech module
Group:		Documentation

%description examples
Example code for the Qt 6 Text-to-Speech module

%prep
%autosetup -p1 -n qtspeech%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_MKSPECS_DIR:FILEPATH=%{_qtdir}/mkspecs \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files examples
%{_qtdir}/examples
