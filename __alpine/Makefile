all: 
	cd ../src
	CGO_ENABLED=0 go build . -o ./y2j.exe

prepare:
	sudo /opt/bin/install_golang.sh 1.24.4 amd64
	sudo apk update --no-cache

install:
	test -d $(DESTDIR)$(PREFIX)/bin || mkdir -p $(DESTDIR)$(PREFIX)/bin
	install -pm 755 $(BUILDDIR)/y2j.exe $(DESTDIR)$(PREFIX)/bin/y2j
	strip $(DESTDIR)$(PREFIX)/bin/y2j
