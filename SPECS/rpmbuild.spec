Name:       simple-restapi-server
Version:    0.1
Release:    1

Source0:    restapi.service
Source1:    simple_rest_server.py
Source2:    test_rest_server.py


Summary:    Simple RESTful Server which is used for demo only
BuildArch:  noarch
License:    BSD


%define cwd %(pwd)
%define _app restapi

%description
%{summary}

%clean
rm -rf %{buildroot}

%build
install -d %{buildroot}/opt/script/restapi/
install %{S:1} %{S:2} %{buildroot}/opt/script/restapi/

install -d %{buildroot}%{_unitdir}
install %{S:0} %{buildroot}%{_unitdir}

%files
%defattr(644, root, root, 755)
%attr(755, root, root) /opt/script/restapi/*.py
%config %{_unitdir}/*.service

%post
systemctl daemon-reload
systemctl enable %{_app}

%postun
systemctl stop %{_app}
systemctl disable %{_app}
systemctl daemon-reload

%changelog
* Thu Jun 15 2017 Dapeng Jiao <harper1011@gmail.com> - %{version}-%{release}
- initial build
