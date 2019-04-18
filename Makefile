#
# Makefile for rhsm-api-client
#

NAME	= rhsm-api-client
VERSION := $(shell echo `awk '/^Version:/ {print $$2}' rhsm-api-client.spec`)
MAJOR   := $(shell echo $(VERSION) | cut -f 1 -d '.')
MINOR   := $(shell echo $(VERSION) | cut -f 2 -d '.')
RELEASE := $(shell echo `awk '/^Release:/ {gsub(/\%.*/,""); print $2}' rhsm-api-client.spec`)
REPO = https://github.com/antonioromito/rhsm-api-client/

SUBDIRS = rhsm
PYFILES = $(wildcard *.py)
# OS X via brew
# MSGCAT = /usr/local/Cellar/gettext/0.18.1.1/bin/msgcat
MSGCAT = msgcat

DIST_BUILD_DIR = dist-build
RPM_DEFINES = --define "_topdir %(pwd)/$(DIST_BUILD_DIR)" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir %{_topdir}"
RPM = rpmbuild
RPM_WITH_DIRS = $(RPM) $(RPM_DEFINES)
ARCHIVE_DIR = $(DIST_BUILD_DIR)/$(NAME)-$(VERSION)
DEB_ARCHIVE_DIR = $(DIST_BUILD_DIR)/$(NAME)report-$(VERSION)

SRC_BUILD = $(DIST_BUILD_DIR)/sdist


.PHONY: docs
docs:
	make -C html

.PHONY: build
build:
	for d in $(SUBDIRS); do make -C $$d; [ $$? = 0 ] || exit 1 ; done

.PHONY: install
install:
	mkdir -p $(DESTDIR)/usr/sbin
	mkdir -p $(DESTDIR)/usr/share/$(NAME)/extras
	install -m755 rhsm-cli $(DESTDIR)/usr/sbin/rhsm-cli
	install -m644 AUTHORS README.md $(DESTDIR)/usr/share/$(NAME)/.
	for d in $(SUBDIRS); do make DESTDIR=`cd $(DESTDIR); pwd` -C $$d install; [ $$? = 0 ] || exit 1; done

$(NAME)-$(VERSION).tar.gz: clean
	@mkdir -p $(ARCHIVE_DIR)
	@tar -cv rhsm-cli rhsm AUTHORS LICENSE README.md rhsm-api-client.spec Makefile | tar -x -C $(ARCHIVE_DIR)
	@tar Ccvzf $(DIST_BUILD_DIR) $(DIST_BUILD_DIR)/$(NAME)-$(VERSION).tar.gz $(NAME)-$(VERSION) --exclude-vcs

clean:
	@rm -fv *~ .*~ changenew ChangeLog.old $(NAME)-$(VERSION).tar.gz
	@rm -rf rpm-build
	@for i in `find . -iname *.pyc`; do \
		rm -f $$i; \
	done; \
	for d in $(SUBDIRS); do make -C $$d clean ; done

srpm: clean $(NAME)-$(VERSION).tar.gz
	$(RPM_WITH_DIRS) -ts $(DIST_BUILD_DIR)/$(NAME)-$(VERSION).tar.gz

rpm: clean $(NAME)-$(VERSION).tar.gz
	$(RPM_WITH_DIRS) -tb $(DIST_BUILD_DIR)/$(NAME)-$(VERSION).tar.gz

test:
	nosetests -v --with-cover --cover-package=rhsm --cover-html
