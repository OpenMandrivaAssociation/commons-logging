%bcond_without	bootstrap

Name:           commons-logging
Version:        1.1.1
Release:        5
Summary:        Jakarta Commons Logging Package
License:        Apache License
Group:          Development/Java
URL:            http://commons.apache.org/logging/
Source0:        http://mirror.lwnetwork.org.uk/APACHE/commons/logging/source/%name-%version-src.tar.gz
Patch1:         %name-eclipse-manifest.patch
BuildRequires:  ant
%if !%{with bootstrap}
BuildRequires:	ant-junit
BuildRequires:  avalon-framework
BuildRequires:  avalon-logkit
%endif
BuildRequires:  java-1.6.0-openjdk-devel
BuildRequires:  junit 
BuildRequires:  log4j
BuildRequires:  servlet6
BuildArch:      noarch
%rename jakarta-%name

%description
The commons-logging package provides a simple, component oriented
interface (org.apache.commons.logging.Log) together with wrappers for
logging systems. The user can choose at runtime which system they want
to use. In addition, a small number of basic implementations are
provided to allow users to use the package standalone. 
commons-logging was heavily influenced by Avalon's Logkit and Log4J. The
commons-logging abstraction is meant to minimixe the differences between
the two, and to allow a developer to not tie himself to a particular
logging implementation.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}-src
%apply_patches
sed -i -e 's,-SNAPSHOT,,' *.xml *.pom

# -----------------------------------------------------------------------------

%build
export JAVA_HOME=%_prefix/lib/jvm/java-1.6.0
cat > build.properties <<EOBM
junit.jar=$(build-classpath junit)
log4j.jar=$(build-classpath log4j)
log4j12.jar=$(build-classpath log4j)
%if !%{with bootstrap}
logkit.jar=$(build-classpath avalon-logkit)
avalon-framework.jar=$(build-classpath avalon-framework)
%endif
servletapi.jar=$(build-classpath tomcat6-servlet-2.5-api)
EOBM
%if !%{with bootstrap}
export OPT_JAR_LIST="ant/ant-junit"
%endif
ant -Dsource.version=1.4 -Dtarget.version=1.4 clean compile

(cd src/java && javadoc -d ../../target/docs/api `%{_bindir}/find . -type f -name '*.java'`)

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -p -m 644 target/%{name}-adapters-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-adapters-%{version}.jar
install -p -m 644 target/%{name}-api-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-api-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} jakarta-${jar}; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)
# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a target/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

%files
%defattr(0644,root,root,0755)
%doc PROPOSAL.html STATUS.html LICENSE.txt RELEASE-NOTES.txt
%{_javadir}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
