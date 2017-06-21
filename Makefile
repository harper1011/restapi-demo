cwd := $(shell pwd)
buildroot = $(cwd)/rpmbuild
VERSION = $(shell git describe --dirty --always --tags | sed -s 's:-:.:g')

rpm:
	# mimic rpmdev-setuptree manually
	mkdir -p $(buildroot)/{BUILD,RPMS,SRPMS,tmp}
	cp -r $(cwd)/SOURCES $(buildroot)/
	cp -r $(cwd)/SPECS $(buildroot)/
	rpmbuild --define "_topdir $(buildroot)" --define "_version $(VERSION)" -bb $(buildroot)/SPECS/*.spec
	cp $(buildroot)/RPMS/noarch/*.rpm $(cwd)

clean:
	rm -rf $(buildroot)
	rm -f $(cwd)/*.rpm

.PHONY: build rpm clean
